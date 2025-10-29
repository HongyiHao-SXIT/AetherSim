# 目标

在不同硬件、不同 CUDA/PyTorch 版本条件下，复现 ABS（Agile But Safe）核心能力，并在允许的情况下融合 ASAP 的“Delta Action（残差动作）对齐”思想以增强 sim-to-real 与跨硬件泛化。

---

## 一、系统总览（你的项目应包含的 4 个可训练模块 + 1 个运行时开关）

* **Agile Policy（敏捷策略）**：端到端、目标驱动（goal-reaching），直接输出 12DoF（或你的机器人关节数）关节位置目标。奖励兼顾“尽快到达目标 + 高速 + 避障”。
* **RA Value Network（Reach-Avoid 值函数）**：基于折扣式 reach-avoid Bellman 方程，离线用敏捷策略 rollout 数据训练，在线作为安全指示器与恢复目标的优化目标。
* **Recovery Policy（恢复策略）**：输入 twist 指令（vx, vy, ωz），快速稳定跟踪；当 RA 值提示风险时接管。
* **Ray-Prediction Network（外感知表征）**：将深度图/点云映射为低维“11 根射线距离”的对数值（或你自定义的稀疏激光束）。
* **Policy Switch（策略切换）**：根据 $\hat V(s)$ 与阈值 $V_{\text{threshold}}$ 切换敏捷/恢复控制，并在风险态时在线搜索“更安全的 twist”。

> 以上 5 个部件彼此解耦，可分别替换传感器、机器人、物理引擎与训练框架。

---

## 二、目录结构建议

```
abs_asap_project/
  configs/
    robot_go1.yaml
    robot_yourbot.yaml
    train_agile.yaml
    train_ra.yaml
    train_recovery.yaml
    train_raynet.yaml
    deploy.yaml
  robots/
    yourbot/urdf/*
    adapters.py        # 关节/尺度/PD/限制适配
  sim/
    isaacgym_env.py    # 或 mujoco_env.py / isaaclab_env.py
    terrain.py
    obstacles.py
    sensors.py         # 深度 → 射线 或 直接 raycast
  abs_core/
    policies.py        # AgilePolicy, RecoveryPolicy
    ra_value.py        # RANetwork + 目标构造 & Bellman 训练
    raynet.py          # Ray-Prediction CNN/UNet
    switch.py          # 策略切换与在线 twist 搜索
    rewards.py         # 奖励分解
    utils.py
  asap_plus/
    delta_action.py    # π_Δ 残差动作模型
    real_dataset.py    # 真实轨迹 I/O
    finetune.py        # 带残差的仿真微调
  train/
    train_agile.py
    train_ra.py
    train_recovery.py
    train_raynet.py
    train_delta_action.py
  deploy/
    run_robot.py       # 读传感器→ray→V_hat→switch→policy→PD
  scripts/
    export_onnx.py
    bench_replay.py
  README.md
```

---

## 三、关键接口（硬件/传感器无关）

```python
# robots/adapters.py
class RobotAdapter:
    def __init__(self, urdf, dof_names, kp, kd, q_limits, qd_limits, tau_limits, action_scale):
        ...
    def action_to_torque(self, q_cmd, q_meas, qd_meas):
        # τ = Kp(q* - q) - Kd q̇
        ...
    def clip_safety(self, q, qd, tau):
        ...
```

```python
# sim/sensors.py
class RayProjector:
    def __init__(self, pattern='forward_fan_11', log_space=True):
        self.dirs = self._make_pattern(pattern)  # 11 根射线，或自定
        self.log_space = log_space
    def from_depth(self, depth_image, K, T_cam_base):
        # 将深度/点云投影到这些方向的最小距离
        # 返回 shape=(N_rays,) 的距离 or log(距离)
        ...
```

---

## 四、核心网络骨架

```python
# abs_core/policies.py
import torch, torch.nn as nn

class MLP(nn.Module):
    def __init__(self, in_dim, out_dim, hidden=(256,256,256), act=nn.ReLU):
        super().__init__()
        layers = []
        last = in_dim
        for h in hidden:
            layers += [nn.Linear(last, h), act()]
            last = h
        layers += [nn.Linear(last, out_dim)]
        self.net = nn.Sequential(*layers)
    def forward(self, x):
        return self.net(x)

class AgilePolicy(nn.Module):
    def __init__(self, obs_dim, act_dim):
        super().__init__()
        self.pi = MLP(obs_dim, act_dim)
    def forward(self, obs):
        return self.pi(obs)  # 关节位置目标 a

class RecoveryPolicy(nn.Module):
    def __init__(self, obs_dim, act_dim):
        super().__init__()
        self.pi = MLP(obs_dim, act_dim)
    def forward(self, obs, twist_cmd):
        z = torch.cat([obs, twist_cmd], dim=-1)
        return self.pi(z)
```

