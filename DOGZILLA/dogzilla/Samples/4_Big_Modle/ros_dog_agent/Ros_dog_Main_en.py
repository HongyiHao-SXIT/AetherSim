from dog_record import * #唤醒并录音 Wake up and record

from DAgent_Image_en import * #动作编排 choreography
from dog_base_control import * #基础动作 Basic actions

from dog_qa_api import * #动态查询时间日期
from dog_football_api import * #踢球 play football
from dog_Track_food_api import * #追踪物体 Tracking objects
from dog_lidar_action import * #雷达导航动作
# from dog_Track_line_api import * #巡线 Tracking Line
# from dog_Track_face_api import * #人脸 Face
# from dog_gesture_api import * #手势 hands
# from dog_qrcode_api import * #二维码识别 QR


import os,sys,time,threading,requests

from dog_speak_iat_en import rec_wav_music_en #语音识别 speak_iat
from dog_tts_en import Xinghou_speaktts #语音合成并播放 Speech synthesis and playback



huanxin = 0
response = ''
def Speak_Vioce():
    global response,huanxin
    try:
        Xinghou_speaktts(response)
        huanxin = 0
    except:
        huanxin = 0
        
#读取图片 read image
def read_image():
    imagedata = cv2.imread("./ros_dog_agent/rec.jpg")
    cv2.imshow('image',imagedata)
    cv2.waitKey(1)
    time.sleep(3)



def play_agent_image():
    print("start")
    global response,huanxin
    while True:
        if detect_keyword() and huanxin == 0:
            huanxin = 1

            if os.path.exists('./demos/ros_dog_agent/myrec.wav'):
                os.remove('./demos/ros_dog_agent/myrec.wav')
            time.sleep(0.2)

            try:
                start_recording()
                time.sleep(0.2)
                rectext = rec_wav_music_en()
                #rectext = "What's in the picture"
                #print(rectext)
            except:
                print("Cannot hear command,try again")
                huanxin = 0
                continue

            #rectext = 'If you see yellow, dance; otherwise, lie down'
            if rectext != "":
                print("Q:"+rectext)
                take_photo() #调用摄像头拍照  Call the camera to take photos
                time.sleep(0.5)
                
                read_image()
                
                #进行动作编排 Perform action choreography
                try:
                    agent_plan_output = eval(Dog_agent_plan_Image_en(rectext))
                    print('The specific image intelligent agent choreography actions are as follows', agent_plan_output)

                    response = agent_plan_output['response'] # 获取机器人想对我说的话 Get what the robot wants to say to me
                    #print('Start speech synthesis and play:'+response)
                    print("A:"+response)
                except:
                    print("try again...")
                    huanxin = 0
                    continue


                #开启语音线程,使其能边动边用 Activate the voice thread so that it can be used while moving
                tts_thread = threading.Thread(target=Speak_Vioce)
                tts_thread.daemon = True  
                tts_thread.start()

                for each in agent_plan_output['function']: # 运行智能体规划编排的每个函数 Run each function of intelligent agent planning and orchestration
                    try: #有异常往下接着运行 There is an abnormality and it continues to run downwards
                        eval(each)
                    except:
                        continue

                time.sleep(0.5)

        else :
            time.sleep(0.5)
            huanxin = 0
            
        if rectext == 0:
            break
        
        

if __name__ == '__main__':
    #Test the network
    net = False
    try:
        html = requests.get("http://www.baidu.com", timeout=2)
        net = True
    except Exception as e:
        print(f"Network check failed: {e}")
        net = False

    if net:    
        play_agent_image()

    else:
        while True:
            time.sleep(0.1)