import os,sys,time,threading,requests


from creat_img import *
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from audio import start_recording, detect_keyword

from xinghou_speak_iat import rec_wav_music





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
            
            start_recording()
            content = rec_wav_music()

            if content != "":
                
                print("Q:"+content)                
                gpt_draw(content)
                
            if content == 0:
               break

        time.sleep(0.1)  
else:
    print("请检查网络连接,重启")
    while True:
        time.sleep(0.1)

