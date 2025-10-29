import ipywidgets.widgets as widgets
from IPython.display import display

from DOGZILLALib import DOGZILLA
g_dog = DOGZILLA()

g_ENABLE_CHINESE = False

Name_widgets = {
    'Reset':("Reset", "恢复默认姿态"),
    'Shoulder': ("Shoulder", "肩部"),
    'Thigh': ("Thigh", "大腿"),
    'Calf': ("Calf", "小腿"),
    'Left_front': ("Left_front", "左前腿"),
    'Right_front': ("Right_front", "右前腿"),
    'Right_rear': ("Right_rear", "右后腿"),
    'Left_rear': ("Left_rear", "左后腿"),
    'Load':("Load", "已加载"),
    'Unload':("Unload", "已卸载"),
    'Load_ALL':("Load_ALL", "加载全部舵机"),
    'Unload_ALL':("Unload_ALL", "卸载全部舵机"),
    'Motor_speed':("Motor_speed", "舵机速度")
}

button_Reset = widgets.Button(        
    description=Name_widgets['Reset'][g_ENABLE_CHINESE],
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    icon='uncheck' )

# 已加载全部舵机 Load_ALL
button_Load_ALL = widgets.Button(        
    description=Name_widgets['Load_ALL'][g_ENABLE_CHINESE],
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    icon='uncheck' )

