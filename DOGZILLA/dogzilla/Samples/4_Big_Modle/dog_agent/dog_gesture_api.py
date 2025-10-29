from DOGZILLALib import DOGZILLA
import cv2
import threading
from gesture_action import handDetector  
import time




g_dog = DOGZILLA()

finger_number = None
action_flag = 0


def dog_action():
    global finger_number,action_flag
    
    while True:
        if(finger_number == "OK"):
            action_flag = 1
            g_dog.action(12) #坐下 Sit_Down
            time.sleep(5)
            action_flag = 0
           
            
        
        elif(finger_number == "Five"):
            action_flag = 1
            g_dog.action(13) #招手 Wave_Hand
            time.sleep(7)
            action_flag = 0
            
        
        elif(finger_number == "Six"):
            action_flag = 1
            g_dog.action(11) #撒尿 Pee
            time.sleep(7)
            action_flag = 0
    
    




def gesture_function():
    try:
        cv2.destroyAllWindows() 
        dlet = 1
        hand_detector = handDetector(detectorCon=0.8)
        cap = cv2.VideoCapture(0)
        cap.set(3,320*dlet)
        cap.set(4,240*dlet)
        fps_num = 0
        
        action_thread = threading.Thread(target=dog_action)
        action_thread.daemon = True  
        action_thread.start()
        
        global finger_number,action_flag
        while True:
            ret, frame = cap.read()
            #img_height, img_width, _ = frame.shape
            hand_detector.findHands(frame, draw=False) 
            if len(hand_detector.lmList) != 0:
                # 转向控制部分
                # Turning control section
                # MediaPipe中, 手部最中心的指关节的编号为9
                # In MediaPipe, the index of the central finger joint is 9
                x,y = hand_detector.findPoint(9)
                cv2.circle(frame,(int(x),int(y)),2,(0,255,255),6)

                value_x = x - 160*dlet
                value_y = y - 120*dlet

                if value_x > 55*dlet:
                    value_x = 55*dlet
                elif value_x < -55*dlet:
                    value_x = -55*dlet
                if value_y > 75*dlet:
                    value_y = 75*dlet
                elif value_y < -75*dlet:
                    value_y = -75*dlet

                finger_number = hand_detector.get_gesture()
                #finger_str=f"Number:{finger_number}"
                
                try:
                    fps_num +=1
                    if fps_num %2 == 0:
                        cv2.putText(frame, finger_number, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 1)
                        cv2.imshow('frame',frame)
                        fps_num = 0
                            
                except:
                    continue

                #print(finger_number)

                
                if(finger_number != "Zero")and action_flag == 0:
                    g_dog.attitude(['y','p'],[-value_x/(8*dlet), value_y/(8*dlet)]) #8
                    
                
            else:
                x = 0
                y = 0



            if cv2.waitKey(1) == ord('q'):
                g_dog.reset()
                cap.release()
                cv2.destroyAllWindows() 
                break
    finally:
        g_dog.reset()
        cap.release()
        cv2.destroyAllWindows() 
        


