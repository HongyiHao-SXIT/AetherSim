# 导入库  import library
import cv2
import ipywidgets.widgets as widgets
from IPython.display import display
import time
import threading
import inspect
import ctypes
import numpy as np
import os

# Dogzilla drive library
from DOGZILLALib import DOGZILLA
g_dog = DOGZILLA()

# 中文开关，默认为英文 Chinese switch. The default value is English
g_ENABLE_CHINESE = False

Name_widgets = {
    'Stop_Study': ("Stop_Study", "停止学习"),
    'Start_Study': ("Start_Study", "开始学习"),
    'Study_Action': ("Study_Action", "记录动作"),
    'Clear_Action': ("Clear_Action", "清空动作组"),
    'Play_Action': ("Play_Action", "运行动作组")
}

PATH_ACTION = "/home/pi/DOGZILLA/Samples/3_AI_Visual/Action_Data.txt"

# 恢复默认姿态，并且把机器狗坐着摆放
# Restore the default position and place the robot dog in a sitting position
g_dog.reset()

# 写入动作  Write action
def write_action(wf_path, value):
    if len(value) != 6:
        return
    with open(wf_path, "a") as wf:
        wf_str = str(value[0]) + ', ' + str(value[1]) + ', ' + \
            str(value[2]) + ', ' + str(value[3]) + ', ' + \
            str(value[4]) + ', ' + str(value[5])  + '\n'
        wf.write(wf_str)
        wf.flush()

# 读取所有动作 Read all actions
def read_all_action():
    rf = open(PATH_ACTION, "r+")
    lines = rf.readlines()
    group = ()
    for line in lines:
        if len(line) != 0:
            list = line.split(',')
            if len(list) == 6:
                action = ([int(list[0]), int(list[1]), int(list[2]),
                       int(list[3]), int(list[4]), int(list[5])], )
                group = group + action
    rf.flush()
    return group

# 清除动作，删除PATH_ACTION文件  Clear ACTION to delete the PATH_ACTION file
def clear_action():
    os.system('rm ' + PATH_ACTION)

# 开始学习动作，卸载两个前腿舵机
# Start learning the moves, unloading both front leg steering gear
def start_study():
    g_dog.unload_motor(1)
    time.sleep(.1)
    g_dog.unload_motor(2)

# 学习动作，记录并保存当前动作到文件里
# Learn the action, record and save the current action to a file
def study_action():
    read_angle = g_dog.read_motor(True)
    leg_angle = [0, 0, 0, 0, 0, 0]
    for i in range(6):
        leg_angle[i] = read_angle[i]
    write_action(PATH_ACTION, leg_angle)

# 停止学习动作  Stop learning the action
def stop_study():
    g_dog.load_motor(1)
    time.sleep(.1)
    g_dog.load_motor(2)

# 运行动作组  Operation action group
def play_action():
    group = read_all_action()
    len_group = len(group)
    print("group:", len_group, group)
    motor_id = [11, 12, 13, 21, 22, 23]
    g_dog.motor_speed(50)
    index = 0
    for action in group:
        g_dog.motor(motor_id, action)
        
        if index == 4 or index == 3:
            time.sleep(.5)
        else:
            time.sleep(1.2)
        index = index + 1

# 停止学习 Stop_Study
button_Stop_Study = widgets.Button(         
    description=Name_widgets['Stop_Study'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 开始学习 Start_Study
button_Start_Study = widgets.Button(       
    description=Name_widgets['Start_Study'][g_ENABLE_CHINESE],
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    icon='uncheck' )

# 记录动作 Study_Action
button_Study_Action = widgets.Button(     
    description=Name_widgets['Study_Action'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 清空动作组 Clear_Action
button_Clear_Action = widgets.Button(        
    description=Name_widgets['Clear_Action'][g_ENABLE_CHINESE],         
    button_style='danger', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 运行动作组 Play_Action
button_Play_Action = widgets.Button(        
    description=Name_widgets['Play_Action'][g_ENABLE_CHINESE],        
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 按键按下事件处理   Key press event processing
def on_button_clicked(b):
    with output:
        print("Button clicked:", b.description)
    if b.description == Name_widgets['Stop_Study'][g_ENABLE_CHINESE]:
        stop_study()
    elif b.description == Name_widgets['Start_Study'][g_ENABLE_CHINESE]:
        start_study()
    elif b.description == Name_widgets['Study_Action'][g_ENABLE_CHINESE]:
        study_action()
    elif b.description == Name_widgets['Clear_Action'][g_ENABLE_CHINESE]:
        clear_action()
    elif b.description == Name_widgets['Play_Action'][g_ENABLE_CHINESE]:
        play_action()

# 关联按键事件回调 Button event callbacks
button_Stop_Study.on_click(on_button_clicked)
button_Start_Study.on_click(on_button_clicked)
button_Study_Action.on_click(on_button_clicked)
button_Clear_Action.on_click(on_button_clicked)
button_Play_Action.on_click(on_button_clicked)

output = widgets.Output()
box_btn_1 = widgets.HBox([button_Start_Study, button_Study_Action, button_Stop_Study])
box_btn_2 = widgets.HBox([button_Clear_Action, button_Play_Action])
box_display = widgets.VBox([box_btn_1, box_btn_2, output])
display(box_display)

