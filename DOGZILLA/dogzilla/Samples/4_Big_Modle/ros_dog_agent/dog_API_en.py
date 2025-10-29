from openai import OpenAI
import base64
import os,sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from API_KEY import *


def dogGPT_en(inputtext):
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



def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")



def dogGPT_Image_en(inputtext):
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openAI_KEY,
    )

    image_path = "./ros_dog_agent/rec.jpg"
    base64_image = encode_image(image_path)

    completion = client.chat.completions.create(

    model="qwen/qwen2.5-vl-32b-instruct:free",
    #model="meta-llama/llama-3.2-11b-vision-instruct:free",
    messages=[
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": inputtext
            },
            {
              "type": "image_url",
              "image_url": {"url": f"data:image/jpg;base64,{base64_image}"},
            }
        ]
        }
    ]
    )

    result = completion.choices[0].message.content
    #print(result)
    return result
    


