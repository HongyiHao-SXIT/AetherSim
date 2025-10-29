#!/usr/bin/env python
# coding: utf-8



# 导入库  import library
import cv2
import ipywidgets.widgets as widgets
from IPython.display import display
import time
import threading
import inspect
import ctypes




# Dogzilla drive library
from DOGZILLALib import DOGZILLA
g_dog = DOGZILLA()


# # 网页上位机综合控制机器狗
# # Web host computer integrated control DOGZILLA



# 中文开关，默认为英文 Chinese switch. The default value is English
g_ENABLE_CHINESE = False

Name_widgets = {
    'Stop': ("Stop", "停止"),
    'Forward': ("Forward", "前进"),
    'Backward': ("Backward", "后退"),
    'Left': ("Left", "左平移"),
    'Right': ("Right", "右平移"),
    'TurnLeft': ("TurnLeft", "向左转"),
    'TurnRight': ("TurnRight", "向右转"),
    'Normal': ("Normal", "默认步频"),
    'Slow': ("Slow", "慢速步频"),
    'High': ("High", "高速步频"),
    "Step":("Step", "步伐宽度"),
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
    'Play_Ball':("Play_Ball", "踢球"),
    'Rotation': ("Rotation", "动作轮播"),
    'Reset': ("Reset", "恢复初始姿态"),
    'Translation_X': ("Translation_X", "前后平移"),
    'Translation_Y': ("Translation_Y", "左右平移"),
    'Translation_Z': ("Translation_Z", "身高调节"),
    'Attitude_roll': ("Attitude_roll", "滚转角"),
    'Attitude_pitch': ("Attitude_pitch", "俯仰角"),
    'Attitude_yaw': ("Attitude_yaw", "偏航角"),
    'Close_Camera': ("Close_Camera", "关闭摄像头")
}




# 图像数据转化  Image data transformation
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])




# 创建摄像头显示组件  Create the camera display component
image_widget = widgets.Image(format='jpeg', width=640, height=480)  

# 打开摄像头，数字0需根据/dev/videoX修改为X
# Turn on the camera, you need to change the number 0 to X based on /dev/videoX
image = cv2.VideoCapture(0)
image.set(3, 640)
image.set(4, 480)
image.set(5, 30)
image.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))




# 关闭线程  stop thread
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)




# 摄像头显示画面  Camera display screen
def Display_Camera():
    global g_height, g_width, g_roll, g_pitch, g_yaw
    t_start = time.time()
    fps = 0
    while(True):
        ret, frame = image.read()
        fps = fps + 1
        mfps = fps / (time.time() - t_start)
        try:
            cv2.putText(frame, "FPS " + str(int(mfps)), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 3)
            image_widget.value = bgr8_to_jpeg(frame)
        except:
            pass




# 清除按键显示状态  Clear button display status
def ALL_Uncheck():
    button_stop.icon = 'uncheck'
    button_forward.icon = 'uncheck'
    button_backward.icon = 'uncheck'
    button_move_left.icon = 'uncheck'
    button_move_right.icon = 'uncheck'
    button_turn_left.icon = 'uncheck'
    button_turn_right.icon = 'uncheck'
    

# 按键按下事件处理   Key press event processing
def on_button_clicked_control(b):
    ALL_Uncheck()
    b.icon = 'check'
    with output:
        print("Button clicked:", b.description)
    if b.description == Name_widgets['Stop'][g_ENABLE_CHINESE]:
        g_dog.stop()
        b.icon = 'uncheck'
    elif b.description == Name_widgets['Forward'][g_ENABLE_CHINESE]:
        g_dog.stop()
        g_dog.forward(int(g_step_width*0.20))
    elif b.description == Name_widgets['Backward'][g_ENABLE_CHINESE]:
        g_dog.stop()
        g_dog.back(int(g_step_width*0.20))
    elif b.description == Name_widgets['Left'][g_ENABLE_CHINESE]:
        g_dog.stop()
        g_dog.left(int(g_step_width*0.18))
    elif b.description == Name_widgets['Right'][g_ENABLE_CHINESE]:
        g_dog.stop()
        g_dog.right(int(g_step_width*0.18))
    elif b.description == Name_widgets['TurnLeft'][g_ENABLE_CHINESE]:
        g_dog.stop()
        g_dog.turnleft(int(g_step_width/2+20))
    elif b.description == Name_widgets['TurnRight'][g_ENABLE_CHINESE]:
        g_dog.stop()
        g_dog.turnright(int(g_step_width/2+20))
    elif b.description == Name_widgets['Normal'][g_ENABLE_CHINESE]:
        g_dog.stop()
        g_dog.pace('normal')
        button_normal.icon = 'check'
        button_slow.icon = 'uncheck'
        button_high.icon = 'uncheck'
    elif b.description == Name_widgets['Slow'][g_ENABLE_CHINESE]:
        g_dog.stop()
        g_dog.pace('slow')
        button_normal.icon = 'uncheck'
        button_slow.icon = 'check'
        button_high.icon = 'uncheck'
    elif b.description == Name_widgets['High'][g_ENABLE_CHINESE]:
        g_dog.stop()
        g_dog.pace('high')
        button_normal.icon = 'uncheck'
        button_slow.icon = 'uncheck'
        button_high.icon = 'check'
    elif b.description == Name_widgets['Close_Camera'][g_ENABLE_CHINESE]:
        # 停止线程，释放摄像头  Stop the thread and release the camera
        b.icon = 'uncheck'
        stop_thread(thread1)
        image.release()
    else:
        return




