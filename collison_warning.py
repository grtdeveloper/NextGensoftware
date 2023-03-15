######## Webcam Object Detection Using Tensorflow-trained Classifier #########
#
# Author: Evan Juras
# Date: 10/2/19
# Description: 
# This program uses a TensorFlow Lite model to perform object detection on a
# video. It draws boxes and scores around the objects of interest in each frame
# from the video.
#
# This code is based off the TensorFlow Lite image classification example at:
# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/examples/python/label_image.py
#
# I added my own method of drawing boxes and labels using OpenCV.

# Import packages
import os
import argparse
import cv2  
import numpy as np
import sys
import importlib.util
# from sympy import Point, Polygon
import time
from shapely.geometry import Polygon
# import matplotlib.pyplot as plt
import pygame
import settings
from time import sleep
import socket

MODEL_NAME = './Sample_TFLite_model/'
GRAPH_NAME = 'detect.tflite'
LABELMAP_NAME = 'labelmap.txt'
VIDEO_NAME = './00380017.AVI'
min_conf_threshold = float(0.5)
use_TPU = False
plyOption=""
clicked = False
col_Video=""
host = socket.gethostname()  # as both code is running on same pc
port = 5000  # socket server port number

with open(settings.FILE_PATH_OPTION, 'r') as f:
    plyOption = [line.strip() for line in f.readlines()]

settings.sock_Client = socket.socket()  # instantiate
settings.sock_Client.connect((host, port))  # connect to the server


def client_program(cliSock, message):
    try:
        cliSock.send(message.encode())  # send message
        data = cliSock.recv(100).decode()  # receive response
        print('Received from server: ' + data)  # show in terminal
    except Exception as err:
        print(" Got error in cliSock:", str(err))
        pass

def onMouse(event, x, y, flags, param):
    global clicked
    if event == cv2.EVENT_LBUTTONUP:
        clicked = True

# Import TensorFlow libraries
# If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
# If using Coral Edge TPU, import the load_delegate library
pkg = importlib.util.find_spec('tflite_runtime')
if pkg:
    from tflite_runtime.interpreter import Interpreter
    if use_TPU:
        from tflite_runtime.interpreter import load_delegate
else:
    from tensorflow.lite.python.interpreter import Interpreter
    if use_TPU:
        from tensorflow.lite.python.interpreter import load_delegate

# If using Edge TPU, assign filename for Edge TPU model
if use_TPU:
    # If user has specified the name of the .tflite file, use that name, otherwise use default 'edgetpu.tflite'
    if (GRAPH_NAME == 'detect.tflite'):
        GRAPH_NAME = 'edgetpu.tflite'   

# Get path to current working directory
CWD_PATH = os.getcwd()

# Path to video file
VIDEO_PATH = os.path.join(CWD_PATH,'../',VIDEO_NAME)
print("VIDEO_PATH : ", VIDEO_PATH)

# Output_video_path = os.path.join(CWD_PATH,VIDEO_NAME)

# Path to .tflite file, which contains the model that is used for object detection
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,GRAPH_NAME)

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,MODEL_NAME,LABELMAP_NAME)

