from openai import OpenAI
import os
import base64
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from API_KEY import *



#  base 64 编码格式
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def QwenVL_api_picture(PROMPT='机械狗管家智能体'):
    base64_image = encode_image("./ros_dog_agent/rec.jpg")
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
        api_key= TONYI_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-vl-max-latest",  #qwen-vl-max-latest
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpg;base64,{base64_image}"}, 
                    },
                    {"type": "text", 
                     "text": PROMPT
                    },
                ],
            }
        ],
    )
    #print(completion.model_dump_json())
    #print('大模型调用成功！')
    result = eval(completion.choices[0].message.content)
    #print(result)

    return result



