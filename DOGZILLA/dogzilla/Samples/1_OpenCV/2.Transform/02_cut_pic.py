#!/usr/bin/env python
# coding: utf-8

# <center><img src="../logo.png" alt="Header" style="width: 800px;"/></center>



import cv2
img = cv2.imread('yahboom.jpg', 1)

dst = img[500:700,300:500]  #这里选取矩形区域X：300-500  Y：500-700

#cv2.imshow('image',dst)
#cv2.waitKey(0)


# # 以下会在jupyterLab控件中显示两种压缩后的图像对比显示



#bgr8转jpeg格式
import enum
import cv2

def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])




import ipywidgets.widgets as widgets

image_widget1 = widgets.Image(format='jpg', )
image_widget2 = widgets.Image(format='jpg', )

# display the container in this cell's output
display(image_widget1)
display(image_widget2)

img1 = cv2.imread('yahboom.jpg',1)

image_widget1.value = bgr8_to_jpeg(img1)  #原始图像
image_widget2.value = bgr8_to_jpeg(dst)   #剪切的图像






