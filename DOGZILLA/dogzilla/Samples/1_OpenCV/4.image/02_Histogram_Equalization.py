
import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread('yahboom.jpg',1)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#cv2.imshow('src',gray)
dst = cv2.equalizeHist(gray)
#cv2.imshow('dst',dst)
#cv2.waitKey(0)


gray = cv2.cvtColor(gray, cv2.COLOR_BGR2RGB)
dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
#plt绘制前后两张图片显示效果
#源图显示
plt.figure(figsize=(14, 9), dpi=100)#设置绘图区域的大小和像素
plt.subplot(121)  # 一行两列第一个
plt.imshow(gray)

#灰度 直方图均衡化
plt.subplot(122)  # 一行两列第二个
plt.imshow(dst)

plt.show()
 


import cv2
import numpy as np
img = cv2.imread('yahboom.jpg',1)
# cv2.imshow('src',img)
(b,g,r) = cv2.split(img)#通道分解
bH = cv2.equalizeHist(b)
gH = cv2.equalizeHist(g)
rH = cv2.equalizeHist(r)
result = cv2.merge((bH,gH,rH))# 通道合成
# cv2.imshow('dst',result)
# cv2.waitKey(0)

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
#plt绘制前后两张图片显示效果
plt.figure(figsize=(14, 9), dpi=100)#设置绘图区域的大小和像素
plt.subplot(121)  # 一行两列第一个
plt.imshow(img)
plt.subplot(122)  # 一行两列第二个
#彩色 直方图均衡化
plt.imshow(dst)
plt.show()

