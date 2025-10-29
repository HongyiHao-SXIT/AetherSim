
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('yahboom.jpg',1)
imgInfo = img.shape
height = imgInfo[0]
width = imgInfo[1]
#cv2.imshow('src',img)
dst = np.zeros((height, width, 3),np.uint8)
for i in range(0, height):
    for j in range(0, width):
        (b,g,r) = img[i,j]
        bb = int(b) + 40
        gg = int(g) + 40
        rr = int(r) + 40
        if bb>255:
            bb = 255
        if gg>255:
            gg = 255
        if rr>255:
            rr = 255
        dst[i,j] = (bb,gg,rr)
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

