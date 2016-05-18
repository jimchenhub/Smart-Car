# -*- coding: UTF-8 -*-
'''
Find Path implementation
~~~~~~~~

第一阶段任务
通过结合move模块完成运动，结合network模块完成方向预测，通过config文件中的权值和偏差来初始化网络
'''

## Library
# Standard library
import time
import sys
from threading import Thread

# Third party library
import numpy as np
import cv2

# my library - configuration
# sys.path.append("/home/pi/Documents/Github/Smart-Car/source/config")
# sys.path.append("/home/pi/Documents/Github/Smart-Car/source/component")
sys.path.append("../config")
sys.path.append("../component")
# import move
import network
import image_preprocess as imgprocess
import common as common_config

THRESHOLD = 220

## Main function
# major variables
cap = cv2.VideoCapture(1)
ret, frame = cap.read()
# mo = move.Move()
net = network.load("../config/result/0316-93%")


## Get Frame part
#Continually updates the frame
class GetFrameThread(Thread):
    def __init__(self):  
        Thread.__init__(self)
        self.thread_stop = False  
   
    def run(self):
        global ret, frame
        while not self.thread_stop:  
            ret, frame = cap.read()

    def stop(self):  
        self.thread_stop = True  

def getFrame():
    global ret, frame
    return ret, frame

tr = GetFrameThread()
tr.start()

## main loop
pre_a = np.ndarray((3,1))
while(cap.isOpened()):
    # Capture frame-by-frame
    # ret, frame = cap.read()
    ret, current_frame = getFrame()

    # Our operations on the frame come here
    # Change frame to gray level image and do some trasition
    gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    img = imgprocess.imageDW(gray,(common_config.CAP_HEIGHT,common_config.CAP_WIDTH),1)
    new_img = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i][j] = 0 if img[i][j] < THRESHOLD else 255
    new_img = new_img.ravel()
    new_img = [y/255.0 for y in new_img]
    new_img = np.reshape(new_img, (common_config.NETWORK_INPUT_SIZE, 1))

    # decide direction
    a = net.feedforward(new_img)
    print a
    if (pre_a == a).all():
        print "Image not change. ignore this turn"
        continue
    pre_a = a.copy()
    direction = np.argmax(a)
    print direction

    # Choose direction or quit
    # input_key = raw_input("move or quit?")
    input_key = 'm'

    if input_key == 'q':
        break
    elif input_key == 'm':
        if direction == 0:
            mo.forward(common_config.SLEEP_TIME)
            print "forward"
        elif direction == 1:
            mo.turn_left(common_config.SLEEP_TIME)
            print "turn left"
        elif direction == 2:
            mo.turn_right(common_config.SLEEP_TIME)
            print "turn right"
    time.sleep(0.1)

# When everything done, release the capture
tr.stop() # stop the thread 

cap.release()
cv2.destroyAllWindows()
print "Finish recording"

# shutdown the car
mo.stop()
mo.shutdown()
print "Car shutdown"

