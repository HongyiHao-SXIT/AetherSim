from dog_UltraAPI import Ultra_gpt #中文版
from dog_API_en import dogGPT_en #英文版
from dog_ImageAPI import *
from dog_tongyiAPI import *
from dog_base_control import * #基础动作 Basic actions
from dog_tts import Dog_speaktts #音频合成

import time

def QA_Contect(str = "今天的天气如何"):
    re = Ultra_gpt(str)
    print("A:"+re)
    time.sleep(3)
    Dog_speaktts(re)
    
    
def QA_Contect_en(str = "who are you"):
    re = dogGPT_en(str+"English reply")
    print("A:"+re)
    time.sleep(3)
    Dog_speaktts(re)
    
    
    
def read_image_func():
    imagedata = cv2.imread("./ros_dog_agent/rec.jpg")
    cv2.imshow('image',imagedata)
    cv2.waitKey(1)
    time.sleep(3)    
    
#增加个图像描述的接口
def Image_Contect(str="你看到了什么"):
    take_photo()
    time.sleep(0.5)
    read_image_func() #读取图片
    re = Dog_Image(str+"回复50个字以内")
    print("A:"+re)
    time.sleep(3)
    Dog_speaktts(re)
    
#增加个图像描述的接口
def Image_Contect_en(str="what can you see"):
    take_photo()
    time.sleep(0.5)
    read_image_func()
    re = dogGPT_Image_en(str+"Reply within 50 words")
    print("A:"+re)
    time.sleep(3)
    Dog_speaktts(re)
    
