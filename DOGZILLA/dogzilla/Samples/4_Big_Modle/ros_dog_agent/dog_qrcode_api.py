import cv2
import os,socket,sys,time
import numpy as np
from DOGZILLALib import DOGZILLA

import threading
import inspect
import ctypes
#-----------------------COMMON INIT-----------------------
import pyzbar.pyzbar as pyzbar




g_dog = DOGZILLA()
g_barcodeData = ''
g_Tstop = True

 



def control_action():
    global g_barcodeData,g_Tstop
    while g_Tstop:
        time.sleep(1)
        barcodeData = g_barcodeData.casefold()
        #print('control_action',barcodeData)
        if(barcodeData == "goahead".casefold()):
            g_dog.move('x',20) 
            time.sleep(2)
            g_dog.stop()

        elif(barcodeData == "goback".casefold()):
            g_dog.move('x',-20) 
            time.sleep(2)
            g_dog.stop()

        elif(barcodeData == "turnright".casefold()):
            g_dog.turn(-20) 
            time.sleep(2)
            g_dog.stop()
            
        elif(barcodeData == "turnleft".casefold()):
            g_dog.turn(20) 
            time.sleep(2)
            g_dog.stop()

        
        elif barcodeData == "LIE DOWN".casefold():
            g_dog.action(1) #趴下
            
        elif barcodeData == "STAND UP".casefold():
            g_dog.action(2)  #站起
            
        elif barcodeData == "CRAWL".casefold():
            g_dog.action(3)  #匍匐前进
            
        elif barcodeData == "TURN AROUND".casefold():
            g_dog.action(4) #转圈
            
        elif barcodeData == "MARK TIME".casefold():
            g_dog.action(5) #原地踏步
            
        elif barcodeData == "SQUAT".casefold():
            g_dog.action(6) #蹲起
            
        elif barcodeData == "TURN ROLL".casefold():
            g_dog.action(7) #转动ROLL
            
        elif barcodeData == "TURN PITCH".casefold():
            g_dog.action(8) #转动PITCH
            
        elif barcodeData == "TURN YAW".casefold():
            g_dog.action(9) #转动YAW
            
        elif barcodeData == "3 AXIS".casefold():
            g_dog.action(10) #三轴联动
            
        elif barcodeData == "PEE".casefold():
            g_dog.action(11) #撒尿
            
        elif barcodeData == "SIT DOWN".casefold():
            g_dog.action(12) #坐下
            
        elif barcodeData == "WAVE(HAND)".casefold():
            g_dog.action(13) #招手
            
        elif barcodeData == "STRETCH".casefold():
            g_dog.action(14) #伸懒腰
            
        elif barcodeData == "WAVE(BODY)".casefold():
            g_dog.action(15) #波浪
        
        elif barcodeData == "SWING".casefold():
            g_dog.action(16) #摇摆
        
        elif barcodeData == "PRAY".casefold():
            g_dog.action(17) #求食
            
        elif barcodeData == "SEEK".casefold():
            g_dog.action(18) #找食物
            
        elif barcodeData == "HANDSHAKE".casefold():
            g_dog.action(19) #握手
    

        g_barcodeData = ''



# 解析图像中的二维码信息  Analyze the qrcode information in the image
def decodeDisplay(image, qrdisplay):
    global g_barcodeData
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        # 提取二维码的边界框的位置, 画出图像中条形码的边界框
        # Extract the position of the bounding box of the qrcode, 
        # and draw the bounding box of the barcode in the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(qrdisplay, (x, y), (x + w, y + h), (225, 225, 225), 2)

        # 提取二维码数据为字节对象，转换成字符串
        # The qrcode data is extracted as byte objects and converted into strings
        g_barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # 绘出图像上条形码的数据和条形码类型  
        # Plot the barcode data and barcode type on the image
        text = "{} ({})".format(g_barcodeData, barcodeType)
        cv2.putText(qrdisplay, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (225, 0, 0), 2)

        #print("[INFO] Found {} barcode: {}".format(barcodeType, g_barcodeData))
        
    return qrdisplay


# 检测二维码  detect qrcode
def Detect_Qrcode_Task():
    global g_Tstop
    t_start = time.time()
    fps = 0
    
    cap=cv2.VideoCapture(0)
    cap.set(3,320)
    cap.set(4,240)
    if(not cap.isOpened()):
        print("[camera.py:cam]:can't open this camera")
        g_Tstop = False
        g_dog.reset()
        return
        
    while True:
        ret, frame = cap.read()
        # 转为灰度图像  Convert to grayscale image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = decodeDisplay(gray, frame)
        fps = fps + 1
        mfps = fps / (time.time() - t_start)
        cv2.putText(frame, "FPS " + str(int(mfps)), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 3)
        
        cv2.imshow("image1",frame)

        if (cv2.waitKey(1)) == ord('q'):
            g_Tstop = False
            g_dog.reset()
            cap.release()
            cv2.destroyAllWindows() 
            break


def dog_QR_sport():
    global g_Tstop
    try:
        cv2.destroyAllWindows() 
        thread1 = threading.Thread(target=control_action)
        thread1.setDaemon(True)
        thread1.start()
        Detect_Qrcode_Task()
    except:
        g_Tstop = False
        g_dog.reset()
        cv2.destroyAllWindows() 



