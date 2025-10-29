import cv2
import os,socket,sys,time
from PIL import Image,ImageDraw,ImageFont
import numpy as np

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from DOGZILLALib import DOGZILLA
import PID



mode=1 
color_lower = np.array([0, 43, 46])
color_upper = np.array([10, 255, 255])


def limit_fun(input,min,max):
    if input < min:
        input = min
    elif input > max:
        input = max
    return input

def change_color(colorball='red'):
    global color_lower,color_upper,mode
    if colorball=='red':  #red
        color_lower = np.array([0, 43, 46])
        color_upper = np.array([10, 255, 255])
        mode = 1
        return 0
    elif colorball=='green': #green
        color_lower = np.array([35, 43, 46])
        color_upper = np.array([77, 255, 255])
        mode = 2
        return 0
    elif colorball=='blue':   #blue
        color_lower = np.array([100, 43, 46])
        color_upper = np.array([124, 255, 255])
        mode = 3
        return 0
    elif colorball=='yellow':   #yellow
        color_lower = np.array([26, 43, 46])
        color_upper = np.array([34, 255, 255])
        mode = 4
        return 0  
    return 1


def play_football_color(colorball = 'red'):
    
    cv2.destroyAllWindows() 
    
    global color_lower,color_upper,mode
    flag = change_color(colorball)

    if flag == 1: #不是这4个颜色失败 Not these four colors failed
        return
    
    g_mode=1 

    #初始化pid init pid
    Px = 0.25 #0.35
    Ix = 0
    Dx = 0.0001
    X_Middle_error = 160 #图像X轴中心 Image X-axis center
    X_track_PID = PID.PositionalPID(Px, Ix, Dx) 
    obj_error = 105 #球距离中心点的偏差 Deviation of the ball from the center point

    four_leg = [11,12,13,21,22,23,31,32,33,41,42,43]
    g_dog = DOGZILLA()

    #让狗蹲下，重心后移 Let the dog squat down and shift its center of gravity backwards
    g_dog.attitude(['p'],[15])
    time.sleep(0.2)
    #蹲下找寻 Squat down to search
    g_dog.translation(['z'],[75])
    time.sleep(0.2)

    g_dog.pace('slow') #巡线的速度 Speed of patrol line
    time.sleep(.2)

    blue=(255,0,0)
    green=(0,255,0)
    red=(0,0,255)
    yellow=(0,255,255)


    #-----------------------COMMON INIT-----------------------
    cap=cv2.VideoCapture(0)
    cap.set(3,320)
    cap.set(4,240)

    t_start = time.time()
    fps = 0
    color_x = 0
    color_y = 0
    color_radius = 0
    step = 0 #用于记录到达目标的时间点 Used to record the time point of arrival at the target
    
    fps_time = 0

    try:
        while 1:
            ret, frame = cap.read()
            frame_ = cv2.GaussianBlur(frame,(5,5),0)                    
            hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv,color_lower,color_upper)  
            mask = cv2.erode(mask,None,iterations=2)
            mask = cv2.dilate(mask,None,iterations=2)
            mask = cv2.GaussianBlur(mask,(3,3),0)     
            cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2] 

            
            if g_mode == 1:
                if len(cnts) > 0:
                    cnt = max (cnts, key = cv2.contourArea)
                    (color_x,color_y),color_radius = cv2.minEnclosingCircle(cnt)
                    if color_radius > 10:
                        cv2.circle(frame,(int(color_x),int(color_y)),int(color_radius),(255,0,255),2)  
                    
                    # if color_x < X_Middle_error:
                    #     X_track_PID.SystemOutput = color_x #在屏幕的左侧
                    # else:
                    
                    X_track_PID.SystemOutput = color_x - obj_error #X 因为球要在右足方向上  Because the ball needs to be in the right foot direction
                    
                    
                    X_track_PID.SetStepSignal(X_Middle_error)
                    X_track_PID.SetInertiaTime(0.01, 0.1)               
                    x_real_value = int(X_track_PID.SystemOutput)
                    x_real_value = limit_fun(x_real_value ,-13,13)
                    print(x_real_value)
                    g_dog.move('y',x_real_value)
                    if color_y > 230 or color_y ==0 :
                        g_dog.move('x',0) 
                    else :
                        g_dog.move('x',10) 

                    #停止定点，进行踢球运动 Stop stationary and start playing soccer
                    if color_y > 230 :
                        if abs(color_x -obj_error -160)<8:###6
                            step = step+1
                        else :
                            step = 0
                        if step > 5:
                            g_dog.stop()
                            g_mode = 2 #进入踢球运动 Enter the sport of football
                    elif step >=1 and color_y == 0 :
                        g_dog.stop()
                        g_mode = 2 #进入踢球运动 Enter the sport of football
                else:
                    color_x = 0
                    color_y = 0
                    g_dog.stop()
                
                #print([color_x,color_y])
                cv2.putText(frame, "X:%d, Y%d" % (int(color_x), int(color_y)), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 3)
                t_start = time.time()
                fps = 0

            elif g_mode == 2: #踢球运动  Football sports
                
                g_dog.reset()#恢复动作 recovery actions
                time.sleep(0.2)
                g_dog.translation(['x'],[-10])
                time.sleep(0.5)
                g_dog.attitude(['p'],[0]) 
                time.sleep(0.5)

                g_dog.motor_speed(200) #加快运动速度 Accelerate the speed of movement
                time.sleep(0.2)
                g_dog.motor(four_leg,[7.55, 44.99, 0.85, -49.55, 66.19, 0.36, 8.06, 53.09, 1.34, 9.59, 51.85, 0.36])#收 put away
                time.sleep(0.2)
                g_dog.motor(four_leg,[7.04, 44.99, 0.85, -13.86, 27.53, -15.44, 8.06, 53.72, 1.09, 9.59, 52.47, -0.12])#伸 extend
                time.sleep(0.2)
                g_dog.motor(four_leg,[5.51, 44.36, 2.07, 57.0, -42.31, 5.71, 5.51, 53.72, 2.8, 9.59, 51.22, -1.34])#踢 kick
                time.sleep(0.2)
                g_dog.motor(four_leg,[7.55, 44.99, 0.85, 8.06, 45.61, -0.61, 8.57, 53.72, 1.34, 9.59, 51.85, -0.61])#收回 withdraw
                time.sleep(1)
                                
                '''
                # g_dog.translation(['x'],[0])#恢复追踪目标的姿态 Restore the posture of the tracked target
                # time.sleep(0.2)
                # g_dog.attitude(['p'],[15])
                # time.sleep(0.2)
                # g_dog.translation(['z'],[75])
                # time.sleep(0.2)

                # g_dog.pace('slow') #恢复寻找目标的速度 Restore the speed of searching for targets
                # time.sleep(0.2)
                '''
                
                g_dog.reset()
                time.sleep(0.5)
                cap.release()
                cv2.destroyAllWindows() 
                break #程序结束 END

            else:
                fps = fps + 1
                mfps = fps / (time.time() - t_start)
                cv2.putText(frame, "FPS " + str(int(mfps)), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 3)

            
            img = frame
            if mode==1:
                cv2.rectangle(img, (290, 10), (320, 40), red, -1)
            elif mode==2:
                cv2.rectangle(img, (290, 10), (320, 40), green, -1)
            elif mode==3:
                cv2.rectangle(img, (290, 10), (320, 40), blue, -1)
            elif mode==4:
                cv2.rectangle(img, (290, 10), (320, 40), yellow, -1)
            
            framecv = img #这里可以resize
            #显示到电脑上 Display on computer
            
            fps_time+=1
            if fps_time%2==0:
                cv2.imshow("frame",framecv)
                fps_time=0
            
            if (cv2.waitKey(1)) == ord('q'):
                g_dog.stop()
                g_dog.reset()
                cap.release()
                cv2.destroyAllWindows() 
                break

    except:
        g_dog.reset()
        cap.release()
        cv2.destroyAllWindows() 
        

# play_football_color('yellow')


