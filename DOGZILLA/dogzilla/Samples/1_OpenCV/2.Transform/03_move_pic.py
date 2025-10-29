#!/usr/bin/env python
# coding: utf-8

# <center><img src="../logo.png" alt="Header" style="width: 800px;"/></center>



# 1 API 2 算法原理 3 源代码
import cv2
import numpy as np
img = cv2.imread('yahboom.jpg',1)
#cv2.imshow('src',img)
imgInfo = img.shape
height = imgInfo[0]
width = imgInfo[1]
####
matShift = np.float32([[1,0,200],[0,1,100]])# 2*3
dst = cv2.warpAffine(img,matShift,(height,width))#1 data 2 mat 3 info
# 移位 矩阵
# cv2.imshow('dst',dst)
# cv2.waitKey(0)


# # 以下会在jupyterLab控件中显示原图像和平移后的图像对比显示



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






