import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('yahboom.jpg',1)
# cv2.imshow('src',img)
dst = cv2.GaussianBlur(img,(5,5),1.5)
# cv2.imshow('dst',dst)
# cv2.waitKey(0)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(14, 6), dpi=100) #设置绘图区域的大小和像素
plt.subplot(121)  # 一行二列第一个
plt.imshow(img)
plt.subplot(122)  # 一行二列第二个
plt.imshow(dst)
plt.show()

