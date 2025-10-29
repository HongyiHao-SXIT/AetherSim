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
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
origin_widget = widgets.Image(format='jpeg', width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
mask_widget = widgets.Image(format='jpeg',width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
result_widget = widgets.Image(format='jpeg',width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)


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

# 默认选择红色的，想识别其他请注释下面红色区间代码，放开后面其他区间代码段
# The default is red. If you want to identify others, please comment the following red interval code, and let go of other interval code segments
# 红色区间  Red range
color_lower = np.array([0, 43, 46])
color_upper = np.array([10, 255, 255])

# #绿色区间 Green range
# color_lower = np.array([35, 43, 46])
# color_upper = np.array([77, 255, 255])

# #蓝色区间 Blue range
# color_lower=np.array([100, 43, 46])
# color_upper = np.array([124, 255, 255])

# #黄色区间 Yello range
# color_lower = np.array([26, 43, 46])
# color_upper = np.array([34, 255, 255])


# 颜色识别功能任务  Color recognition task
def Color_Recongnize_Task():
    while(True):
        ret, frame = image.read()
        origin_widget.value = bgr8_to_jpeg(frame)

        # 改为HSV模型 change to hsv model
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # get mask 利用inRange()函数和HSV模型中所选颜色范围的上下界获取mask，
        # mask中原视频中的所选颜色部分会被弄成白色，其他部分黑色。
        # Get Mask uses the inRange() function and the upper and lower bounds of the selected color range in the HSV model to obtain the mask. 
        # The selected color part of the mask in the original video will be made white, and the other parts will be black.
        mask = cv2.inRange(hsv, color_lower, color_upper)
        mask_widget.value = bgr8_to_jpeg(mask)

        # detect blue 将mask于原视频帧进行按位与操作，
        # 则会把mask中的白色用真实的图像替换
        # Detect Blue will bitwise and operate the mask in the original video frame, 
        # then replace the white in the mask with the real image
        res = cv2.bitwise_and(frame, frame, mask=mask)
        result_widget.value = bgr8_to_jpeg(res)


# 启动摄像头显示任务  Start the camera display task
thread1 = threading.Thread(target=Color_Recongnize_Task)
thread1.daemon=True
thread1.start()

# 创建一个横向的盒子容器，以便将图像小部件相邻放置
# create a horizontal box container to place the image widget next to eachother
image_container_mask = widgets.HBox([origin_widget, mask_widget])
image_container_result = widgets.HBox([origin_widget, result_widget])
box_display = widgets.VBox([image_container_mask, image_container_result, button_Close_Camera])
display(box_display)