play_ball_state = 0

# 踢球动作 play_ball_task
def play_ball_task(leg_id):
    global play_ball_state
    motor_id = [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43]
    angle_down=[-16, 66, 1, -17, 66, 1, -14, 74, 1, -14, 72, 1]

    if leg_id == 2:
        motor_2 = [21, 22, 23]
        angle_hand = [-15, 51, 2, -13, 33, -1, -15, 64, 3, -19, 59, 0]
        angle_play_2 = [10, 0, 0]
        if play_ball_state:
            g_dog.motor_speed(100)
            g_dog.motor(motor_id, angle_down)
            time.sleep(.3)
        if play_ball_state:
            g_dog.motor(motor_id, angle_hand)
            time.sleep(.2)
        if play_ball_state:
            g_dog.motor_speed(255)
            time.sleep(.01)
        if play_ball_state:
            g_dog.motor(motor_2, angle_play_2)
            time.sleep(.3)
        if play_ball_state:
            g_dog.motor(motor_id, angle_hand)
            time.sleep(.3)
        if play_ball_state:
            g_dog.motor_speed(100)
            g_dog.motor(motor_id, angle_down)
            time.sleep(.3)
        if play_ball_state:
            g_dog.action(0xff)
    play_ball_state = 0




# 恢复默认状态  Restore default status
def reset_dogzilla():
    global play_ball_state
    g_dog.action(0xff)
    if button_Rotation.icon == 'check':
            button_Rotation.icon = 'uncheck'
            g_dog.perform(0)
    button_stop.icon = 'uncheck'
    button_forward.icon = 'uncheck'
    button_backward.icon = 'uncheck'
    button_move_left.icon = 'uncheck'
    button_move_right.icon = 'uncheck'
    button_turn_left.icon = 'uncheck'
    button_turn_right.icon = 'uncheck'
    
    button_normal.icon = 'check'
    button_slow.icon = 'uncheck'
    button_high.icon = 'uncheck'

    slider_x.value = 0
    slider_y.value = 0
    slider_z.value = 105
    slider_roll.value = 0
    slider_pitch.value = 0
    slider_yaw.value = 0
    play_ball_state = 0




# 按键按下事件处理   Key press event processing
def on_button_clicked(b):
    with output:
        print("Button clicked:", b.description)
    if b.description == Name_widgets['Reset'][g_ENABLE_CHINESE]:
        reset_dogzilla()
        
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
    elif b.description == Name_widgets['Play_Ball'][g_ENABLE_CHINESE]:
        global play_ball_state
        if play_ball_state == 0:
            play_ball_state = 2
            task_1 = threading.Thread(target=play_ball_task, args=(play_ball_state,), name="play_ball_task")
            task_1.setDaemon(True)
            task_1.start()





# 保存滑块的上一个值，主要用于定位哪个滑竿数值改变。
# Saves the last value of the slider, mainly to locate which slider value has changed
g_translation_x = 0
g_translation_y = 0
g_translation_z = 0

g_attitude_roll = 0
g_attitude_pitch = 0
g_attitude_yaw = 0

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

# 滑块滑动事件处理  Slider event handling
def on_slider_step(step):
    global g_step_width
    print("   slider:", step)
    g_step_width = int(step)




