import os,sys,time,threading,requests


from xinghou_UltraAPI import *


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from audio import start_recording, detect_keyword
from tts_en import *
from speak_iat_en import rec_wav_music_en


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
            
            content = rec_wav_music_en()

            if content != "":
                print("Q:"+content)
                re = QAGPT_en(content+"English reply") #English

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
    print("The detection network is not connected, please restart")
    while True:
        time.sleep(0.1)

