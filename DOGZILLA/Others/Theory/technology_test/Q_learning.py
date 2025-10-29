import numpy as np
import random
import matplotlib.pyplot as plt

class PacmanEnv:
    def __init__(self, size=5):
        self.size = size
        self.reset()

    def reset(self):
        self.pacman_pos = [0, 0]
        self.food_pos = [self.size - 1, self.size - 1]
        self.walls = [[1, 1], [2, 2], [3, 1]]
        return self._get_state()

    def _get_state(self):
        return (self.pacman_pos[0], self.pacman_pos[1])

    def step(self, action):
        x, y = self.pacman_pos
        if action == 0:
            x = max(0, x - 1)
        elif action == 1:
            x = min(self.size - 1, x + 1)
        elif action == 2:
            y = max(0, y - 1)
        elif action == 3:
            y = min(self.size - 1, y + 1)

        if [x, y] in self.walls:
            x, y = self.pacman_pos

        self.pacman_pos = [x, y]

        if self.pacman_pos == self.food_pos:
            return self._get_state(), 10, True
        else:
            return self._get_state(), -1, False

def train_q_learning(episodes=1000):
    env = PacmanEnv()
    q_table = np.zeros((env.size, env.size, 4))
    
    alpha = 0.1
    gamma = 0.9
    epsilon = 0.2
    
    episode_rewards = np.zeros(episodes)
    episode_steps = np.zeros(episodes)
    success_rates = np.zeros(episodes // 50 + 1)
    
    for episode in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0
        steps = 0
        
        while not done:
            if random.uniform(0, 1) < epsilon:
                action = random.randint(0, 3)
            else:
                action = np.argmax(q_table[state[0], state[1]])
            
            next_state, reward, done = env.step(action)
            total_reward += reward
            steps += 1
            
            old_value = q_table[state[0], state[1], action]
            next_max = np.max(q_table[next_state[0], next_state[1]])
            new_value = old_value + alpha * (reward + gamma * next_max - old_value)
            q_table[state[0], state[1], action] = new_value
            
            state = next_state
        
        episode_rewards[episode] = total_reward
        episode_steps[episode] = steps
        
        if (episode + 1) % 50 == 0:
            batch_start = max(0, episode - 49)
            success_rate = np.mean(episode_rewards[batch_start:episode+1] > 0)
            success_rates[episode//50] = success_rate
            print(f"Episode {episode + 1}: Avg reward={np.mean(episode_rewards[batch_start:episode+1]):.1f}, "
                  f"Success rate={success_rate:.2%}, Avg steps={np.mean(episode_steps[batch_start:episode+1]):.1f}")
    
    print("\nTraining summary:")
    print(f"Overall success rate: {np.mean(episode_rewards > 0):.2%}")
    print(f"Average reward: {np.mean(episode_rewards):.2f}")
    print(f"Average steps: {np.mean(episode_steps):.2f}")
    
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 3, 1)
    plt.plot(np.convolve(episode_rewards, np.ones(50)/50, mode='valid'))
    plt.title('Moving Avg Reward (window=50)')
    plt.xlabel('Episode')
    plt.ylabel('Avg Reward')
    
    plt.subplot(1, 3, 2)
    plt.plot(success_rates)
    plt.title('Success Rate (per 50 episodes)')
    plt.xlabel('Batch (50 episodes)')
    plt.ylabel('Success Rate')
    
    plt.subplot(1, 3, 3)
    plt.plot(np.convolve(episode_steps, np.ones(50)/50, mode='valid'))
    plt.title('Moving Avg Steps (window=50)')
    plt.xlabel('Episode')
    plt.ylabel('Avg Steps')
    
    plt.tight_layout()
    plt.savefig('training_stats.png')
    plt.close()
    
    return q_table, episode_rewards, success_rates

def test_agent(q_table, num_tests=10):
    env = PacmanEnv()
    test_results = {
        'success': 0,
        'steps': [],
        'paths': []
    }
    
    for test in range(num_tests):
        state = env.reset()
        done = False
        steps = 0
        path = [state]
        
        while not done and steps < 50:
            action = np.argmax(q_table[state[0], state[1]])
            state, _, done = env.step(action)
            path.append(state)
            steps += 1
        
        test_results['steps'].append(steps)
        test_results['paths'].append(path)
        if done:
            test_results['success'] += 1
    
    success_rate = test_results['success'] / num_tests
    avg_steps = np.mean(test_results['steps'])
    
    print(f"\nTest results ({num_tests} runs):")
    print(f"Success rate: {success_rate:.2%}")
    print(f"Average steps: {avg_steps:.1f}")
    
    shortest_path = min(test_results['paths'], key=len)
    print("\nShortest path example:")
    for i, pos in enumerate(shortest_path):
        print(f"Step {i}: {pos}")
    
    return test_results

if __name__ == "__main__":
    q_table, rewards, success_rates = train_q_learning(episodes=1000)
    test_results = test_agent(q_table)