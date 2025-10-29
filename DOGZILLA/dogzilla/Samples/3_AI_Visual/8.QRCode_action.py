# 导入库  import library
import cv2
import ipywidgets.widgets as widgets
from IPython.display import display
import time
import threading
import inspect
import ctypes
import numpy as np
import pyzbar.pyzbar as pyzbar

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

# 根据识别到的命令做动作 Act on recognized commands
def control_action(info):
    if info == "LIE DOWN":
        g_dog.action(1) #趴下
        
    elif info == "STAND UP":
        g_dog.action(2)  #站起
        
    elif info == "CRAWL":
        g_dog.action(3)  #匍匐前进
        
    elif info == "TURN AROUND":
        g_dog.action(4) #转圈
        
    elif info == "MARK TIME":
        g_dog.action(5) #原地踏步
        
    elif info == "SQUAT":
        g_dog.action(6) #蹲起
        
    elif info == "TURN ROLL":
        g_dog.action(7) #转动ROLL
        
    elif info == "TURN PITCH":
        g_dog.action(8) #转动PITCH
        
    elif info == "TURN YAW":
        g_dog.action(9) #转动YAW
        
    elif info == "3 AXIS":
        g_dog.action(10) #三轴联动
        
    elif info == "PEE":
        g_dog.action(11) #撒尿
        
    elif info == "SIT DOWN":
        g_dog.action(12) #坐下
        
    elif info == "WAVE(HAND)":
        g_dog.action(13) #招手
        
    elif info == "STRETCH":
        g_dog.action(14) #伸懒腰
        
    elif info == "WAVE(BODY)":
        g_dog.action(15) #波浪
    
    elif info == "SWING":
        g_dog.action(16) #摇摆
    
    elif info == "PRAY":
        g_dog.action(17) #求食
        
    elif info == "SEEK":
        g_dog.action(18) #找食物
        
    elif info == "HANDSHAKE":
        g_dog.action(19) #握手
    

# 解析图像中的二维码信息  Analyze the qrcode information in the image
def decodeDisplay(image, display):
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        # 提取二维码的边界框的位置, 画出图像中条形码的边界框
        # Extract the position of the bounding box of the qrcode, 
        # and draw the bounding box of the barcode in the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(display, (x, y), (x + w, y + h), (225, 225, 225), 2)

        # 提取二维码数据为字节对象，转换成字符串
        # The qrcode data is extracted as byte objects and converted into strings
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # 绘出图像上条形码的数据和条形码类型  
        # Plot the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(display, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (225, 0, 0), 2)

        print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        control_action(barcodeData)
    return display

# 检测二维码  detect qrcode
def Detect_Qrcode_Task():
    ret, frame = image.read()
    image_widget.value = bgr8_to_jpeg(frame)
    t_start = time.time()
    fps = 0
    while True:
        ret, frame = image.read()
        # 转为灰度图像  Convert to grayscale image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = decodeDisplay(gray, frame)
        fps = fps + 1
        mfps = fps / (time.time() - t_start)
        cv2.putText(frame, "FPS " + str(int(mfps)), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 3)
        image_widget.value = bgr8_to_jpeg(frame)


# 启动摄像头显示任务  Start the camera display task
thread1 = threading.Thread(target=Detect_Qrcode_Task)
thread1.daemon=True
thread1.start()

box_display = widgets.HBox([image_widget, button_Close_Camera])
display(box_display)

