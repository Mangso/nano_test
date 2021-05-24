from tracking import Tracker, Trackable
import cv2
import numpy as np
import time
import os
import threading

from threading import Thread
import cv2, time

frame_size = 416
frame_count = 0
min_confidence = 0.5
font=cv2.FONT_HERSHEY_SIMPLEX

height = 0
width = 0
fpsFilt=0

trackers = []
trackables = {}

net = cv2.dnn.readNet("./model/yolov4-tiny.weights", "./cfg/yolov4-tiny.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)



############################################################



frame_count = 0

while True:
    
    file_list = os.listdir('./receive_video')
    
    vs = 
    while True:

            ret, frame = vs.read()
            
            
            if frame_count == 0:
                # Start time capture

                (height, width) = frame.shape[:2]

                # draw a horizontal line in the center of the frame

                # construct a blob for YOLO model
                blob = cv2.dnn.blobFromImage(frame, 0.00392, (frame_size, frame_size), (0, 0, 0), True, crop=False)
                net.setInput(blob)
                outs = net.forward(output_layers) # object detection 나옴.
                rects = []

                confidences = []
                boxes = []

                # 사람일수도, 물체일수도.
                for out in outs:
                    for detection in out:
                        scores = detection[5:]
                        class_id = np.argmax(scores) # 제일 높은 값을 찾음!!!
                        confidence = scores[class_id] # 그 확률값이 얼마나.
                        # Filter only 'person'
                        if class_id == 0 and confidence > min_confidence:
                            yolo_flag = True
                            break


                
                
            cv2.imshow("frame",frame)



            frame_count += 1
            key = cv2.waitKey(1) & 0xFF
            
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                    break

vs.release()
out_video.release()
cv2.destroyAllWindows()
os.system(f"rm {writing_video_dir}/*")
