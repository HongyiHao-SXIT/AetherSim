#!/usr/bin/env python
# coding: utf-8



# 导入库  import library
import ipywidgets.widgets as widgets
from IPython.display import display




# Dogzilla drive library
from DOGZILLALib import DOGZILLA
g_dog = DOGZILLA()


# # 机器狗自稳模式。自稳状态下，机器狗将自动调节姿态角以保持背部处于水平位置，不可在开启时手动设定姿态角。
# # Robot dog self-stabilization mode. In the self-stable state, the robot dog will automatically adjust the attitude Angle to keep the back in a horizontal position. It is not allowed to manually set the attitude Angle when the robot dog is turned on.



# 中文开关，默认为英文 Chinese switch. The default value is English
g_ENABLE_CHINESE = False

Name_widgets = {
    'Stabilizing_mode': ("Stabilizing_mode", "自稳模式"),
    'ON':("ON", "已开启"),
    'OFF':("OFF", "已关闭"),
}




# 自稳模式  Stabilizing mode
button_Stable = widgets.Button(  
    value=False,  
    description=Name_widgets['Stabilizing_mode'][g_ENABLE_CHINESE],      
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )




# 按键按下事件处理   Key press event processing
def on_button_clicked(b):
    
    if b.description == Name_widgets['Stabilizing_mode'][g_ENABLE_CHINESE]:
        if b.icon == 'uncheck':
            with output:
                print("Button clicked:", b.description, Name_widgets['ON'][g_ENABLE_CHINESE])
            b.icon = 'check'
            g_dog.imu(1)
        else:
            with output:
                print("Button clicked:", b.description, Name_widgets['OFF'][g_ENABLE_CHINESE])
            b.icon = 'uncheck'
            g_dog.imu(0)




# 关联按键事件回调 Button event callbacks
button_Stable.on_click(on_button_clicked)


# ## 布局控件并显示  Layout widgets and display them



output = widgets.Output()
box_display = widgets.VBox([button_Stable, output])
display(box_display)






