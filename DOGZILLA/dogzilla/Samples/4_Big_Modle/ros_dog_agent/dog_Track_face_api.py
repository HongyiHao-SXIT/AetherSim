import cv2
import os,socket,sys,time
from DOGZILLALib import DOGZILLA

#-----------------------COMMON INIT-----------------------
import cv2
import mediapipe as mp



def Face_Track():
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils
    g_dog = DOGZILLA()
    cv2.destroyAllWindows() 
    
    # For static images:
    IMAGE_FILES = []
    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
      for idx, file in enumerate(IMAGE_FILES):
        image = cv2.imread(file)
        # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Draw face detections of each face.
        if not results.detections:
          continue
        annotated_image = image.copy()
        for detection in results.detections:
          print('Nose tip:')
          print(mp_face_detection.get_key_point(
              detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
          mp_drawing.draw_detection(annotated_image, detection)
        cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)

    # For webcam input:
    cap=cv2.VideoCapture(0)
    cap.set(3,320)
    cap.set(4,240)

    fps_num = 0

    try:
      with mp_face_detection.FaceDetection(
          model_selection=0, min_detection_confidence=0.5) as face_detection:
        while cap.isOpened():
          success, image = cap.read()
          if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

          # To improve performance, optionally mark the image as not writeable to
          # pass by reference.
          image.flags.writeable = False
          image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
          results = face_detection.process(image)

          # Draw the face detection annotations on the image.
          image.flags.writeable = True
          image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
          if results.detections:
            for detection in results.detections:
              value_x=0
              value_y=0
              mp_drawing.draw_detection(image, detection)
              xy=(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
              face_x=320-xy.x*320
              face_y=xy.y*240
              value_x = face_x - 160
              value_y = face_y - 120
              
              #print(face_x,face_y)
              if value_x > 55:
                value_x = 55
              elif value_x < -55:
                value_x = -55
              if value_y > 75:
                value_y = 75
              elif value_y < -75:
                value_y = -75
                
          else:
            value_x=value_y=face_x=face_y=0
            

          #print(['y','p'],[value_x/9, value_y/8])
          g_dog.attitude(['y','p'],[value_x/9, value_y/8])
          
        
          fps_num +=1
          
          if fps_num%2 == 0:
            #显示在屏幕上
            cv2.imshow("image1",image)
            fps_num =0

          # Flip the image horizontally for a selfie-view display.
          #cv2.imshow('MediaPipe Face Detection', cv2.flip(image, 1))
          if cv2.waitKey(5) == ord('q'):
            g_dog.reset()
            cap.release()
            cv2.destroyAllWindows() 
            break
        
    except:    
      cv2.destroyAllWindows() 
      cap.release()
      g_dog.reset()
    
