import time,os,sys
from DOGZILLALib import DOGZILLA

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


from PIL import Image


xgo = DOGZILLA()
xgo.reset() 

##前进 forword
def Dog_forword(delay_time):
    xgo.move_x(20) 
    time.sleep(delay_time)
    xgo.stop()

## 后退 back
def Dog_back(delay_time):
    xgo.move_x(-20) 
    time.sleep(delay_time)
    xgo.stop()

## 左平移 Left_move
def Dog_Left_move(delay_time):
    xgo.move_y(12) 
    time.sleep(delay_time)
    xgo.stop()

## 右平移 Rihgt_move
def Dog_Rihgt_move(delay_time):
    xgo.move_y(-12) 
    time.sleep(delay_time)
    xgo.stop()

## 左旋转 LeftTurn
def Dog_LeftTurn(delay_time):
    xgo.turn(-30)
    time.sleep(delay_time)
    xgo.stop()

## 右旋转 RightTurn
def Dog_RightTurn(delay_time):
    xgo.turn(30)
    time.sleep(delay_time)
    xgo.stop()


## 仰视 Looking_up
def Dog_Looking_up():
    xgo.attitude(['p'],[-10])
    time.sleep(1)


## 平视 look_straight
def Dog_look_straight():
    xgo.attitude(['p'],[0])
    time.sleep(1)


## 俯视 look_down
def Dog_look_down():
    xgo.attitude(['p'],[10])
    time.sleep(1)


def Dog_get_down():#趴下 get_down
    xgo.action(1)
    time.sleep(3)

def Dog_Stand_Up():#站起 Stand_Up
    xgo.action(2)
    time.sleep(3)

def Dog_Turn_Around():#转圈 Turn_Around
    xgo.action(4)
    time.sleep(5)

def Dog_Crawl():#匍匐前进 Crawl
    xgo.action(3)
    time.sleep(5)

def Dog_Squat():#蹲起 Squat
    xgo.action(6)
    time.sleep(4)

def Dog_3_Axis():#三轴转动 3Axis
    xgo.action(10)
    time.sleep(7)

def Dog_Pee():#撒尿 Pee
    xgo.action(11)
    time.sleep(7)

def Dog_Sit_Down():#坐下 Sit_Down
    xgo.action(12)
    time.sleep(5)

def Dog_Wave_Hand():#招手 Wave_Hand
    xgo.action(13)
    time.sleep(7)

def Dog_Stretch():#伸懒腰 Stretch
    xgo.action(14)
    time.sleep(10)

def Dog_Wave_Body():#波浪运动 Wave_Body
    xgo.action(15)
    time.sleep(6)

def Dog_Swing():#摇摆运动 Swing
    xgo.action(16)
    time.sleep(6)

def Dog_Handshake():#握手 Handshake
    xgo.action(19)
    time.sleep(10)

def Dog_Dance():#跳舞 Dance
    xgo.action(23)
    time.sleep(6)

def Dog_push_up():#俯卧撑 push up
    xgo.action(21)
    time.sleep(8)



#拍照 #Take photos
import cv2
def take_photo():
    print("take a photo")
    time.sleep(0.5)
    cap=cv2.VideoCapture(0)
    cap.set(3,640)
    cap.set(4,480)

    path = "./ros_dog_agent/"  
    ret,image = cap.read()
    filename = "rec"
    cv2.imwrite(path + filename + ".jpg", image)
    #image = cv2.resize(image, (320, 240))
    
    # imagedata = cv2.imread("./ros_dog_agent/rec.jpg")
    # cv2.imshow('image',imagedata)
    # cv2.waitKey(1)
    # time.sleep(3)
    
    cap.release()
    cv2.destroyAllWindows()
    print("camera close")



from subprocess import Popen
#惊喜的叫 Surprised call
def play_sound_surprised():
    proc = Popen("mplayer ./ros_dog_agent/surprised.wav", shell=True)
    proc.wait()
    time.sleep(2)

#生气的叫 Angry shouting
def play_sound_anger():
    proc = Popen("mplayer ./ros_dog_agent/anger.wav", shell=True)
    proc.wait()
    time.sleep(2)
    
#介绍自己 Introduce yourself  中文版 CN
def play_myself():
    time.sleep(3)
    proc = Popen("mplayer ./ros_dog_agent/myself.mp3", shell=True)
    proc.wait()
    
    
#介绍自己 Introduce yourself  英文版 EN
def play_myself_en():
    time.sleep(3)
    proc = Popen("mplayer ./ros_dog_agent/myself_en.mp3", shell=True)
    proc.wait()
    