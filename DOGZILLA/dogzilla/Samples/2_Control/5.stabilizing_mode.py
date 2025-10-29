import ipywidgets.widgets as widgets
from IPython.display import display
from DOGZILLALib import DOGZILLA
g_dog = DOGZILLA()

g_ENABLE_CHINESE = False

Name_widgets = {
    'Stabilizing_mode': ("Stabilizing_mode", "自稳模式"),
    'ON':("ON", "已开启"),
    'OFF':("OFF", "已关闭"),
}

button_Stable = widgets.Button(  
    value=False,  
    description=Name_widgets['Stabilizing_mode'][g_ENABLE_CHINESE],      
    button_style='success', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

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

button_Stable.on_click(on_button_clicked)

output = widgets.Output()
box_display = widgets.VBox([button_Stable, output])
display(box_display)