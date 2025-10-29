#!/usr/bin/env python
# coding: utf-8



# 导入库  import library
import ipywidgets.widgets as widgets
from IPython.display import display




# Dogzilla drive library
from DOGZILLALib import DOGZILLA
g_dog = DOGZILLA()


# # 读取数据，包括底板固件版本号、舵机角度、电池电量和姿态角。
# # Read data, including firmware version，steering gear Angle, battery level, and attitude Angle



# 中文开关，默认为英文 Chinese switch. The default value is English
g_ENABLE_CHINESE = False

Name_widgets = {
    'Read_version': ("Read_version", "读取版本号"),
    'Read_battery': ("Read_battery", "读取电压"),
    'Read_motor': ("Read_motor", "读取舵机角度"),
    'Read_roll': ("Read_roll", "读取ROLL"),
    'Read_pitch': ("Read_pitch", "读取PITCH"),
    'Read_yaw': ("Read_yaw", "读取YAW")
}




# 读取固件版本号 Read_version
button_Read_version = widgets.Button(       
    description=Name_widgets['Read_version'][g_ENABLE_CHINESE],
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    icon='uncheck' )


# 读取电压 Read_battery
button_Read_battery = widgets.Button(       
    description=Name_widgets['Read_battery'][g_ENABLE_CHINESE],
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    icon='uncheck' )

# 读取舵机角度 Read_motor
button_Read_motor = widgets.Button(     
    description=Name_widgets['Read_motor'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 读取ROLL Read_roll
button_Read_roll = widgets.Button(        
    description=Name_widgets['Read_roll'][g_ENABLE_CHINESE],         
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 读取PITCH Read_pitch
button_Read_pitch = widgets.Button(        
    description=Name_widgets['Read_pitch'][g_ENABLE_CHINESE],         
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 读取YAW Read_yaw
button_Read_yaw = widgets.Button(        
    description=Name_widgets['Read_yaw'][g_ENABLE_CHINESE],         
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )




# 按键按下事件处理   Key press event processing
def on_button_clicked(b):
    # with output:
    #     print("Button clicked:", b.description)
    if b.description == Name_widgets['Read_version'][g_ENABLE_CHINESE]:
        version = g_dog.read_version()
        with output:
            print("version:", version)
    elif b.description == Name_widgets['Read_battery'][g_ENABLE_CHINESE]:
        battery = g_dog.read_battery()
        with output:
            print("battery:", battery)
    elif b.description == Name_widgets['Read_motor'][g_ENABLE_CHINESE]:
        motor = g_dog.read_motor()
        with output:
            print("motor:", motor)
    elif b.description == Name_widgets['Read_roll'][g_ENABLE_CHINESE]:
        roll = g_dog.read_roll()
        with output:
            print("roll:", roll)
    elif b.description == Name_widgets['Read_pitch'][g_ENABLE_CHINESE]:
        pitch = g_dog.read_pitch()
        with output:
            print("pitch:", pitch)
    elif b.description == Name_widgets['Read_yaw'][g_ENABLE_CHINESE]:
        yaw = g_dog.read_yaw()
        with output:
            print("yaw:", yaw)




# 关联按键事件回调 Button event callbacks
button_Read_version.on_click(on_button_clicked)
button_Read_battery.on_click(on_button_clicked)
button_Read_motor.on_click(on_button_clicked)
button_Read_roll.on_click(on_button_clicked)
button_Read_pitch.on_click(on_button_clicked)
button_Read_yaw.on_click(on_button_clicked)


# ## 布局控件并显示  Layout widgets and display them



# 布局控件并显示  Layout widgets and display them
output = widgets.Output()
box_btn1 = widgets.HBox([button_Read_version, button_Read_battery, button_Read_motor])
box_btn2 = widgets.HBox([button_Read_roll, button_Read_pitch, button_Read_yaw])
box_display = widgets.VBox([box_btn1, box_btn2])
display(box_display)




display(output)











