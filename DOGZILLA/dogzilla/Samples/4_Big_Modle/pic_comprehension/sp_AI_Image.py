import os,sys,time,threading,requests
import cv2
from xinghou_ImageAPI import *
from xinghou_tts import *
from audio import start_recording, detect_keyword
from xinghou_speak_iat import rec_wav_music

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from audio import start_recording, detect_keyword



imsho_flag = 0
#读取图片
def read_image():
    global imsho_flag
    while True:
        if imsho_flag == 1:
            imagedata = cv2.imread("./pic_comprehension/rec.jpg")
            cv2.imshow('image',imagedata)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            imsho_flag =0
                

response = ''
def Speak_Vioce():
    global response
    Xinghou_speaktts(response)#播放音频 PLAY AUDIO


def take_photo():
    global imsho_flag
    print("take a photo")
    time.sleep(0.5)
    cap=cv2.VideoCapture(0)
    cap.set(3,320*2)
    cap.set(4,240*2)

    path = "./pic_comprehension/"  
    ret, image = cap.read()
    filename = "rec"
    cv2.imwrite(path + filename + ".jpg", image)
    #image = cv2.resize(image, (320, 240))
    
    # cv2.imshow('image',image)
    # cv2.waitKey(5)
    
    time.sleep(1)
    cap.release()
    cv2.destroyAllWindows()
    
    # 拍摄显示图片
    imsho_flag =1
    print("camera close")

#Test the network
net = False
try:
    html = requests.get("http://www.baidu.com", timeout=2)
    net = True
except Exception as e:
    print(f"Network check failed: {e}")
    net = False

#Record and control the dog
if net:
    imshow_thread = threading.Thread(target=read_image)
    imshow_thread.daemon = True  
    imshow_thread.start()
    
    while True:
        if detect_keyword():
            cv2.destroyAllWindows()
            os.system("pkill mplayer") 
            time.sleep(.2)
           
            start_recording()
            content = rec_wav_music()

            if content != "":
                print("Q:"+content)
               
                take_photo()
                time.sleep(1)
                
                mymytext = xinghou_Image(content)#图像描述 image description
                
                time.sleep(1)

                print("A:"+mymytext)
                

                try:
                    response = mymytext
                    tts_thread = threading.Thread(target=Speak_Vioce)
                    tts_thread.daemon = True  
                    tts_thread.start()
                                        
                except:
                    pass
            if content == 0:
               break

        time.sleep(0.1)  
else:
    print("检测网络没连上，请重启")
    while True:
        time.sleep(0.1)