# 已卸载全部舵机 Unload_ALL
button_Unload_ALL = widgets.Button(        
    description=Name_widgets['Unload_ALL'][g_ENABLE_CHINESE],
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

def on_button_clicked(b):
    with output:
        print("Button clicked:", b.description)
    if b.description == Name_widgets['Reset'][g_ENABLE_CHINESE]:
        g_dog.load_allmotor()
        g_dog.reset()
        slider_a11.value = 14
        slider_a12.value = 48
        slider_a13.value = 0
        slider_a21.value = 14
        slider_a22.value = 48
        slider_a23.value = 0
        slider_a31.value = 14
        slider_a32.value = 48
        slider_a33.value = 0
        slider_a41.value = 14
        slider_a42.value = 48
        slider_a43.value = 0
        slider_motor_speed.value = 30
        button_leg1.icon = 'check'
        button_leg1.button_style='success'
        button_leg2.icon = 'check'
        button_leg2.button_style='success'
        button_leg3.icon = 'check'
        button_leg3.button_style='success'
        button_leg4.icon = 'check'
        button_leg4.button_style='success'
    
    elif b.description == Name_widgets['Load_ALL'][g_ENABLE_CHINESE]:
        g_dog.load_allmotor()
        button_leg1.icon = 'check'
        button_leg1.button_style='success'
        button_leg2.icon = 'check'
        button_leg2.button_style='success'
        button_leg3.icon = 'check'
        button_leg3.button_style='success'
        button_leg4.icon = 'check'
        button_leg4.button_style='success'
    elif b.description == Name_widgets['Unload_ALL'][g_ENABLE_CHINESE]:
        g_dog.unload_allmotor()
        button_leg1.icon = 'uncheck'
        button_leg1.button_style=''
        button_leg2.icon = 'uncheck'
        button_leg2.button_style=''
        button_leg3.icon = 'uncheck'
        button_leg3.button_style=''
        button_leg4.icon = 'uncheck'
        button_leg4.button_style=''
        
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
def on_slider_leg1(a3, a2, a1):
    print("ID 11~13:" , (a3, a2, a1))
    # button_leg1.icon = 'check'
    # button_leg1.button_style='success'
    motor_id = [11, 12, 13]
    angle_id = [a1, a2, a3]
    g_dog.motor(motor_id, angle_id)
    
def on_slider_leg2(a3, a2, a1):
    print("ID 21~23:" , (a3, a2, a1))
    # button_leg2.icon = 'check'
    # button_leg2.button_style='success'
    motor_id = [21, 22, 23]
    angle_id = [a1, a2, a3]
    g_dog.motor(motor_id, angle_id)
    
def on_slider_leg3(a3, a2, a1):
    print("ID 31~33:" , (a3, a2, a1))
    # button_leg3.icon = 'check'
    # button_leg3.button_style='success'
    motor_id = [31, 32, 33]
    angle_id = [a1, a2, a3]
    g_dog.motor(motor_id, angle_id)
    
def on_slider_leg4(a3, a2, a1):
    print("ID 41~43:" , (a3, a2, a1))
    # button_leg4.icon = 'check'
    # button_leg4.button_style='success'
    motor_id = [41, 42, 43]
    angle_id = [a1, a2, a3]
    g_dog.motor(motor_id, angle_id)
    
    
def on_slider_motor_speed(speed):
    print("   motor_speed:", speed)
    g_dog.motor_speed(speed)


# In[ ]:


# 关联按键事件回调 Button event callbacks
button_Reset.on_click(on_button_clicked)
button_leg1.on_click(on_button_clicked)
button_leg2.on_click(on_button_clicked)
button_leg3.on_click(on_button_clicked)
button_leg4.on_click(on_button_clicked)
button_Load_ALL.on_click(on_button_clicked)
button_Unload_ALL.on_click(on_button_clicked)


# In[ ]:


# 创建滑块控制舵机 Create slider to control steering gear
slider_a13 = widgets.IntSlider(description=Name_widgets['Shoulder'][g_ENABLE_CHINESE]+':', value=0 , min=-31,max=31,step=1, orientation='horizontal')
slider_a12 = widgets.IntSlider(description=Name_widgets['Thigh'][g_ENABLE_CHINESE]+':', value=48 , min=-66,max=93,step=1, orientation='horizontal')
slider_a11 = widgets.IntSlider(description=Name_widgets['Calf'][g_ENABLE_CHINESE]+':', value=14 , min=-73,max=57,step=1, orientation='horizontal')

slider_a23 = widgets.IntSlider(description=Name_widgets['Shoulder'][g_ENABLE_CHINESE]+':', value=0 , min=-31,max=31,step=1, orientation='horizontal')
slider_a22 = widgets.IntSlider(description=Name_widgets['Thigh'][g_ENABLE_CHINESE]+':', value=48 , min=-66,max=93,step=1, orientation='horizontal')
slider_a21 = widgets.IntSlider(description=Name_widgets['Calf'][g_ENABLE_CHINESE]+':', value=14 , min=-73,max=57,step=1, orientation='horizontal')

slider_a33 = widgets.IntSlider(description=Name_widgets['Shoulder'][g_ENABLE_CHINESE]+':', value=0 , min=-31,max=31,step=1, orientation='horizontal')
slider_a32 = widgets.IntSlider(description=Name_widgets['Thigh'][g_ENABLE_CHINESE]+':', value=48 , min=-66,max=93,step=1, orientation='horizontal')
slider_a31 = widgets.IntSlider(description=Name_widgets['Calf'][g_ENABLE_CHINESE]+':', value=14 , min=-73,max=57,step=1, orientation='horizontal')

slider_a43 = widgets.IntSlider(description=Name_widgets['Shoulder'][g_ENABLE_CHINESE]+':', value=0 , min=-31,max=31,step=1, orientation='horizontal')
slider_a42 = widgets.IntSlider(description=Name_widgets['Thigh'][g_ENABLE_CHINESE]+':', value=48 , min=-66,max=93,step=1, orientation='horizontal')
slider_a41 = widgets.IntSlider(description=Name_widgets['Calf'][g_ENABLE_CHINESE]+':', value=14 , min=-73,max=57,step=1, orientation='horizontal')


slider_motor_speed = widgets.IntSlider(description=Name_widgets['Motor_speed'][g_ENABLE_CHINESE]+':', value=50 , min=0,max=255,step=5, orientation='horizontal')


# ## 布局控件并显示  Layout widgets and display them

# In[ ]:


# 布局控件并显示  Layout widgets and display them
output = widgets.Output()
box_slider_1 = widgets.interactive(on_slider_leg1, a3=slider_a13, a2=slider_a12, a1=slider_a11)
box_slider_2 = widgets.interactive(on_slider_leg2, a3=slider_a23, a2=slider_a22, a1=slider_a21)
box_slider_3 = widgets.interactive(on_slider_leg3, a3=slider_a33, a2=slider_a32, a1=slider_a31)
box_slider_4 = widgets.interactive(on_slider_leg4, a3=slider_a43, a2=slider_a42, a1=slider_a41)
box_motor_speed = widgets.interactive(on_slider_motor_speed, speed=slider_motor_speed)
box_leg1 = widgets.VBox([button_leg1, box_slider_1])
box_leg2 = widgets.VBox([button_leg2, box_slider_2])
box_leg3 = widgets.VBox([button_leg3, box_slider_3])
box_leg4 = widgets.VBox([button_leg4, box_slider_4])
box_h1 = widgets.HBox([box_leg1, box_leg2])
box_h2 = widgets.HBox([box_leg4, box_leg3])
box_h = widgets.HBox([button_Reset, button_Load_ALL, button_Unload_ALL])
box_display = widgets.VBox([box_h, box_motor_speed, box_h1, box_h2, output])
display(box_display)