# Load the label map
with open(PATH_TO_LABELS, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for label map if using the COCO "starter model" from
# https://www.tensorflow.org/lite/models/object_detection/overview
# First label is '???', which has to be removed.
if labels[0] == '???':
    del(labels[0])

# Load the Tensorflow Lite model.
# If using Edge TPU, use special load_delegate argument
if use_TPU:
    interpreter = Interpreter(model_path=PATH_TO_CKPT,
                              experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    print(PATH_TO_CKPT)
else:
    interpreter = Interpreter(model_path=PATH_TO_CKPT)

interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

# Check output layer name to determine if this model was created with TF2 or TF1,
# because outputs are ordered differently for TF2 and TF1 models
outname = output_details[0]['name']

if ('StatefulPartitionedCall' in outname): # This is a TF2 model
    boxes_idx, classes_idx, scores_idx = 1, 3, 0
else: # This is a TF1 model
    boxes_idx, classes_idx, scores_idx = 0, 1, 2

# Open video file
video=None

if plyOption.lower() == "live":
    video = cv2.VideoCapture(0) 
    print(" video is :", video)
else:
    video = cv2.VideoCapture(VIDEO_PATH)

imW = video.get(cv2.CAP_PROP_FRAME_WIDTH)
imH = video.get(cv2.CAP_PROP_FRAME_HEIGHT)


fourcc = cv2.VideoWriter_fourcc(*'XVID')
result = cv2.VideoWriter("Collision_warning_demo.avi", fourcc, 5, (1920, 1080))

print("I came here ", plyOption)

while(video.isOpened()):
    # tic = time.time() 
    # Acquire frame and resize to expected shape [1xHxWx3]
    ret, frame = video.read()
    frame_num = video.get(cv2.CAP_PROP_POS_FRAMES)
    print(video.get(cv2.CAP_PROP_POS_FRAMES))
    if not ret:
      print('Reached the end of the video!')
      break
    if int(frame_num)%5 == 1:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height))
        input_data = np.expand_dims(frame_resized, axis=0)

        # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
        if floating_model:
            input_data = (np.float32(input_data) - input_mean) / input_std

        # Perform the actual detection by running the model with the image as input
        tic = time.time() 
        interpreter.set_tensor(input_details[0]['index'],input_data)
        interpreter.invoke()
        toc = time.time()
        print(toc-tic, 'seconds')

        # Retrieve detection results
        boxes = interpreter.get_tensor(output_details[boxes_idx]['index'])[0] # Bounding box coordinates of detected objects
        classes = interpreter.get_tensor(output_details[classes_idx]['index'])[0] # Class index of detected objects
        scores = interpreter.get_tensor(output_details[scores_idx]['index'])[0] # Confidence of detected objects
        
        # Plot predicted trajectory (safe zone)
        # p1, p2, p3, p4 = map(Point, [(570, 1074), (856, 758), (1062, 756), (1372, 1078)])
        # poly1 = Polygon(p1, p2, p3, p4) - sympy
        # Singapore data safe zone contours
        # poly1 = Polygon([(570, 1074), (856, 758), (1062, 756), (1372, 1078)])  #shapely
        
        # Delhi night data safe zone contours
        poly1 = Polygon([(850, 1079), (1314, 734), (1456, 738), (1620, 1079)])  #shapely
        # contours = np.array([[570, 1074], [856, 758], [1062, 756], [1372, 1078]])
        
        poly_critical = Polygon([(808, 1079), (1196, 792), (1424, 788), (1422, 1079)])        
        # contours = np.array([[850, 1079], [1314, 734], [1456, 738], [1620, 1079]])
        
        # cv2.fillPoly(frame, pts = [contours], color =(255,255,255))
        # cv2.imshow('Intermediate', cv2.pyrDown(frame))
        
        # Loop over all detections and draw detection box if confidence is above minimum threshold
        for i in range(len(scores)):
            if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0)):

                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1,(boxes[i][0] * imH)))
                xmin = int(max(1,(boxes[i][1] * imW)))
                ymax = int(min(imH,(boxes[i][2] * imH)))
                xmax = int(min(imW,(boxes[i][3] * imW)))
                
                # cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 4)
                
                
                # p5, p6, p7, p8 = map(Point, [(xmin,ymin), (xmin, ymax), (xmax,ymax), (xmax,ymin)])
                # poly2 = Polygon(p5, p6, p7, p8)
                poly2 = Polygon([(xmin,ymin), (xmin, ymax), (xmax,ymax), (xmax,ymin)])
                
                # Find intersection(whether overlapping) ###Yellow
                if poly1.intersects(poly2):
                    cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (0, 255, 255), 4)
                    col_Video=",yellow"
                    pygame.mixer.init()
                    pygame.mixer.music.load("beep-08b.wav")
                    pygame.mixer.music.play()
                    
                if poly_critical.intersects(poly2): ### Red
                    cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (0, 0, 255), 4)
                    col_Video=",red"
                    pygame.mixer.init()
                    pygame.mixer.music.load("beep-09.wav")
                    pygame.mixer.music.play()
  
                # print(isIntersection)
                
                # Draw label
                object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                client_program( settings.sock_Client , object_name + str(col_Video))
                label = '%s: %d%%' % (object_name, int(scores[i]*100)) # Example: 'person: 72%'
                labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
                label_ymin = max(ymin, labelSize[1] + 10) # Make sure not to draw label too close to top of window
                cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin+labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED) # Draw white box to put label text in
                cv2.putText(frame, label, (xmin, label_ymin-7), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2) # Draw label text
                
                # if poly1.intersection(poly2):
                #     print('collision! Alert!')
                    
        # All the results have been drawn on the frame, so it's time to display it.
        if settings.enablebackVideo is False:
            cv2.imshow('Live_Detection', cv2.pyrDown(frame))
            cv2.namedWindow('Live_Detection', cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty('Live_Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        # plt.show()
        
        result.write(frame)
        
        # toc = time.time()
        # print(toc-tic, 'seconds')

        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break
        if cv2.getWindowProperty('just_a_window', cv2.WND_PROP_VISIBLE) > -1 and clicked:
            break

# Clean up
video.release()
settings.sock_Client.close()  # close the connection
result.release()

cv2.destroyAllWindows()


