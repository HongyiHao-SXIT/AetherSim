import ipywidgets.widgets as widgets
from IPython.display import display

from DOGZILLALib import DOGZILLA
g_dog = DOGZILLA()

g_ENABLE_CHINESE = False

Name_widgets = {
    'Stop': ("Stop", "停止"),
    'Normal': ("Normal", "默认步频"),
    'Slow': ("Slow", "慢速步频"),
    'High': ("High", "高速步频"),
    'Step_X': ("Step_X", "前进后退X"),
    'Step_Y': ("Step_Y", "左右平移Y"),
    'Speed_Z': ("Speed_Z", "左右旋转Z")
}

g_last_x = 0
g_last_y = 0
g_last_z = 0

button_stop = widgets.Button(       
    description=Name_widgets['Stop'][g_ENABLE_CHINESE],
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    icon='uncheck' )

# 默认步频  normal pace
button_normal = widgets.Button(         
    description=Name_widgets['Normal'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',
    icon='check' )

# 慢速步频 slow pace
button_slow = widgets.Button(         
    description=Name_widgets['Slow'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',
    icon='uncheck' )

# 高速步频 high pace
button_high = widgets.Button(        
    description=Name_widgets['High'][g_ENABLE_CHINESE],       
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',
    icon='uncheck' )

def ALL_Uncheck():
    button_normal.icon = 'uncheck'
    button_slow.icon = 'uncheck'
    button_high.icon = 'uncheck'
    g_dog.stop()

# 按键按下事件处理   Key press event processing
def on_button_clicked(b):
    if b.description == Name_widgets['Stop'][g_ENABLE_CHINESE]:
        slider_x.value = 0
        slider_y.value = 0
        slider_z.value = 0
        return
    ALL_Uncheck()
    b.icon = 'check'
    with output:
        print("Button clicked:", b.description)
    if b.description == Name_widgets['Normal'][g_ENABLE_CHINESE]:
        g_dog.pace('normal')
    elif b.description == Name_widgets['Slow'][g_ENABLE_CHINESE]:
        g_dog.pace('slow')
    elif b.description == Name_widgets['High'][g_ENABLE_CHINESE]:
        g_dog.pace('high')
    else:
        return
    if g_last_x != 0:
        g_dog.move('x', g_last_x)
    if g_last_y != 0:
        g_dog.move('y', g_last_y)
    if g_last_z != 0:
        g_dog.turn(g_last_z)

# 滑块滑动事件处理  Slider event handling
def on_slider_slide(x, y, z):
    global g_last_x, g_last_y, g_last_z
    print("   slider:", x, y, z)
    if g_last_x != x:
        g_last_x = x
        g_dog.move('x', x)
        with output:
            print("move x:", x)
    if g_last_y != y:
        g_last_y = y
        g_dog.move('y', y)
        with output:
            print("move y:", y)
    if g_last_z != z:
        g_last_z = z
        step = 0
        if z > 0:
            step = int(z/2+20)
        elif z < 0:
            step = int(z/2-20)
        else:
            step = 0
        g_dog.turn(step)
        with output:
            print("turn z:", z, step)

button_normal.on_click(on_button_clicked)
button_slow.on_click(on_button_clicked)
button_high.on_click(on_button_clicked)
button_stop.on_click(on_button_clicked)

slider_x = widgets.IntSlider(description=Name_widgets['Step_X'][g_ENABLE_CHINESE]+':', value=0 , min=-20,max=20,step=5, orientation='horizontal')
slider_y = widgets.IntSlider(description=Name_widgets['Step_Y'][g_ENABLE_CHINESE]+':', value=0 , min=-18,max=18,step=3, orientation='horizontal')
slider_z = widgets.IntSlider(description=Name_widgets['Speed_Z'][g_ENABLE_CHINESE]+':', value=0 , min=-100,max=100,step=20, orientation='horizontal')

output = widgets.Output()
box_btn = widgets.VBox([button_normal, button_slow, button_high, button_stop])
box_slider = widgets.interactive(on_slider_slide, x=slider_x, y=slider_y, z=slider_z)
box_h = widgets.HBox([box_btn, box_slider])
box_display = widgets.VBox([box_h, output])
display(box_display)


