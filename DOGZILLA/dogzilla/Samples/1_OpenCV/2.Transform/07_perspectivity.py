#!/usr/bin/env python
# coding: utf-8

# <center><img src="../logo.png" alt="Header" style="width: 800px;"/></center>



import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('yahboom.jpg',1)

imgInfo = img.shape
height = imgInfo[0]
width = imgInfo[1]
#src 4->dst 4 (左上角 左下角 右上角 右下角)
matSrc = np.float32([[200,100],[200,400],[600,100],[width-1,height-1]])
matDst = np.float32([[200,200],[200,300],[500,200],[500,400]])
#组合
matAffine = cv2.getPerspectiveTransform(matSrc,matDst)# mat 1 src 2 dst
dst = cv2.warpPerspective(img,matAffine,(width,height))
img_bgr2rgb = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
plt.imshow(img_bgr2rgb)
plt.show()






