#!/usr/bin/env python
# coding: utf-8

# <center><img src="../logo.png" alt="Header" style="width: 800px;"/></center>



import cv2
import numpy as np
img = cv2.imread('yahboom.jpg',1)
#cv2.imshow('src',img)
imgInfo = img.shape
height = imgInfo[0]
width = imgInfo[1]
# 2*3 
# cv2.getRotationMatrix2D(center, angle, scale)  
# center: 旋转中心点
# angle：旋转角度，正数表示逆时针，负数表示顺时针
# scale：变换尺度
matRotate = cv2.getRotationMatrix2D((height*0.5, width*0.5), 45, 0.5)# mat rotate 1 center 2 angle 3 scale
#100*100 25 
dst = cv2.warpAffine(img, matRotate, (height,width))
#cv2.imshow('dst',dst)
#cv2.waitKey(0)


# # 以下会在jupyterLab控件中显示原图像和旋转后的图像对比显示



#bgr8转jpeg格式
import enum
import cv2

def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])




import ipywidgets.widgets as widgets

image_widget1 = widgets.Image(format='jpg', )
image_widget2 = widgets.Image(format='jpg', )
# create a horizontal box container to place the image widget next to eachother
image_container = widgets.HBox([image_widget1, image_widget2])

# display the container in this cell's output
display(image_container)
#display(image_widget2)

img1 = cv2.imread('yahboom.jpg',1)

image_widget1.value = bgr8_to_jpeg(img1)
image_widget2.value = bgr8_to_jpeg(dst)






