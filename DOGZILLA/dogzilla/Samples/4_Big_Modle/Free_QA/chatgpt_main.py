import os,sys,time,threading,requests

from xinghou_speak_iat import rec_wav_music
from xinghou_UltraAPI import *
from xinghou_tts import *

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from audio import start_recording, detect_keyword


response = ''
def Speak_Vioce():
    global response
    Xinghou_speaktts(response)#播放音频 PLAY AUDIO



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
    while True:
        if detect_keyword():
            os.system("pkill mplayer") 
            time.sleep(.2)
            
            start_recording()
            time.sleep(1)
            
            content = rec_wav_music()

            if content != "":
                print("Q:"+content)
                re = Ultra_gpt(content) #中文版 chinese

                print("A:"+re)
                try:
                    response = re
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

