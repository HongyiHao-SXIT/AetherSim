import cv2
import numpy as np
newImageInfo = (500,500,3)
dst = np.zeros(newImageInfo,np.uint8)
#  1 2 左上角 3 右下角 4 5 fill -1 >0 line w
cv2.rectangle(dst,(350,100),(400,270),(0,255,0),3)
# 2 center 3 r 
cv2.circle(dst,(250,250),(50),(255,0,0),2)
# 2 center 3 轴 4 angle 5 begin 6 end 7 
cv2.ellipse(dst, (256,256), (150,100), 0, 0, 180, (0,255,255), -1)

points = np.array([[150,50], [140,140], [200,170], [250,250], [150,50]], np.int32)
#print(points.shape)
points = points.reshape((-1,1,2))
#print(points.shape)
cv2.polylines(dst,[points],True,(255,255,0))
# cv2.imshow('dst',dst)
# cv2.waitKey(0)

import matplotlib.pyplot as plt

dst = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
plt.imshow(dst)
plt.show()

