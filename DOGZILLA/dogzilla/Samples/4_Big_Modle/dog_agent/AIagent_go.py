# 机械狗智能体主要程序入口文件 Main program entry files for mechanical dog intelligent agents

from dog_record import * #唤醒并录音 Wake up and record
from dog_speak_iat import * #音频识别 Audio recognition
from dog_agent import * #动作编排 choreography
from dog_base_control import * #基础动作 Basic actions
from dog_tts import * #语音合成并播放 Speech synthesis and playback

from dog_qa_api import * #动态查询时间日期

from dog_football_api import * #踢球 play football

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



def play_agent():
    print("start")
    global response,huanxin
    while True:
        if huanxin ==0:
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

                    
                    
                except:
                    print("录音出现未知错误，请重试!")
                    huanxin = 0
                    continue

                if rectext != "":
                    print("Q:"+rectext)
                    try:
                        agent_plan_output = eval(Dog_agent_plan(rectext))#进行动作编排  Perform action choreography
                        print('智能体编排动作如下\n', agent_plan_output)
                        response = agent_plan_output['response'] # 获取机器人想对我说的话 Get what the robot wants to say to me
                        print('A:'+response)  
                    except:
                        print("在线大模型信息返回错误，请重试!")
                        huanxin = 0
                        continue



                    #开启语音线程,使其能边动边用 Activate the voice thread so that it can be used while moving
                    tts_thread = threading.Thread(target=Speak_Vioce)
                    tts_thread.daemon = True  
                    tts_thread.start()
                    

                    for each in agent_plan_output['function']: # 运行智能体规划编排的每个函数  Run each function of intelligent agent planning and orchestration
                        print('开始执行动作', each)
                        try: 
                            eval(each)
                        except:
                            continue
                    
                    time.sleep(0.5)

                else :
                    print("没有识别到任何信息,请重试")
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
        play_agent()

    else:
        print("网络连接失败,请重试!")
        while True:
            time.sleep(0.1)