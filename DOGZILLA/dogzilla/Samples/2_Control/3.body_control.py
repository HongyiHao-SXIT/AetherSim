import ipywidgets.widgets as widgets
from IPython.display import display

# Dogzilla drive library
from DOGZILLALib import DOGZILLA
g_dog = DOGZILLA()

# 调节位姿时，机器狗四条腿足端位置不发生改变，机身的位置或角度发生变化。
# When adjusting the posture, the position of the four legs of the robot dog does not change, and the position or Angle of the body changes.

# 中文开关，默认为英文 Chinese switch. The default value is English
g_ENABLE_CHINESE = False

Name_widgets = {
    'Reset': ("Reset", "恢复默认"),
    'Translation_X': ("Translation_X", "前后平移"),
    'Translation_Y': ("Translation_Y", "左右平移"),
    'Translation_Z': ("Translation_Z", "身高调节"),
    'Attitude_roll': ("Attitude_roll", "滚转角"),
    'Attitude_pitch': ("Attitude_pitch", "俯仰角"),
    'Attitude_yaw': ("Attitude_yaw", "偏航角")
}

# 保存滑块的上一个值，主要用于定位哪个滑竿数值改变。
# Saves the last value of the slider, mainly to locate which slider value has changed
g_translation_x = 0
g_translation_y = 0
g_translation_z = 0

g_attitude_roll = 0
g_attitude_pitch = 0
g_attitude_yaw = 0

# 恢复默认 Reset
button_reset = widgets.Button(      
    description=Name_widgets['Reset'][g_ENABLE_CHINESE],
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    icon='uncheck' )

# 按键按下事件处理   Key press event processing
def on_button_clicked(b):
    with output:
        print("Button clicked:", b.description)
    if b.description == Name_widgets['Reset'][g_ENABLE_CHINESE]:
        slider_x.value = 0
        slider_y.value = 0
        slider_z.value = 105
        slider_roll.value = 0
        slider_pitch.value = 0
        slider_yaw.value = 0
        
# 关联按键事件回调 Button event callbacks
button_reset.on_click(on_button_clicked)

# 滑块滑动事件处理  Slider event handling
def on_slider_translation(x, y, z):
    global g_translation_x, g_translation_y, g_translation_z
    print("   slider:", x, y, z)
    if g_translation_x != x:
        g_translation_x = x
        g_dog.translation('x', x)
        with output:
            print("Translation x:", x)
    if g_translation_y != y:
        g_translation_y = y
        g_dog.translation('y', y)
        with output:
            print("Translation y:", y)
    if g_translation_z != z:
        g_translation_z = z
        g_dog.translation('z', z)
        with output:
            print("Translation z:", z)

# 创建滑块控制身体平移，slider_x控制前后，slider_y控制左右，slider_z控制身高。
# Create sliders for body translation, slider_x for front and back, slider_y for left and right, and slider_z for height
slider_x = widgets.IntSlider(description=Name_widgets['Translation_X'][g_ENABLE_CHINESE]+':', value=0 , min=-35,max=35,step=1, orientation='horizontal')
slider_y = widgets.IntSlider(description=Name_widgets['Translation_Y'][g_ENABLE_CHINESE]+':', value=0 , min=-18,max=18,step=1, orientation='horizontal')
slider_z = widgets.IntSlider(description=Name_widgets['Translation_Z'][g_ENABLE_CHINESE]+':', value=105 , min=75,max=110,step=1, orientation='horizontal')

# 滑块滑动事件处理  Slider event handling
def on_slider_attitude(roll, pitch, yaw):
    global g_attitude_roll, g_attitude_pitch, g_attitude_yaw
    print("   slider:", roll, pitch, yaw)
    if g_attitude_roll != roll:
        g_attitude_roll = roll
        g_dog.attitude('r', roll)
        with output:
            print("Attitude roll:", roll)
    if g_attitude_pitch != pitch:
        g_attitude_pitch = pitch
        g_dog.attitude('p', pitch)
        with output:
            print("Attitude pitch:", pitch)
    if g_attitude_yaw != yaw:
        g_attitude_yaw = yaw
        g_dog.attitude('y', yaw)
        with output:
            print("Attitude yaw:", yaw)

# 创建滑块控制身体姿态，slider_roll控制翻转角，slider_pitch控制俯仰角，slider_yaw控制偏航角。
# Create sliders to control body posture, slider_roll to control roll, slider_pitch to control pitch, and slider_yaw to control yaw.
slider_roll = widgets.IntSlider(description=Name_widgets['Attitude_roll'][g_ENABLE_CHINESE]+':', value=0 , min=-20,max=20,step=1, orientation='horizontal')
slider_pitch = widgets.IntSlider(description=Name_widgets['Attitude_pitch'][g_ENABLE_CHINESE]+':', value=0 , min=-15,max=15,step=1, orientation='horizontal')
slider_yaw = widgets.IntSlider(description=Name_widgets['Attitude_yaw'][g_ENABLE_CHINESE]+':', value=0 , min=-11,max=11,step=1, orientation='horizontal')

# 布局控件并显示  Layout widgets and display them
output = widgets.Output()
box_slider1 = widgets.interactive(on_slider_translation, x=slider_x, y=slider_y, z=slider_z)
box_slider2 = widgets.interactive(on_slider_attitude, roll=slider_roll, pitch=slider_pitch, yaw=slider_yaw)
box_h = widgets.HBox([box_slider1, box_slider2, button_reset])
box_display = widgets.VBox([box_h, output])
display(box_display)