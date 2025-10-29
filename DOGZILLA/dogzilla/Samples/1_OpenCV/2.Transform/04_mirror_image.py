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
deep = imgInfo[2]
newImgInfo = (height*2,width,deep)
dst = np.zeros(newImgInfo,np.uint8)#uint8 
for i in range(0,height):
    for j in range(0,width):
        dst[i,j] = img[i,j]
        #x y = 2*h - y -1
        dst[height*2-i-1,j] = img[i,j]
for i in range(0,width):
    dst[height,i] = (0,0,255)#BGR
#cv2.imshow('dst',dst)
#cv2.waitKey(0)


# # 以下会在jupyterLab控件中显示原图像和镜像后的图像对比显示



#bgr8转jpeg格式
import enum
import cv2

def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])




import ipywidgets.widgets as widgets

image_widget1 = widgets.Image(format='jpg', )
# image_widget2 = widgets.Image(format='jpg', )
# create a horizontal box container to place the image widget next to eachother
# image_container = widgets.HBox([image_widget1, image_widget2])

# display the container in this cell's output
display(image_widget1)
#display(image_widget2)

image_widget1.value = bgr8_to_jpeg(dst)






