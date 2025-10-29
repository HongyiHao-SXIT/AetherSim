import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('Road_test.jpg', 1)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.imshow(img)
plt.show()

plt.hist(img.ravel(), 256)   #ravel() 二维降一维  256灰度级的分组情况
plt.show()

# plot绘制opencv返回的直方图值

histb = cv2.calcHist([img], [0], None, [256], [0, 255])
plt.plot(histb, color='b')
plt.show()



