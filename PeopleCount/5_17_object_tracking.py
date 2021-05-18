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

height = 0
width = 0

trackers = []
trackables = {}

file_name = './video/test4.mp4'

# Load Yolo
net = cv2.dnn.readNet("./model/yolov4-tiny.weights", "./cfg/yolov4-tiny.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# initialize Tracker
tracker = Tracker()


vs = cv2.VideoCapture('v4l2src device=/dev/video0 ! video/x-raw, format=YUY2, framerate=30/1, width=640, height=480 ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
# vs = cv2.VideoCapture(file_name)
# loop over the frames from the video stream
############################################################
fc = 20.0
count = 0

codec = cv2.VideoWriter_fourcc(*"mp4v")
writing_video_dir="writing_video"
receive_video_dir="receive_video"

record_flag = False
init_flag = False
startTime=None
out = None

############################################################
os.system(f"rm {writing_video_dir}/*")

while True:

        ret, frame = vs.read()

        if frame is None:
            print('### No more frame ###')
            break
        # Start time capture
        start_time = time.time()
        frame_count += 1

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
                #label = '{:,.2%}'.format(confidences[i])
                #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1) # 박스처리해줌.
                #cv2.putText(frame, label, (x + 5, y + 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)

        # use Tracker
        objects = tracker.update(rects)
        total = len(objects)

        # loop over the trackable objects
        # 아디하고 centroid 좌표가 온다.
        # for (objectID, centroid) in objects.items():
        #         # check if a trackable object exists with the object ID
        #         # 트랙킹 되고 있는 알고리즘.
        #         trackable = trackables.get(objectID, None)
        #
        #         # 아디 값 오면 trackable이라는 객체가 생성됨.
        #         if trackable is None:
        #                 trackable = Trackable(objectID, centroid)
        #
        #
        #         # store the trackable object in our dictionary
        #         trackables[objectID] = trackable
        #         text = "ID {}".format(objectID)
        #         cv2.putText(frame, text, (centroid[0] + 10, centroid[1] + 10),
        #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        #         cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

        info = [
            ("total", total),
        ]

        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, height - ((i * 20) + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # show the output frame
        cv2.imshow("Frame", frame)
        frame_time = time.time() - start_time
        print("Frame {} time {}".format(frame_count, frame_time))

        if total >= 1:
            if not record_flag:
                record_flag = True
                startTime=time.time()
                out_video = cv2.VideoWriter(f'{writing_video_dir}/{startTime}.mp4', codec, fc, (640, 480))

            if startTime!=None and record_flag:
                record_time = time.time()-startTime

                if record_time <5:
                    out_video.write(frame)
                else:
                    record_flag=False
                    if record_time > 2:
                        print("Saved")
                        out_video.release()
                        os.system(f"mv {writing_video_dir}/* {receive_video_dir}/")
                    else:
                        os.system(f"rm {writing_video_dir}/*")

        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break

vs.release()
out_video.release()
cv2.destroyAllWindows()
os.system(f"rm {writing_video_dir}/*")
