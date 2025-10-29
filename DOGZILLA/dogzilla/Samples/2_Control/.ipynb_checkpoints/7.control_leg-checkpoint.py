#!/usr/bin/env python
# coding: utf-8



# 导入库  import library
import ipywidgets.widgets as widgets
from IPython.display import display




# Dogzilla drive library
from DOGZILLALib import DOGZILLA
g_dog = DOGZILLA()


# # 控制机器狗的腿运动
# # Control the leg movement of DOGZILLA



# 中文开关，默认为英文 Chinese switch. The default value is English
g_ENABLE_CHINESE = False

Name_widgets = {
    'Reset':("Reset", "恢复默认姿态"),
    'X': ("X", "X"),
    'Y': ("Y", "Y"),
    'Z': ("Z", "Z"),
    'Left_front': ("Left_front", "左前腿"),
    'Right_front': ("Right_front", "右前腿"),
    'Right_rear': ("Right_rear", "右后腿"),
    'Left_rear': ("Left_rear", "左后腿"),
    'Load':("Load", "已加载"),
    'Unload':("Unload", "已卸载")
}




# 恢复默认 Reset
button_Reset = widgets.Button(        
    description=Name_widgets['Reset'][g_ENABLE_CHINESE],
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    icon='uncheck' )

# 加载或卸载腿部舵机  Load or unload leg steering gear
button_leg1 = widgets.Button(        
    description=Name_widgets['Left_front'][g_ENABLE_CHINESE],
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    layout=widgets.Layout(width='100%'),
    icon='check' )
# 加载或卸载腿部舵机  Load or unload leg steering gear
button_leg2 = widgets.Button(        
    description=Name_widgets['Right_front'][g_ENABLE_CHINESE],
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    layout=widgets.Layout(width='100%'),
    icon='check' )
# 加载或卸载腿部舵机  Load or unload leg steering gear
button_leg3 = widgets.Button(        
    description=Name_widgets['Right_rear'][g_ENABLE_CHINESE],
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    layout=widgets.Layout(width='100%'),
    icon='check' )
# 加载或卸载腿部舵机  Load or unload leg steering gear
button_leg4 = widgets.Button(        
    description=Name_widgets['Left_rear'][g_ENABLE_CHINESE],
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    layout=widgets.Layout(width='100%'),
    icon='check' )




# 按键按下事件处理   Key press event processing
def on_button_clicked(b):
    with output:
        print("Button clicked:", b.description)
    if b.description == Name_widgets['Reset'][g_ENABLE_CHINESE]:
        g_dog.load_allmotor()
        g_dog.reset()
        slider_leg1_x.value = 0
        slider_leg1_y.value = 0
        slider_leg1_z.value = 105
        slider_leg2_x.value = 0
        slider_leg2_y.value = 0
        slider_leg2_z.value = 105
        slider_leg3_x.value = 0
        slider_leg3_y.value = 0
        slider_leg3_z.value = 105
        slider_leg4_x.value = 0
        slider_leg4_y.value = 0
        slider_leg4_z.value = 105
        button_leg1.icon = 'check'
        button_leg1.button_style='success'
        button_leg2.icon = 'check'
        button_leg2.button_style='success'
        button_leg3.icon = 'check'
        button_leg3.button_style='success'
        button_leg4.icon = 'check'
        button_leg4.button_style='success'
    
    elif b.description == Name_widgets['Left_front'][g_ENABLE_CHINESE]:
        if b.icon == 'check':
            b.icon = 'uncheck'
            b.button_style=''
            g_dog.unload_motor(1)
            with output:
                print(Name_widgets['Unload'][g_ENABLE_CHINESE] + ":", b.description)
        else:
            b.icon = 'check'
            b.button_style='success'
            g_dog.load_motor(1)
            with output:
                print(Name_widgets['Load'][g_ENABLE_CHINESE] + ":", b.description)
    elif b.description == Name_widgets['Right_front'][g_ENABLE_CHINESE]:
        if b.icon == 'check':
            b.icon = 'uncheck'
            b.button_style=''
            g_dog.unload_motor(2)
            with output:
                print(Name_widgets['Unload'][g_ENABLE_CHINESE] + ":", b.description)
        else:
            b.icon = 'check'
            b.button_style='success'
            g_dog.load_motor(2)
            with output:
                print(Name_widgets['Load'][g_ENABLE_CHINESE] + ":", b.description)
    elif b.description == Name_widgets['Right_rear'][g_ENABLE_CHINESE]:
        if b.icon == 'check':
            b.icon = 'uncheck'
            b.button_style=''
            g_dog.unload_motor(3)
            with output:
                print(Name_widgets['Unload'][g_ENABLE_CHINESE] + ":", b.description)
        else:
            b.icon = 'check'
            b.button_style='success'
            g_dog.load_motor(3)    
            with output:
                print(Name_widgets['Load'][g_ENABLE_CHINESE] + ":", b.description)
    elif b.description == Name_widgets['Left_rear'][g_ENABLE_CHINESE]:
        if b.icon == 'check':
            b.icon = 'uncheck'
            b.button_style=''
            g_dog.unload_motor(4)
            with output:
                print(Name_widgets['Unload'][g_ENABLE_CHINESE] + ":", b.description)
        else:
            b.icon = 'check'
            b.button_style='success'
            g_dog.load_motor(4)  
            with output:
                print(Name_widgets['Load'][g_ENABLE_CHINESE] + ":", b.description)


