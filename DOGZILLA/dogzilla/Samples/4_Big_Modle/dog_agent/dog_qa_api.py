from dog_UltraAPI import Ultra_gpt #中文版
from dog_API_en import dogGPT_en #英文版

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
    