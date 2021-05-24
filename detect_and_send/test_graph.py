import cv2
import numpy as np
import time
import os
import threading

frame_size = 416
frame_count = 0
min_confidence = 0.5
font=cv2.FONT_HERSHEY_SIMPLEX

height = 0
width = 0
fpsFilt=0

trackers = []
trackables = {}

# Load Yolo
net = cv2.dnn.readNet("./model/yolov4-tiny.weights", "./cfg/yolov4-tiny.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

abnormal_path = '../PeopleCount/abnormal/'
normal_path = '../PeopleCount/normal/'
abnormal_filelist = os.listdir(abnormal_path)
normal_filelist =  os.listdir(normal_path)

number = 1

for file_name in abnormal_filelist:

    cap=cv2.VideoCapture(abnormal_path+file_name)
    ret,frame= cap.read()


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

                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2) # 시작점의 x
                y = int(center_y - h / 2) # 시작점의 y

                boxes.append([x, y, w, h]) # 배열로 계속 넣어줌.

                confidences.append(float(confidence))

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, min_confidence, 0.4)
    # 박스 중복을 줄여주는 거.
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            rects.append([x, y, x+w, y+h]) # 이 박스안에 중복된 내용이 있을수도 없을수도.
            label = '{:,.2%}'.format(confidences[i])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1) # 박스처리해줌.
            cv2.putText(frame, label, (x + 5, y + 15), cv2.FONT_HERSHEY_PLAIN, 1, (255,0 , 0), 1)
    
    print(file_name, max(confidences))

   
    
    cv2.imwrite("./first_frame/Frame_%d.jpg" % number, frame)
    number += 1
        
