import ipywidgets.widgets as widgets
from IPython.display import display

from DOGZILLALib import DOGZILLA
g_dog = DOGZILLA()

g_ENABLE_CHINESE = False

Name_widgets = {
    'Lie_Down': ("Lie_Down", "趴下"),
    'Stand_Up': ("Stand_Up", "站起"),
    'Crawl': ("Crawl", "匍匐前进"),
    'Turn_Around': ("Turn_Around", "转圈"),
    'Mark_Time': ("Mark_Time", "原地踏步"),
    'Squat': ("Squat", "蹲起"),
    'Turn_Roll': ("Turn_Roll", "转动Roll"),
    'Turn_Pitch': ("Turn_Pitch", "转动Pitch"),
    'Turn_Yaw': ("Turn_Yaw", "转动Yaw"),
    '3_Axis': ("3_Axis", "三轴联动"),
    'Pee': ("Pee", "撒尿"),
    'Sit_Down': ("Sit_Down", "坐下"),
    'Wave_Hand': ("Wave_Hand", "招手"),
    'Stretch': ("Stretch", "伸懒腰"),
    'Wave_Body': ("Wave_Body", "波浪"),
    'Swing': ("Swing", "左右摇摆"),
    'Pray': ("Pray", "求食"),
    'Seek': ("Seek", "找食物"),
    'Handshake': ("Handshake", "握手"),
    'Rotation': ("Rotation", "动作轮播"),
    'Reset': ("Reset", "恢复初始姿态"),
}