# 滑块滑动事件处理  Slider event handling
def on_slider_leg1(x, y, z):
    print("   leg1:", x, y, z)
    # button_leg1.icon = 'check'
    # button_leg1.button_style='success'
    motor_id = 1
    coord_id = [x, y, z]
    g_dog.leg(motor_id, coord_id)
    
def on_slider_leg2(x, y, z):
    print("   leg2:", x, y, z)
    # button_leg2.icon = 'check'
    # button_leg2.button_style='success'
    motor_id = 2
    coord_id = [x, y, z]
    g_dog.leg(motor_id, coord_id)
    
def on_slider_leg3(x, y, z):
    print("   leg3:", x, y, z)
    # button_leg3.icon = 'check'
    # button_leg3.button_style='success'
    motor_id = 3
    coord_id = [x, y, z]
    g_dog.leg(motor_id, coord_id)

def on_slider_leg4(x, y, z):
    print("   leg4:", x, y, z)
    # button_leg4.icon = 'check'
    # button_leg4.button_style='success'
    motor_id = 4
    coord_id = [x, y, z]
    g_dog.leg(motor_id, coord_id)




# 关联按键事件回调 Button event callbacks
button_Reset.on_click(on_button_clicked)
button_leg1.on_click(on_button_clicked)
button_leg2.on_click(on_button_clicked)
button_leg3.on_click(on_button_clicked)
button_leg4.on_click(on_button_clicked)




# 创建滑块控制舵机 Create slider to control steering gear
slider_leg1_x = widgets.IntSlider(description=Name_widgets['X'][g_ENABLE_CHINESE]+':', value=0 , min=-35,max=35,step=1, orientation='horizontal')
slider_leg1_y = widgets.IntSlider(description=Name_widgets['Y'][g_ENABLE_CHINESE]+':', value=0 , min=-18,max=18,step=1, orientation='horizontal')
slider_leg1_z = widgets.IntSlider(description=Name_widgets['Z'][g_ENABLE_CHINESE]+':', value=105 , min=75,max=115,step=1, orientation='horizontal')

slider_leg2_x = widgets.IntSlider(description=Name_widgets['X'][g_ENABLE_CHINESE]+':', value=0 , min=-35,max=35,step=1, orientation='horizontal')
slider_leg2_y = widgets.IntSlider(description=Name_widgets['Y'][g_ENABLE_CHINESE]+':', value=0 , min=-18,max=18,step=1, orientation='horizontal')
slider_leg2_z = widgets.IntSlider(description=Name_widgets['Z'][g_ENABLE_CHINESE]+':', value=105 , min=75,max=115,step=1, orientation='horizontal')

slider_leg3_x = widgets.IntSlider(description=Name_widgets['X'][g_ENABLE_CHINESE]+':', value=0 , min=-35,max=35,step=1, orientation='horizontal')
slider_leg3_y = widgets.IntSlider(description=Name_widgets['Y'][g_ENABLE_CHINESE]+':', value=0 , min=-18,max=18,step=1, orientation='horizontal')
slider_leg3_z = widgets.IntSlider(description=Name_widgets['Z'][g_ENABLE_CHINESE]+':', value=105 , min=75,max=115,step=1, orientation='horizontal')

slider_leg4_x = widgets.IntSlider(description=Name_widgets['X'][g_ENABLE_CHINESE]+':', value=0 , min=-35,max=35,step=1, orientation='horizontal')
slider_leg4_y = widgets.IntSlider(description=Name_widgets['Y'][g_ENABLE_CHINESE]+':', value=0 , min=-18,max=18,step=1, orientation='horizontal')
slider_leg4_z = widgets.IntSlider(description=Name_widgets['Z'][g_ENABLE_CHINESE]+':', value=105 , min=75,max=115,step=1, orientation='horizontal')




# 设置舵机运动速度 Set the steering gear speed
g_dog.motor_speed(50)


# ## 布局控件并显示  Layout widgets and display them



# 布局控件并显示  Layout widgets and display them
output = widgets.Output()
box_slider_1 = widgets.interactive(on_slider_leg1, x=slider_leg1_x, y=slider_leg1_y, z=slider_leg1_z)
box_slider_2 = widgets.interactive(on_slider_leg2, x=slider_leg2_x, y=slider_leg2_y, z=slider_leg2_z)
box_slider_3 = widgets.interactive(on_slider_leg3, x=slider_leg3_x, y=slider_leg3_y, z=slider_leg3_z)
box_slider_4 = widgets.interactive(on_slider_leg4, x=slider_leg4_x, y=slider_leg4_y, z=slider_leg4_z)
box_leg1 = widgets.VBox([button_leg1, box_slider_1])
box_leg2 = widgets.VBox([button_leg2, box_slider_2])
box_leg3 = widgets.VBox([button_leg3, box_slider_3])
box_leg4 = widgets.VBox([button_leg4, box_slider_4])
box_h1 = widgets.HBox([box_leg1, box_leg2])
box_h2 = widgets.HBox([box_leg4, box_leg3])
box_display = widgets.VBox([button_Reset, box_h1, box_h2, output])
display(box_display)











