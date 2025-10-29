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
    'Close': ("Close", "关闭"),
    'Red': ("Red", "红色"),
    'Green': ("Green", "绿色"),
    'Blue': ("Blue", "蓝色"),
    'Yellow': ("Yellow", "黄色"),
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

# 创建存储HSV色域颜色分类数据的数组  Creates an array that stores the HSV gamut color classification data
color_lower = np.array([156, 43, 46])
color_upper = np.array([180, 255, 255])
g_mode = 0

# 颜色选择按钮配置  Color selection button configuration
# 关闭 Close
Closebutton = widgets.Button(         
    description=Name_widgets['Close'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 红色 Red
Redbutton = widgets.Button(       
    description=Name_widgets['Red'][g_ENABLE_CHINESE],
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    icon='uncheck' )

# 绿色 Green
Greenbutton = widgets.Button(     
    description=Name_widgets['Green'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 蓝色 Blue
Bluebutton = widgets.Button(        
    description=Name_widgets['Blue'][g_ENABLE_CHINESE],         
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 黄色 Yellow
Yellowbutton = widgets.Button(        
    description=Name_widgets['Yellow'][g_ENABLE_CHINESE],        
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''     
    tooltip='Description',     
    icon='uncheck' )

# 清除按键显示状态  Clear button display status
def ALL_Uncheck():
    Redbutton.icon = 'uncheck'
    Greenbutton.icon = 'uncheck'
    Bluebutton.icon = 'uncheck'
    Yellowbutton.icon = 'uncheck'

# 按键按下事件处理   Key press event processing
def on_button_clicked(b):
    global color_lower, color_upper, g_mode
    global g_action
    ALL_Uncheck()
    b.icon = 'check'
    with output:
        print("Button clicked:", b.description)
    if b.description == Name_widgets['Close'][g_ENABLE_CHINESE]:
        g_dog.action(0xff)
        g_mode = 0
        b.icon = 'uncheck'
    elif b.description == Name_widgets['Red'][g_ENABLE_CHINESE]:
        color_lower = np.array([0, 43, 46])
        color_upper = np.array([10, 255, 255])
        g_dog.action(0xff)
        g_mode = 1
    elif b.description == Name_widgets['Green'][g_ENABLE_CHINESE]:
        color_lower = np.array([35, 43, 46])
        color_upper = np.array([77, 255, 255])
        g_dog.action(0xff)
        g_mode = 1
    elif b.description == Name_widgets['Blue'][g_ENABLE_CHINESE]:
        color_lower=np.array([100, 43, 46])
        color_upper = np.array([124, 255, 255])
        g_dog.action(0xff)
        g_mode = 1
    elif b.description == Name_widgets['Yellow'][g_ENABLE_CHINESE]:
        color_lower = np.array([26, 43, 46])
        color_upper = np.array([34, 255, 255])
        g_dog.action(0xff)
        g_mode = 1


# 关联按键事件回调 Button event callbacks
Redbutton.on_click(on_button_clicked)
Greenbutton.on_click(on_button_clicked)
Bluebutton.on_click(on_button_clicked)
Yellowbutton.on_click(on_button_clicked)
Closebutton.on_click(on_button_clicked)

# 颜色追踪任务  Color tracking task
def Color_Tracking_Task():
    global color_lower, color_upper, g_mode
    t_start = time.time()
    fps = 0
    color_x = 0
    color_y = 0
    color_radius = 0
    while True:
        ret, frame = image.read()
        frame_ = cv2.GaussianBlur(frame,(5,5),0)                    
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv,color_lower,color_upper)  
        mask = cv2.erode(mask,None,iterations=2)
        mask = cv2.dilate(mask,None,iterations=2)
        mask = cv2.GaussianBlur(mask,(3,3),0)     
        cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2] 
        if g_mode == 1: # 按钮切换开关  button switch
            if len(cnts) > 0:
                cnt = max (cnts, key = cv2.contourArea)
                (color_x,color_y),color_radius = cv2.minEnclosingCircle(cnt)
                if color_radius > 10:
                    # 将检测到的颜色标记出来  Mark the detected color
                    cv2.circle(frame,(int(color_x),int(color_y)),int(color_radius),(255,0,255),2)  
                    value_x = color_x - 320
                    value_y = color_y - 240
                    if value_x > 110:
                        value_x = 110
                    elif value_x < -110:
                        value_x = -110
                    if value_y > 150:
                        value_y = 150
                    elif value_y < -150:
                        value_y = -150
                    g_dog.attitude(['y','p'],[-value_x/10, value_y/10])
            else:
                color_x = 0
                color_y = 0
            cv2.putText(frame, "X:%d, Y%d" % (int(color_x), int(color_y)), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 3)
            t_start = time.time()
            fps = 0
        else:
            fps = fps + 1
            mfps = fps / (time.time() - t_start)
            cv2.putText(frame, "FPS " + str(int(mfps)), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 3)
        # 实时传回图像数据进行显示
        image_widget.value = bgr8_to_jpeg(frame)



# 机器狗恢复默认姿态  DOGZILLA reverts to default
g_dog.reset()

# 启动摄像头显示任务  Start the camera display task
thread1 = threading.Thread(target=Color_Tracking_Task)
thread1.setDaemon(True)
thread1.start()

output = widgets.Output()
box_btn = widgets.VBox([Redbutton, Greenbutton, Bluebutton, Yellowbutton, Closebutton, button_Close_Camera])
box_display = widgets.HBox([image_widget, box_btn, output])
display(box_display)