button_action_1 = widgets.Button(        
    description=Name_widgets['Lie_Down'][g_ENABLE_CHINESE],     
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_action_2 = widgets.Button(     
    description=Name_widgets['Stand_Up'][g_ENABLE_CHINESE],     
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )


button_action_3 = widgets.Button(      
    description=Name_widgets['Crawl'][g_ENABLE_CHINESE],      
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_action_4 = widgets.Button(       
    description=Name_widgets['Turn_Around'][g_ENABLE_CHINESE],       
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_action_5 = widgets.Button(     
    description=Name_widgets['Mark_Time'][g_ENABLE_CHINESE],      
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_action_6 = widgets.Button(       
    description=Name_widgets['Squat'][g_ENABLE_CHINESE],      
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_action_7 = widgets.Button(        
    description=Name_widgets['Turn_Roll'][g_ENABLE_CHINESE],      
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_action_8 = widgets.Button(     
    description=Name_widgets['Turn_Pitch'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_action_9 = widgets.Button(       
    description=Name_widgets['Turn_Yaw'][g_ENABLE_CHINESE],      
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )


button_action_10 = widgets.Button(       
    description=Name_widgets['3_Axis'][g_ENABLE_CHINESE],       
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_action_11 = widgets.Button(         
    description=Name_widgets['Pee'][g_ENABLE_CHINESE],     
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_action_12 = widgets.Button(      
    description=Name_widgets['Sit_Down'][g_ENABLE_CHINESE],       
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_action_13 = widgets.Button(      
    description=Name_widgets['Wave_Hand'][g_ENABLE_CHINESE],     
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_action_14 = widgets.Button(       
    description=Name_widgets['Stretch'][g_ENABLE_CHINESE],       
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_action_15 = widgets.Button(       
    description=Name_widgets['Wave_Body'][g_ENABLE_CHINESE],       
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_action_16 = widgets.Button(        
    description=Name_widgets['Swing'][g_ENABLE_CHINESE],      
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )


button_action_17 = widgets.Button(        
    description=Name_widgets['Pray'][g_ENABLE_CHINESE],      
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_action_18 = widgets.Button(         
    description=Name_widgets['Seek'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_action_19 = widgets.Button(       
    description=Name_widgets['Handshake'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_Rotation = widgets.Button(        
    description=Name_widgets['Rotation'][g_ENABLE_CHINESE],       
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

button_Reset = widgets.Button(      
    description=Name_widgets['Reset'][g_ENABLE_CHINESE],      
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

def on_button_clicked(b):
    with output:
        print("Button clicked:", b.description)
    if b.description == Name_widgets['Reset'][g_ENABLE_CHINESE]:
        g_dog.action(0xff)
        if button_Rotation.icon == 'check':
            button_Rotation.icon = 'uncheck'
            g_dog.perform(0)
    elif b.description == Name_widgets['Rotation'][g_ENABLE_CHINESE]:
        b.icon == 'check'
        g_dog.perform(1)
    elif b.description == Name_widgets['Lie_Down'][g_ENABLE_CHINESE]:
        g_dog.action(1)
    elif b.description == Name_widgets['Stand_Up'][g_ENABLE_CHINESE]:
        g_dog.action(2)
    elif b.description == Name_widgets['Crawl'][g_ENABLE_CHINESE]:
        g_dog.action(3)
    elif b.description == Name_widgets['Turn_Around'][g_ENABLE_CHINESE]:
        g_dog.action(4)
    elif b.description == Name_widgets['Mark_Time'][g_ENABLE_CHINESE]:
        g_dog.action(5)
    elif b.description == Name_widgets['Squat'][g_ENABLE_CHINESE]:
        g_dog.action(6)
    elif b.description == Name_widgets['Turn_Roll'][g_ENABLE_CHINESE]:
        g_dog.action(7)
    elif b.description == Name_widgets['Turn_Pitch'][g_ENABLE_CHINESE]:
        g_dog.action(8)
    elif b.description == Name_widgets['Turn_Yaw'][g_ENABLE_CHINESE]:
        g_dog.action(9)
    elif b.description == Name_widgets['3_Axis'][g_ENABLE_CHINESE]:
        g_dog.action(10)
    elif b.description == Name_widgets['Pee'][g_ENABLE_CHINESE]:
        g_dog.action(11)
    elif b.description == Name_widgets['Sit_Down'][g_ENABLE_CHINESE]:
        g_dog.action(12)
    elif b.description == Name_widgets['Wave_Hand'][g_ENABLE_CHINESE]:
        g_dog.action(13)
    elif b.description == Name_widgets['Stretch'][g_ENABLE_CHINESE]:
        g_dog.action(14)
    elif b.description == Name_widgets['Wave_Body'][g_ENABLE_CHINESE]:
        g_dog.action(15)
    elif b.description == Name_widgets['Swing'][g_ENABLE_CHINESE]:
        g_dog.action(16)
    elif b.description == Name_widgets['Pray'][g_ENABLE_CHINESE]:
        g_dog.action(17)
    elif b.description == Name_widgets['Seek'][g_ENABLE_CHINESE]:
        g_dog.action(18)
    elif b.description == Name_widgets['Handshake'][g_ENABLE_CHINESE]:
        g_dog.action(19)

button_action_1.on_click(on_button_clicked)
button_action_2.on_click(on_button_clicked)
button_action_3.on_click(on_button_clicked)
button_action_4.on_click(on_button_clicked)
button_action_5.on_click(on_button_clicked)
button_action_6.on_click(on_button_clicked)
button_action_7.on_click(on_button_clicked)
button_action_8.on_click(on_button_clicked)
button_action_9.on_click(on_button_clicked)
button_action_10.on_click(on_button_clicked)
button_action_11.on_click(on_button_clicked)
button_action_12.on_click(on_button_clicked)
button_action_13.on_click(on_button_clicked)
button_action_14.on_click(on_button_clicked)
button_action_15.on_click(on_button_clicked)
button_action_16.on_click(on_button_clicked)
button_action_17.on_click(on_button_clicked)
button_action_18.on_click(on_button_clicked)
button_action_19.on_click(on_button_clicked)
button_Rotation.on_click(on_button_clicked)
button_Reset.on_click(on_button_clicked)

output = widgets.Output()
box_btn_1 = widgets.HBox([button_action_1, button_action_2, button_action_3, button_action_4, button_Rotation])
box_btn_2 = widgets.HBox([button_action_5, button_action_6, button_action_7, button_action_8, button_Reset])
box_btn_3 = widgets.HBox([button_action_9, button_action_10, button_action_11, button_action_12])
box_btn_4 = widgets.HBox([button_action_13, button_action_14, button_action_15, button_action_16])
box_btn_5 = widgets.HBox([button_action_17, button_action_18, button_action_19])

box_v = widgets.VBox([box_btn_1, box_btn_2, box_btn_3, box_btn_4, box_btn_5])
box_display = widgets.VBox([box_v, output])
display(box_display)




