# 机械狗智能体主要程序入口文件 英文部分
#Main program entry files for mechanical dog intelligent agents  English section

from dog_record import * #唤醒并录音 Wake up and record



from DAgent_en import * #动作编排 choreography

from dog_base_control import * #基础动作 Basic actions
from dog_football_api import * #踢球 play football
from dog_qa_api import * #动态查询时间日期


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




def play_agent():
    print("start")
    global response,huanxin
    while True:
        if detect_keyword() and huanxin == 0:
            huanxin = 1
            
            if os.path.exists('./demos/dog_agent/myrec.wav'):
                os.remove('./demos/dog_agent/myrec.wav')
            time.sleep(0.2)

            try:
                start_recording()
                time.sleep(0.2)
                rectext = rec_wav_music_en()
                #rectext = "Tell me what can you see?"
                #print(rectext)
            except:
                print("Cannot hear command,try again")
                huanxin = 0
                continue


            if rectext != "":
                print("Q:"+rectext)
                               
                try:
                    agent_plan_output = eval(Dog_agent_plan_en(rectext)) 
                    print('**The intelligent agent arranges actions as follows**', agent_plan_output)
                    response = agent_plan_output['response'] 
                    #print('**Start speech synthesis and play**：'+response)  
                except:
                    display_text = "try again..."
                    print(display_text)
                    
                    huanxin = 0
                    continue

                print("A:"+response)                          

                tts_thread = threading.Thread(target=Speak_Vioce)
                tts_thread.daemon = True  
                tts_thread.start()
                

                for each in agent_plan_output['function']: 
                    print('Start executing action', each)
                    try: 
                        eval(each)
                    except:
                        continue

                time.sleep(0.5)

            else :
                print("No information was recognized, try again") 
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
        while True:
            time.sleep(0.1)