# 停止 STOP
button_stop = widgets.Button(       
    description=Name_widgets['Stop'][g_ENABLE_CHINESE],
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
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

# 关闭摄像头  Close_Camera
button_Close_Camera = widgets.Button(      
    description=Name_widgets['Close_Camera'][g_ENABLE_CHINESE],      
    button_style='danger', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )




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

button_action_20 = widgets.Button(       
    description=Name_widgets['Play_Ball'][g_ENABLE_CHINESE],        
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




# 关联按键事件回调 Button event callbacks
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
button_action_20.on_click(on_button_clicked)
button_Rotation.on_click(on_button_clicked)
button_Reset.on_click(on_button_clicked)

button_stop.on_click(on_button_clicked_control)
button_forward.on_click(on_button_clicked_control)
button_backward.on_click(on_button_clicked_control)
button_move_left.on_click(on_button_clicked_control)
button_move_right.on_click(on_button_clicked_control)
button_turn_left.on_click(on_button_clicked_control)
button_turn_right.on_click(on_button_clicked_control)
button_normal.on_click(on_button_clicked_control)
button_slow.on_click(on_button_clicked_control)
button_high.on_click(on_button_clicked_control)
button_Close_Camera.on_click(on_button_clicked_control)




# 创建滑块控制身体姿态，slider_roll控制翻转角，slider_pitch控制俯仰角，slider_yaw控制偏航角。
# Create sliders to control body posture, slider_roll to control roll, slider_pitch to control pitch, and slider_yaw to control yaw.
slider_roll = widgets.IntSlider(description=Name_widgets['Attitude_roll'][g_ENABLE_CHINESE]+':', value=0 , min=-20,max=20,step=1, orientation='horizontal')
slider_pitch = widgets.IntSlider(description=Name_widgets['Attitude_pitch'][g_ENABLE_CHINESE]+':', value=0 , min=-15,max=15,step=1, orientation='horizontal')
slider_yaw = widgets.IntSlider(description=Name_widgets['Attitude_yaw'][g_ENABLE_CHINESE]+':', value=0 , min=-11,max=11,step=1, orientation='horizontal')

# 创建滑块控制身体平移，slider_x控制前后，slider_y控制左右，slider_z控制身高。
# Create sliders for body translation, slider_x for front and back, slider_y for left and right, and slider_z for height
slider_x = widgets.IntSlider(description=Name_widgets['Translation_X'][g_ENABLE_CHINESE]+':', value=0 , min=-35,max=35,step=1, orientation='horizontal')
slider_y = widgets.IntSlider(description=Name_widgets['Translation_Y'][g_ENABLE_CHINESE]+':', value=0 , min=-18,max=18,step=1, orientation='horizontal')
slider_z = widgets.IntSlider(description=Name_widgets['Translation_Z'][g_ENABLE_CHINESE]+':', value=105 , min=75,max=110,step=1, orientation='horizontal')

# 创建滑块控制步伐宽度  Create slider to control step width
slider_step = widgets.IntSlider(description=Name_widgets['Step'][g_ENABLE_CHINESE]+':', value=50 , min=20,max=100,step=10, orientation='horizontal')


# ## 布局控件并显示  Layout widgets and display them



thread1 = threading.Thread(target=Display_Camera)
thread1.setDaemon(True)
thread1.start()

output = widgets.Output()
box_btn_1 = widgets.HBox([button_action_1, button_action_2, button_action_3, button_action_4])
box_btn_2 = widgets.HBox([button_action_5, button_action_6, button_action_7, button_action_8])
box_btn_3 = widgets.HBox([button_action_9, button_action_10, button_action_11, button_action_12])
box_btn_4 = widgets.HBox([button_action_13, button_action_14, button_action_15, button_action_16])
box_btn_5 = widgets.HBox([button_action_17, button_action_18, button_action_19, button_action_20])
box_btn_6 = widgets.HBox([button_normal, button_slow, button_high])
box_btn_7 = widgets.HBox([button_forward, button_backward, button_stop])
box_btn_8 = widgets.HBox([button_move_left, button_move_right, button_turn_left, button_turn_right])
box_btn_9 = widgets.HBox([button_Reset, button_Close_Camera])
box_control = box_btn = widgets.VBox([box_btn_6, box_btn_7, box_btn_8])
box_action = widgets.VBox([box_btn_1, box_btn_2, box_btn_3, box_btn_4, box_btn_5, box_btn_9])

box_slider1 = widgets.interactive(on_slider_translation, x=slider_x, y=slider_y, z=slider_z)
box_slider2 = widgets.interactive(on_slider_attitude, roll=slider_roll, pitch=slider_pitch, yaw=slider_yaw)
box_slider3 = widgets.interactive(on_slider_step, step=slider_step)
box_slider = widgets.HBox([box_slider1, box_slider2])

box_v = widgets.VBox([box_slider3, box_control, box_slider, box_action], layout=widgets.Layout(align_self='center'))
box_h = widgets.HBox([image_widget, box_v], layout=widgets.Layout(align_self='center'))
box_display = widgets.VBox([box_h, output])
display(box_display)