```python
# abs_core/ra_value.py
class RANetwork(nn.Module):
    def __init__(self, obs_dim):
        super().__init__()
        self.v = MLP(obs_dim, 1)
    def forward(self, obs):
        return self.v(obs)  # 估计 \hat V(s)
```

```python
# abs_core/raynet.py
class RayNet(nn.Module):
    def __init__(self, out_rays=11):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 16, 5, 2, 2), nn.ReLU(),
            nn.Conv2d(16, 32, 3, 2, 1), nn.ReLU(),
            nn.Conv2d(32, 64, 3, 2, 1), nn.ReLU(),
            nn.AdaptiveAvgPool2d(1)
        )
        self.mlp = MLP(64, out_rays)
    def forward(self, depth):
        f = self.cnn(depth)[:, :, 0, 0]
        rays = self.mlp(f)
        return rays  # 输出 log 距离，或对数前先软阈
```

---

## 五、训练要点（可直接对照实现）

### 1) Agile Policy（PPO）

* **观测**：$o=\{c_f,\, \omega,\, g,\, G_c,\, T-t,\, q,\, \dot q,\, a_{t-1},\, R\}$。其中 $R$ 为 11 射线的对数距离；$G_c$ 为目标在机体坐标系下的相对位置与期望朝向。
* **动作**：关节位置目标（与硬件 DoF 对齐）。
* **奖励分解**：`penalty + task + regularization`。task 含**软/紧位置跟踪**、**朝向跟踪**、**到点站立**、**敏捷项**（沿前向的速度奖励）与**防发呆项**；regularization 包含姿态/加速度/关节限制/腾空惩罚等。
* **场景**：平地、低台阶、粗糙地面；障碍为若干圆柱或你自定义几何；课程学习（越后越难）。
* **随机化**：摩擦、质量、编码器偏置、关节噪声、ERFI-50 扭矩扰动、ray “幻觉”随机覆盖远距离值。

### 2) RA Value（折扣 RA Bellman）

* 用已训练的敏捷策略在仿真中采样轨迹，构造 $\zeta(s)$（碰撞指示）、$l(s)$（到达目标指示），以 $\gamma_{RA}\in[0,1)$ 训练 $\hat V$。
* 训练完用于：

  * **开关**：$\hat V < V_{thr}$ → Agile；否则 Recovery。
  * **指导**：在风险态时，将搜索的 twist 目标纳入 $\min \hat V$ 目标的约束优化。

### 3) Recovery Policy

* 目标：高频率、强鲁棒地跟踪传入 twist（vx, vy, ωz）并稳定身体。
* 训练：PPO/离线行为克隆均可，含速度/姿态/足端稳定等正则项。

### 4) RayNet

* 自监督：在仿真中通过几何 raycast 得到真值射线距离，以深度图 → 射线 监督训练；部署时用实机深度即可。
* 若有 2D LiDAR，可**绕过 RayNet**，直接用激光束作为 R。

---

## 六、运行时策略切换与在线 twist 搜索

伪代码：

```python
obs = build_obs(proprio, rays, goal, t_left)
V = ra_net(obs)
if V < V_thr:
    a = agile(obs)                      # 直接输出关节目标
else:
    tw = search_safe_twist(obs, V, goal)
    a = recovery(torch.cat([obs, tw], -1))

tau = adapter.action_to_torque(a, q, qd)
```

