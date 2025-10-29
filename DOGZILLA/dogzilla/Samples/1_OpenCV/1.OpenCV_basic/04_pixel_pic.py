#!/usr/bin/env python
# coding: utf-8

# <center><img src="../logo.png" alt="Header" style="width: 800px;"/></center>



import cv2

img = cv2.imread('yahboom.jpg',1)
(b,g,r) = img[100,100]
print(b,g,r)# bgr
#10 100 --- 110 100
i=j=0
for j in range(1,500):
    img[i,j] = (255,255,255)
    for i in range(1,500):
        img[i,j] = (255,255,255)


# # 以下会在jupyter Lab控件中显示前后像素变化对比显示



#bgr8转jpeg格式
import enum
import cv2

def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])




import ipywidgets.widgets as widgets

image_widget1 = widgets.Image(format='jpg', width=300, height=300)
image_widget2 = widgets.Image(format='jpg', width=300, height=300)
# create a horizontal box container to place the image widget next to eachother
image_container = widgets.HBox([image_widget1, image_widget2])

# display the container in this cell's output
display(image_container)

img1 = cv2.imread('yahboom.jpg',1)

image_widget1.value = bgr8_to_jpeg(img1)  #原始的
image_widget2.value = bgr8_to_jpeg(img)   #经过像素操作的

