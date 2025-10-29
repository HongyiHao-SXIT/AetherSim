# encoding: UTF-8
import time,sys,os
import requests
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json
from PIL import Image
from io import BytesIO

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from API_KEY import *

splash_theme_color = (15,21,46)

class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Url:
    def __init__(this, host, path, schema):
        this.host = host
        this.path = path
        this.schema = schema
        pass


# calculate sha256 and encode to base64
def sha256base64(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
    return digest


def parse_url(requset_url):
    stidx = requset_url.index("://")
    host = requset_url[stidx + 3:]
    schema = requset_url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise AssembleHeaderException("invalid request url:" + requset_url)
    path = host[edidx:]
    host = host[:edidx]
    u = Url(host, path, schema)
    return u


# 生成鉴权url Generate authentication URL
def assemble_ws_auth_url(requset_url, method="GET", api_key="", api_secret=""):
    u = parse_url(requset_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    # print(date)
    # date = "Thu, 12 Dec 2019 01:57:27 GMT"
    signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
    # print(signature_origin)
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    # print(authorization_origin)
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }

    return requset_url + "?" + urlencode(values)

# 生成请求body体 Generate request body
def getBody(appid,text):
    body= {
        "header": {
            "app_id": appid,
            "uid":"123456789"
        },
        "parameter": {
            "chat": {
                "domain": "general",
                "temperature":0.5,
                "max_tokens":4096
            }
        },
        "payload": {
            "message":{
                "text":[
                    {
                        "role":"user",
                        "content":text
                    }
                ]
            }
        }
    }
    return body

# 发起请求并返回结果 Initiate a request and return the result
def draw_main(text,appid,apikey,apisecret):
    host = 'http://spark-api.cn-huabei-1.xf-yun.com/v2.1/tti'
    url = assemble_ws_auth_url(host,method='POST',api_key=apikey,api_secret=apisecret)
    content = getBody(appid,text)
    print(time.time())
    response = requests.post(url,json=content,headers={'content-type': "application/json"}).text
    print(time.time())
    return response

#将base64 的图片数据存在本地 Store the image data of base64 locally
def base64_to_image(base64_data, save_path):
    # 解码base64数据 Decoding base64 data
    img_data = base64.b64decode(base64_data)

    # 将解码后的数据转换为图片 Convert decoded data into images
    img = Image.open(BytesIO(img_data))

    # 保存图片到本地 Save the image locally
    img.save(save_path)



# 解析并保存到指定位置 Parse and save to the specified location
def parser_Message(message):
    data = json.loads(message)
    # print("data" + str(message))
    code = data["header"]["code"]
    if code != 0:
        print(f"请求错误: {code}, {data}")
    else:
        text = data["payload"]["choices"]["text"]
        imageContent = text[0]
        # if('image' == imageContent["content_type"]):
        imageBase = imageContent["content"]
        imageName = data["header"]["sid"]
        savePath = f"./Image_create/original.jpg"
        base64_to_image(imageBase, savePath)
        print("图片保存路径：" + savePath)

def resize_image(image_path, output_path, size=(640, 480)):
    with Image.open(image_path) as img:
        img_resized = img.resize(size)
        img_resized.save(output_path)
        print(f"Image resized successfully and saved at {output_path}")

import cv2
def gpt_draw(scr):
    desc = scr
    res = draw_main(
        desc,
        appid=XINGHOU_APPID,
        apikey=XINGHOU_KEY,
        apisecret=XINGHOU_APISecret,
    )
    parser_Message(res)
    original_image_path = "./Image_create/original.jpg"
    resized_image_path = "./Image_create/resized.jpg"
    resize_image(original_image_path, resized_image_path)
    time.sleep(0.5)

    #image = Image.open("./Image_create/resized.jpg")
    imagedata = cv2.imread("./Image_create/resized.jpg")
    cv2.imshow('image',imagedata)
    cv2.waitKey(1)
    
    time.sleep(5.5)
    cv2.destroyAllWindows()




