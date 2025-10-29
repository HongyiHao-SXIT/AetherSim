from openai import OpenAI
import os
import base64
import cv2
import sys
import time
from DOGZILLALib import DOGZILLA

from PIL import Image,ImageDraw,ImageFont

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


from API_KEY import *


SYSTEM_PROMPT ='''
下边我会说想要追踪的物体，请把我想要追踪的物体的左上角和右下角的像素坐标返回给我，直接返回坐标位置即可。
比如追踪物体它的左上角坐标是(120,140)，右下角的坐标是(200,210)，则回复我[120,140,200,210]，不要回复其它的内容。
请注意图片大小只有320*240的像素尺寸,其中图片左上角的起始点的坐标为(0,0),图片右下角的最终点坐标为(320,240)。
现在，我的指令是:
'''

g_dog = DOGZILLA()



#  base 64 编码格式
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def QwenVL_api_picture(PROMPT='追踪积木块上方的物体'):
    base64_image = encode_image("./ros_dog_agent/myrec.jpeg")
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
        api_key= TONYI_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
        model="qwen-vl-max-latest",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}, 
                    },
                    {"type": "text", 
                     "text": SYSTEM_PROMPT + PROMPT
                    },
                ],
            }
        ],
    )
    #print(completion.model_dump_json())
    #print('大模型调用成功！')
    result = eval(completion.choices[0].message.content)
    print(result)
    # img_bgr = cv2.imread('/home/pi/RaspberryPi-CM4-main/demos/speech_ai_file/myrec.jpeg')
    # img_bgr = cv2.rectangle(img_bgr, (result[0], result[1]), (result[2], result[3]), [0, 255, 255], thickness=2)
    # cv2.imwrite('./testt.jpg', img_bgr)
    return result


def take_photo_Track():
    cv2.destroyAllWindows()
    print("camera open Track")
    g_dog.attitude(['p'],[15])
    time.sleep(2)

    time.sleep(0.5)
    cap=cv2.VideoCapture(0)
    cap.set(3,320)
    cap.set(4,240)

    path = "./ros_dog_agent/"
    ret, image  = cap.read()
    filename = "myrec"
    cv2.imwrite(path + filename + ".jpeg", image)
    image = cv2.resize(image, (320, 240))
    time.sleep(1)
    cap.release()
    cv2.destroyAllWindows()
    print("camera close")


# 图像预处理：转换为灰度图并进行直方图均衡化 Image preprocessing: Convert to grayscale image and perform histogram equalization
def preprocess_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(2, 2)) 
    equalized = clahe.apply(gray)
    return cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)  # 转换回 BGR 格式


# message = sys.argv[1]

def Tarck_Food(str='追踪可乐旁边的物体'):
    try:
        #拍照 take photo
        time.sleep(1)
        take_photo_Track()

        result_my = QwenVL_api_picture(str)

        # 让用户选择 ROI  Allow users to choose ROI
        bbox = (result_my[0], result_my[1], result_my[2]-result_my[0], result_my[3]-result_my[1])  #替换成大模型给的坐标 Replace with the coordinates given by the large model

        cap=cv2.VideoCapture(0)
        cap.set(3,320)
        cap.set(4,240)

        # 读取首帧 Read the first frame
        ret, frame = cap.read()
        frame = preprocess_frame(frame)

        # 验证 bbox 的有效性 Verify the effectiveness of bbox
        if bbox[2] <= 0 or bbox[3] <= 0:
            print("BOX Error!!!")
            cap.release()
            return


        param = cv2.TrackerKCF.Params()
        param.detect_thresh = 0.2
        tracker = cv2.TrackerKCF_create(param)
        tracker.init(frame, bbox)

        pTime, cTime = 0, 0
        imshow_num = 0
        # 主循环 main
        while True:
            ret, frame = cap.read()

            # 更新跟踪器 Update tracker
            timer = cv2.getTickCount()
            success, bbox = tracker.update(frame)
            cTime = time.time()
            

            # 绘制跟踪结果 Draw tracking results
            if success:
                x, y, w, h = [int(v) for v in bbox]

                value_x = x+w/2 - 160
                value_y = y+h/2 - 120
                if value_x > 55:
                    value_x = 55
                elif value_x < -55:
                    value_x = -55
                if value_y > 75:
                    value_y = 75
                elif value_y < -75:
                    value_y = -75
                g_dog.attitude(['y','p'],[-value_x/10, value_y/10])

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "success", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "fail", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        
            
            
            imshow_num +=1
            if imshow_num%2==0:
                # 显示结果 Display results
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                cv2.imshow("frame", frame)
                imshow_num = 0

            

            if cv2.waitKey(1)==ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                g_dog.reset()
                break

        # 释放资源 Release resources
        cap.release()
        g_dog.reset()
        
    except:
        cap.release()
        g_dog.reset()
        cv2.destroyAllWindows()
        

