#!/usr/bin/env python
# coding: utf-8

# <center><img src="../logo.png" alt="Header" style="width: 800px;"/></center>
# 



import cv2

# 1 文件的读取 2 封装格式解析 3 数据解码 4 数据加载
img = cv2.imread('yahboom.jpg', 1)
# cv2.imshow('image', img)  #这段需要在树莓派图形化界面命令行执行，会显示一个图像的窗口
cv2.imwrite('yahboom1.jpg', img) # 1 name 2 data 


# # 以下会在jupyter Lab控件中显示写入后读取的图像



#bgr8转jpeg格式
import enum
import cv2

def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])




import ipywidgets.widgets as widgets

image_widget = widgets.Image(format='jpg', width=320, height=240)
display(image_widget)
img = cv2.imread('yahboom1.jpg',1)
image_widget.value = bgr8_to_jpeg(img)






