#pip install --upgrade spark_ai_python
import os,sys
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

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



from openai import OpenAI
def QAGPT_en(inputtext):
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openAI_KEY,
    )

    completion = client.chat.completions.create(

    #model="google/gemini-2.5-pro-exp-03-25:free",
    model="qwen/qwen2.5-vl-32b-instruct:free",
    #model="meta-llama/llama-4-maverick:free",
    #model="nvidia/llama-3.1-nemotron-ultra-253b-v1:free",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": inputtext
            }
        ]
        }
    ]
    )

    result = completion.choices[0].message.content
    #print(result)
    return result
