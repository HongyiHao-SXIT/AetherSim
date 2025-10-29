# 导入库  import library
import cv2
import ipywidgets.widgets as widgets
from IPython.display import display
import time
import threading
import inspect
import ctypes
import numpy as np

# Dogzilla drive library
from DOGZILLALib import DOGZILLA
g_dog = DOGZILLA()

# 中文开关，默认为英文 Chinese switch. The default value is English
g_ENABLE_CHINESE = False

Name_widgets = {
    'Stop': ("Stop", "停止"),
    'Play_Ball': ("Play_Ball", "踢球"),
    'Close_Camera': ("Close_Camera", "关闭摄像头")
}

# 图像数据转化  Image data transformation
def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

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

# 创建摄像头显示组件  Create the camera display component
image_widget = widgets.Image(format='jpeg', width=640, height=480)

# 打开摄像头，数字0需根据/dev/videoX修改为X
# Turn on the camera, you need to change the number 0 to X based on /dev/videoX
image = cv2.VideoCapture(0)
image.set(3, 640)
image.set(4, 480)
image.set(5, 30)
image.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))

# 关闭摄像头 Close_Camera
button_Close_Camera = widgets.Button(  
    value=False,  
    description=Name_widgets['Close_Camera'][g_ENABLE_CHINESE],      
    button_style='danger', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )


# 按键按下事件处理   Key press event processing
def on_button_close_camera(b):
    if b.description == Name_widgets['Close_Camera'][g_ENABLE_CHINESE]:
        # 停止线程，释放摄像头  Stop the thread and release the camera
        b.icon = 'uncheck'
        stop_thread(thread1)
        image.release()
    
# 关联按键事件回调 Button event callbacks
button_Close_Camera.on_click(on_button_close_camera)

motor_id = [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43]
angle_down=[-16, 66, 1, -17, 66, 1, -14, 74, 1, -14, 72, 1]

motor_2 = [21, 22, 23]
angle_hand = [-15, 51, 2, -13, 33, -1, -15, 64, 3, -19, 59, 0]
angle_play_2 = [10, 0, 0]
play_state = 0

# 执行踢球动作  Execute the kick
def play_ball_task():
    global play_state
    if play_state:
        g_dog.motor_speed(100)
        g_dog.motor(motor_id, angle_down)
        time.sleep(.3)
    if play_state:
        g_dog.motor(motor_id, angle_hand)
        time.sleep(.2)
    if play_state:
        g_dog.motor_speed(255)
        time.sleep(.01)
    if play_state:
        g_dog.motor(motor_2, angle_play_2)
        time.sleep(.3)
    if play_state:
        g_dog.motor(motor_id, angle_hand)
        time.sleep(.3)
    if play_state:
        g_dog.motor_speed(100)
        g_dog.motor(motor_id, angle_down)
        time.sleep(.3)
    if play_state:
        g_dog.action(0xff)
        play_state = 0


# 停止 Stop
button_Stop = widgets.Button(        
    description=Name_widgets['Stop'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 踢球 Play ball
button_Play_Ball = widgets.Button(        
    description=Name_widgets['Play_Ball'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 按键按下事件处理   Key press event processing
def on_button_clicked(b):
    global play_state
    with output:
        print("Button clicked:", b.description)
    if b.description == Name_widgets['Stop'][g_ENABLE_CHINESE]:
        play_state = 0
        g_dog.reset()
    elif b.description == Name_widgets['Play_Ball'][g_ENABLE_CHINESE]:
        play_state = 1
        thread1 = threading.Thread(target=play_ball_task)
        thread1.setDaemon(True)
        thread1.start()


# 关联按键事件回调 Button event callbacks
button_Stop.on_click(on_button_clicked)
button_Play_Ball.on_click(on_button_clicked)

# 摄像头显示画面  Camera display screen
def camera_show_task():
    t_start = time.time()
    fps = 0
    while True:
        ret, frame = image.read()
        fps = fps + 1
        mfps = fps / (time.time() - t_start)
        cv2.putText(frame, "FPS " + str(int(mfps)), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 3)
        image_widget.value = bgr8_to_jpeg(frame)
        # time.sleep(.1)


# 机器狗恢复默认姿态  DOGZILLA reverts to default
g_dog.reset()

# 启动摄像头显示任务  Start the camera display task
thread1 = threading.Thread(target=camera_show_task)
thread1.setDaemon(True)
thread1.start()

output = widgets.Output()
box_btn = widgets.VBox([button_Play_Ball, button_Stop, button_Close_Camera])
box_display = widgets.HBox([image_widget, box_btn, output])
display(box_display)
