import cv2 
import numpy as np

img = cv2.imread('yahboom.jpg',1)
font = cv2.FONT_HERSHEY_SIMPLEX

cv2.rectangle(img,(200,100),(500,400),(0,255,0),3)
# 1 dst 2 文字内容 3 坐标 4 5 字体大小 6 color 7 粗细 8 line type
cv2.putText(img,'Yahboom',(250,50),font,1,(200,200,0),2,cv2.LINE_AA)
# cv2.imshow('src',img)
# cv2.waitKey(0)

import matplotlib.pyplot as plt

dst = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(dst)
plt.show()

import cv2 
img = cv2.imread('yahboom.jpg',1)
height = int(img.shape[0]*0.2)
width = int(img.shape[1]*0.2)
imgResize = cv2.resize(img,(width,height))
for i in range(0,height):
    for j in range(0,width):
        img[i+200,j+350] = imgResize[i,j]
# cv2.imshow('src',img)
# cv2.waitKey(0)

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img)
plt.show()



