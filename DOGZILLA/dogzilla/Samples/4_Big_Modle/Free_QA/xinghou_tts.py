import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import time
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os,sys
from subprocess import Popen


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from API_KEY import *



STATUS_FIRST_FRAME = 0  # 第一帧的标识 Identification of the first frame
STATUS_CONTINUE_FRAME = 1  # 中间帧标识 Intermediate frame identification
STATUS_LAST_FRAME = 2  # 最后一帧的标识 Identification of the last frame

wsParam = ''

class Ws_Param(object):
    # 初始化 initialization
    def __init__(self, APPID, APIKey, APISecret, Text):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.Text = Text

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {"aue": "lame", "sfl":1,"auf": "audio/L16;rate=16000", "vcn": "xiaoyan", "tte": "utf8"}
        self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-8')), "UTF8")}
        #使用小语种须使用以下方式，此处的unicode指的是 utf16小端的编码方式，即"UTF-16LE"”
        #self.Data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-16')), "UTF8")}

    # 生成url Generate URL
    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        # 生成RFC1123格式的时间戳 Generate timestamp in RFC1123 format
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串 Splicing strings
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密 Encrypt hmac-sha256
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典 Combine the requested authentication parameters into a dictionary
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # 拼接鉴权参数，生成url Splicing authentication parameters and generating URLs
        url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url

def on_message(ws, message):
    try:
        message =json.loads(message)
        code = message["code"]
        sid = message["sid"]
        audio = message["data"]["audio"]
        audio = base64.b64decode(audio)
        status = message["data"]["status"]
        #print(message)
        if status == 2:
            #print("ws is closed")
            ws.close()
        if code != 0:
            errMsg = message["message"]
            print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))
        else:
            with open('./answer.mp3', 'ab') as f:
                f.write(audio)
                #print("iconm")

    except Exception as e:
        print("receive msg,but parse exception:", e)



# 收到websocket错误的处理 Handling of websocket errors received
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理 Received processing for closing websocket
def on_close(ws):
    print("### closed ###")


# 收到websocket连接建立的处理 Received processing for establishing websocket connection
def on_open(ws):
    def run(*args):
        d = {"common": wsParam.CommonArgs,
             "business": wsParam.BusinessArgs,
             "data": wsParam.Data,
             }
        d = json.dumps(d)
        #print("------>开始发送文本数据")
        ws.send(d)
        if os.path.exists('./answer.mp3'):
            os.remove('./answer.mp3')

    thread.start_new_thread(run, ())


def Xinghou_speaktts(context="这个是合成音频程序"):
    global wsParam
    # 测试时候在此处正确填写相关信息即可运行 Fill in the relevant information correctly here during testing to run
    wsParam = Ws_Param(APPID=XINGHOU_APPID,
                       APISecret=XINGHOU_APISecret,
                       APIKey=XINGHOU_KEY,
                       Text=context)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    #播放音频 PLAY AUDIO
    proc = Popen("mplayer ./answer.mp3", shell=True)#sudo 
    #proc.wait()
    time.sleep(0.5)

