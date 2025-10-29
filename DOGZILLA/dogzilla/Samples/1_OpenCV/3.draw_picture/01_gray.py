#方法1 
#注意：有时第一次运行图片不会显示出来，第二次才会显示出来
#方法1 imread 

import cv2
import matplotlib.pyplot as plt

img0 = cv2.imread('yahboom.jpg',0)  
img1 = cv2.imread('yahboom.jpg',1)
# print(img0.shape)
# print(img1.shape)
# cv2.imshow('src',img0)
# cv2.waitKey(0)

#原始图像
# img_bgr2rgb1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
# plt.imshow(img_bgr2rgb1)

#灰色图像
img_bgr2rgb0 = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB)
plt.imshow(img_bgr2rgb0)
plt.show()

#方法2 cvtColor
#注意：有时第一次运行图片不会显示出来，第二次才会显示出来
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('yahboom.jpg',1)
dst = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)# 颜色空间转换 1 data 2 BGR gray
#cv2.imshow('dst',dst)
#cv2.waitKey(0)

#原始图像
# img_bgr2rgb1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# plt.imshow(img_bgr2rgb1)

#灰色图像
img_bgr2rgb0 = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
plt.imshow(img_bgr2rgb0)
plt.show()


#方法3 平均值法
import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread('yahboom.jpg',1)
imgInfo = img.shape
height = imgInfo[0]
width = imgInfo[1]
# RGB R=G=B = gray  (R+G+B)/3
dst = np.zeros((height,width,3),np.uint8)
for i in range(0,height):
    for j in range(0,width):
        (b,g,r) = img[i,j]
        gray = (int(b)+int(g)+int(r))/3
        dst[i,j] = np.uint8(gray)
#cv2.imshow('dst',dst)
#cv2.waitKey(0)

#原始图像
# img_bgr2rgb1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# plt.imshow(img_bgr2rgb1)

#灰色图像
img_bgr2rgb0 = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
plt.imshow(img_bgr2rgb0)
plt.show()

#方法4 加权平均值方法
# gray = r*0.299+g*0.587+b*0.114  

import cv2
import numpy as np
img = cv2.imread('yahboom.jpg',1)
imgInfo = img.shape
height = imgInfo[0]
width = imgInfo[1]
dst = np.zeros((height,width,3),np.uint8)
for i in range(0,height):
    for j in range(0,width):
        (b,g,r) = img[i,j]
        b = int(b)
        g = int(g)
        r = int(r)
        gray = r*0.299+g*0.587+b*0.114
        dst[i,j] = np.uint8(gray)
#cv2.imshow('dst',dst)
#cv2.waitKey(0)

#原始图像
# img_bgr2rgb1 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# plt.imshow(img_bgr2rgb1)

#灰色图像
img_bgr2rgb0 = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
plt.imshow(img_bgr2rgb0)
plt.show()

