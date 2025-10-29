# 机械狗智能体主要程序入口文件 Main program entry files for mechanical dog intelligent agents

from dog_record import * #唤醒并录音 Wake up and record
from dog_speak_iat import * #音频识别 Audio recognition
from dog_agent_Image import * #动作编排+图像的 Action choreography+visual representation
from dog_base_control import * #基础动作 Basic actions
from dog_tts import * #语音合成并播放 Speech synthesis and playback
from dog_qa_api import * #动态查询时间日期
from dog_football_api import * #踢球 play football
from dog_Track_food_api import * #追踪物体 Tracking objects
from dog_Track_line_api import * #巡线 Tracking Line
from dog_Track_face_api import * #人脸 Face
from dog_gesture_api import * #手势 hands
from dog_qrcode_api import * #二维码识别 QR



import os,sys,time,threading,requests
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)



huanxin = 0
response = ''
def Speak_Vioce():
    global response,huanxin
    Dog_speaktts(response)
    huanxin = 0

imsho_flag = 0
#读取图片 read image
def read_image():
    imagedata = cv2.imread("./dog_agent/rec.jpg")
    cv2.imshow('image',imagedata)
    cv2.waitKey(1)
    time.sleep(3)
            
            


def play_agent_image():
    
    print("start")
    global response,huanxin,imsho_flag
    
    while True:
        if huanxin==0:
            if detect_keyword() :
                huanxin = 1
                #先把存在的录音删掉 First, delete the existing recording
                if os.path.exists('./dog_agent/myrec.wav'):
                    os.remove('./dog_agent/myrec.wav')
                time.sleep(0.2)

                try:
                    start_recording()
                    time.sleep(0.2)
                    rectext = rec_wav_music()#进行语音识别 Perform speech recognition
                    #rectext = '眼前的黄色小球我不想看到它'
                    #print(rectext)
                except:
                    print("录音出现未知错误,请重试!")
                    huanxin = 0
                    continue

                if rectext != "":
                
                    print("Q:"+rectext)
                
                    take_photo() #调用摄像头拍照  Call the camera to take photos
                    #time.sleep(0.5)
                    #imsho_flag = 1
                    
                    read_image()
                    
                    
                    try:
                        #进行动作编排 Perform action choreography
                        agent_plan_output = Dog_agent_plan_Image(rectext)#通义千问调用 Tongyi Qianwen Call
                        #agent_plan_output = eval(Dog_agent_plan_Image(rectext))#讯飞星火使用 IFlytek Spark usage
                        print('具体图像智能体编排动作如下\n', agent_plan_output)

                        response = agent_plan_output['response'] # 获取机器人想对我说的话 Get what the robot wants to say to me
                        print('A:'+response)
                    except:
                        print("大模型信息返回有误,请重试!")
                        huanxin = 0
                        continue

                    #开启语音线程,使其能边动边用 Activate the voice thread so that it can be used while moving
                    tts_thread = threading.Thread(target=Speak_Vioce)
                    tts_thread.daemon = True  
                    tts_thread.start()

                    for each in agent_plan_output['function']: # 运行智能体规划编排的每个函数 Run each function of intelligent agent planning and orchestration
                        print('开始执行动作', each)
                        try: #有异常往下接着运行 There is an abnormality and it continues to run downwards
                            eval(each)
                        except:
                            continue

                    time.sleep(0.5)

                else :
                    print("没有识别到任何信息,请重试")
                    huanxin = 0
            
                if rectext == 0:
                    break
        
        
#运行验证部分 Run verification section

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
        try:  
            play_agent_image()
        except:
            cv2.destroyAllWindows() 

    else:
        print("网络连接异常，请重启!")
        while True:
            time.sleep(0.1)