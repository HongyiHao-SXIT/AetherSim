import ipywidgets.widgets as widgets
from IPython.display import display

from DOGZILLALib import DOGZILLA
g_dog = DOGZILLA()

g_ENABLE_CHINESE = False

Name_widgets = {
    'Stop': ("Stop", "停止"),
    'Forward': ("Forward", "前进"),
    'Backward': ("Backward", "后退"),
    'Left': ("Left", "左平移"),
    'Right': ("Right", "右平移"),
    'TurnLeft': ("TurnLeft", "向左转"),
    'TurnRight': ("TurnRight", "向右转")
}

button_stop = widgets.Button(       
    description=Name_widgets['Stop'][g_ENABLE_CHINESE],
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    icon='uncheck' )

# 前进 Forward
button_forward = widgets.Button(     
    description=Name_widgets['Forward'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 后退 Backward
button_backward = widgets.Button(        
    description=Name_widgets['Backward'][g_ENABLE_CHINESE],         
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 左平移 Move Left
button_move_left = widgets.Button(        
    description=Name_widgets['Left'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 右平移 Move Right
button_move_right = widgets.Button(         
    description=Name_widgets['Right'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 向左转 TurnLeft
button_turn_left = widgets.Button(        
    description=Name_widgets['TurnLeft'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 向右转 TurnRight
button_turn_right = widgets.Button(        
    description=Name_widgets['TurnRight'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

def ALL_Uncheck():
    button_stop.icon = 'uncheck'
    button_forward.icon = 'uncheck'
    button_backward.icon = 'uncheck'
    button_move_left.icon = 'uncheck'
    button_move_right.icon = 'uncheck'
    button_turn_left.icon = 'uncheck'
    button_turn_right.icon = 'uncheck'


# 按键按下事件处理   Key press event processing
def on_button_clicked(b):
    ALL_Uncheck()
    b.icon = 'check'
    with output:
        print("Button clicked:", b.description)
    if b.description == Name_widgets['Stop'][g_ENABLE_CHINESE]:
        g_dog.stop()
        b.icon = 'uncheck'
    elif b.description == Name_widgets['Forward'][g_ENABLE_CHINESE]:
        g_dog.stop()
        g_dog.forward(20)
    elif b.description == Name_widgets['Backward'][g_ENABLE_CHINESE]:
        g_dog.stop()
        g_dog.back(20)
    elif b.description == Name_widgets['Left'][g_ENABLE_CHINESE]:
        g_dog.stop()
        g_dog.left(18)
    elif b.description == Name_widgets['Right'][g_ENABLE_CHINESE]:
        g_dog.stop()
        g_dog.right(18)
    elif b.description == Name_widgets['TurnLeft'][g_ENABLE_CHINESE]:
        g_dog.stop()
        g_dog.turnleft(70)
    elif b.description == Name_widgets['TurnRight'][g_ENABLE_CHINESE]:
        g_dog.stop()
        g_dog.turnright(70)

button_stop.on_click(on_button_clicked)
button_forward.on_click(on_button_clicked)
button_backward.on_click(on_button_clicked)
button_move_left.on_click(on_button_clicked)
button_move_right.on_click(on_button_clicked)
button_turn_left.on_click(on_button_clicked)
button_turn_right.on_click(on_button_clicked)

output = widgets.Output()
box_btn1 = widgets.VBox([button_forward, button_backward])
box_btn2 = widgets.VBox([button_move_left, button_move_right])
box_btn3 = widgets.VBox([button_turn_left, button_turn_right])
box_h = widgets.HBox([box_btn1, box_btn2, box_btn3, button_stop])
box_display = widgets.VBox([box_h, output])
display(box_display)