**search\_safe\_twist**：在限制区域内（|vx|≤v\_max等），以 $J(tw)=\alpha\,\text{goal
dist}(tw)+\beta\,\hat V(s')$ 优化下一步 twist，$s'$ 为一步前向模拟/模型近似后的观测。

---

## 七、ASAP 风格的“残差动作”对齐（可选强化）

1. **采集实机轨迹**：用当前策略在真实机器人上跑若干回合，记录 $s^r_t, a^r_t$。
2. **训练 Δ-Action 模型**：在仿真中重放 $s^r_t$，学习 $\pi_Δ(s_t, a_t)$，使得 $f_{sim}(s_t, a^r_t+Δa_t)$ 与 $s^r_{t+1}$ 贴合。
3. **冻结 $\pi_Δ$ 微调策略**：把 $\pi_Δ$ 注入仿真作为“对齐后的动力学”，再对 Agile/Recovery/RayNet 微调。
4. **部署时移除 $\pi_Δ$**：只保留经过对齐微调后的策略。

> 该流程尤其适合跨硬件（电机/减速器差异）、不同低层驱动（PD/电流环）、不同地面与感知延迟的情况。

---

## 八、版本/工程化建议

* **仿真**：优先 Isaac Gym/Isaac Lab（GPU 并行），若 CUDA/PyTorch 受限可改 MuJoCo + 自行并行、或 Genesis/Isaac Sim。
* **容器**：提供 `Dockerfile` 与 `environment.yml`，暴露 `PYTORCH_VERSION`、`CUDA_VERSION` 两个 ARG，构建时注入具体版本。
* **日志与复现实验**：统一 Hydra/OMEGACONF 配置；wandb/tensorboard 记录回放；保存 `seed+git commit`。
* **ONNX/TS 导出**：部署端仅加载 ONNX/torchscript；在实机上做速率/延迟基准。

---

## 九、最小可行里程碑（建议顺序）

1. **仿真跑通 Agile（无障碍）** → 达到稳定高速。
2. **加入障碍 + Ray 输入** → 学到避障。
3. **训练 RA 值 & 开关** → 观察风险态时启用恢复。
4. **训练 Recovery** → 在拥挤/突发障碍下保持零碰撞。
5. **实机短程验证** → 采集数据并做 Δ-Action 对齐（ASAP+）。
6. **端到端部署** → 长时、动态障碍、弱光/噪声条件下测试。

---

## 十、常见适配坑位与修复

* **关节数量/顺序不一致**：在 `RobotAdapter` 中做映射与尺度统一；奖励/正则里的关节上限来自你的硬件限值。
* **相机/FoV 不同**：重采样到相同射线分布；或直接改成 LiDAR beams。
* **里程计漂移**：Agile 的目标是相对位姿；短时漂移可容忍；必要时在恢复阶段用视觉/外参重置。
* **延迟/频率差异**：恢复策略提高控制频率（200Hz）；Agile/RA/RayNet 50Hz；根据硬件改。
* **碰撞定义**：务必与真实机器人形状匹配；脚部**水平碰撞**视为失败（可按需放宽）。

---

## 十一、配置片段示例

```yaml
# configs/train_agile.yaml
obs:
  rays: 11
  use_log_rays: true
  include: [cf, omega, g, goal_rel, t_left, q, qd, a_prev, rays]
reward:
  penalty: {undesired_collision: -100}
  task:
    pos_soft: {w: 60, sigma: 2.0, Tr: 2.0}
    pos_tight:{w: 60, sigma: 0.5, Tr: 1.0}
    heading:  {w: 30, sigma: 1.0, Tr: 2.0, enable_dist_lt: 2.0}
    stand:    {w: -10, Tr: 1.0}
    agile:    {w: 10, vmax: 4.5, fwd_angle_deg: 105}
    stall:    {w: -20}
regularization:
  fly: -20
  tau_l2: -5e-4
  qd_l2: -5e-4
  q_lims: -20
  tau_clip_over: -20
  qd_clip_over: -20
randomization:
  friction: [0.4, 1.1]
  base_mass: [-1.5, 1.5]
  erfi50_per_level: 0.78
  illusions: true
ppo:
  n_envs: 1024
  steps_per_update: 16384
  lr: 3e-4
  gamma: 0.99
  gae_lambda: 0.95
```

---

## 十二、验证清单（交付/答辩友好）

* [ ] 仿真基准视频（无/有障碍各 3 段）
* [ ] RA 值热力图 + 开关事件时间轴
* [ ] 恢复策略介入次数/时长统计
* [ ] 实机短测视频 + 碰撞为 0 的里程统计
* [ ] Δ-Action 微调前后对比曲线（位置/速度/落足误差）
* [ ] ablation：去掉 RA / 去掉 RayNet / 去掉 Δ-Action 的退化情况

---

如需，我可以把以上骨架直接打包成可运行的最小工程（含占位数据与伪环境），并按你的 CUDA/PyTorch 版本出一份 `Dockerfile` 与 `conda` 环境。
