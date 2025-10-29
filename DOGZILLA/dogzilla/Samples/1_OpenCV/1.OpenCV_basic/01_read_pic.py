#!/usr/bin/env python
# coding: utf-8

# <center><img src="../logo.png" alt="Header" style="width: 800px;"/></center>



import cv2 

img = cv2.imread('yahboom.jpg', 1)
# cv2.imshow('image', img)  #此行只能命令行处py文件执行，会弹出一个视频窗口
# cv2.waitKey (0)


# # 以下会在jupyter Lab控件中显示读取的图像



#bgr8转jpeg格式
import enum
import cv2

def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])




import ipywidgets.widgets as widgets

image_widget = widgets.Image(format='jpg', width=800, height=800)
display(image_widget)

image_widget.value = bgr8_to_jpeg(img)






