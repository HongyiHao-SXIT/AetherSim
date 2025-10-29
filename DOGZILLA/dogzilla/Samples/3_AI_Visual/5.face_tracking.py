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

# 摄像头显示控件  Camera display widgets
image_widget = widgets.Image(format='jpeg',width=640, height=480)


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

# 导入人脸Haar特征分类器  Import face Haar feature classifier
face_haar = cv2.CascadeClassifier("haarcascade_profileface.xml")

# 人脸追踪任务 Face Tracking Task
def Face_Tracking_Task():
    value_x = 0
    value_y = 0
    while True:
        ret, frame = image.read()
        # 把图像转为灰度图像  Convert the image to grayscale
        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_haar.detectMultiScale(gray_img, 1.1, 3)

        if len(faces) > 0:
            (face_x, face_y, face_w, face_h) = faces[0]
            cv2.rectangle(frame,(face_x,face_y),(face_x+face_w,face_y+face_h),(0,255,0),2)
            value_x = face_x - 320
            value_y = face_y - 240
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
            value_x = 0
            value_y = 0
        cv2.putText(frame, "X:%d, Y%d" % (int(value_x), int(value_y)), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 3)
        image_widget.value = bgr8_to_jpeg(frame)


# 机器狗恢复默认姿态  DOGZILLA reverts to default
g_dog.reset()

# 启动摄像头显示任务  Start the camera display task
thread1 = threading.Thread(target=Face_Tracking_Task)
thread1.daemon=True
thread1.start()

box_display = widgets.HBox([image_widget, button_Close_Camera])
display(box_display)

