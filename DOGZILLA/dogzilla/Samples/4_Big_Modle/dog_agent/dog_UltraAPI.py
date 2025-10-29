#pip install --upgrade spark_ai_python

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

import os,sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from API_KEY import *

def Ultra_gpt(speech_text):
   
    SPARKAI_URL = "wss://spark-api.xf-yun.com/v4.0/chat"
    SPARKAI_APP_ID = XINGHOU_APPID
    SPARKAI_API_SECRET = XINGHOU_APISecret
    SPARKAI_API_KEY = XINGHOU_KEY
    SPARKAI_DOMAIN = "4.0Ultra"

    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )


    messages = [ChatMessage(role="user", content=speech_text)]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    return a.generations[0][0].text