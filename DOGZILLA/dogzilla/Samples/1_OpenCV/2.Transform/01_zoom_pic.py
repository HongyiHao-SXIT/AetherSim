#!/usr/bin/env python
# coding: utf-8

# <center><img src="../logo.png" alt="Header" style="width: 800px;"/></center>



import cv2
import matplotlib.pyplot as plt  # Python 的 2D绘图库
 
# 读入原图片
img = cv2.imread('yahboom.jpg')
# 打印出图片尺寸
print(img.shape)
# 将图片高和宽分别赋值给x，y
x, y = img.shape[0:2]
 
# 显示原图
#cv.imshow('OriginalPicture', img)
 
# 缩放到原来的二分之一，输出尺寸格式为（宽，高）
img_test1 = cv2.resize(img, (int(y / 2), int(x / 2)))
# cv2.imshow('resize0', img_test1)
# cv2.waitKey()
 
# 最近邻插值法缩放
# 缩放到原来的四分之一
img_test2 = cv2.resize(img, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_NEAREST)
# cv.imshow('resize1', img_test2)
# cv.waitKey()
# cv.destroyAllWindows()
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
dst1 = cv2.cvtColor(img_test1, cv2.COLOR_BGR2RGB)
dst2 = cv2.cvtColor(img_test2, cv2.COLOR_BGR2RGB)

# 显示原始图像
plt.imshow(img)
plt.show()




# 显示缩放1/2
plt.imshow(dst1)
plt.show()




# 显示缩放1/4 邻插值法缩放
plt.imshow(dst2)
plt.show()


# # 以下是matplotlib的一个小例子
# # 参考教程：https://www.runoob.com/numpy/numpy-matplotlib.html 



import numpy as np 
from matplotlib import pyplot as plt 

x = np.arange(1,11) 
y =  2 * x +  5 
plt.title("Matplotlib demo") 
plt.xlabel("x axis caption") 
plt.ylabel("y axis caption") 
plt.plot(x,y) 
plt.show()

