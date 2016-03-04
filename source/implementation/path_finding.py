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


## Main function
# major variables
cap = cv2.VideoCapture(0)
# mo = move.Move()
net = network.Network([76800, 30, 3])

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # Change frame to gray level image and do some trasition
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = imgprocess.imageDW(gray,gray.shape,4)

    # display image
    cv2.imshow('img',img)

    # decide direction
    #direction = net.feedforward(img)

    # Choose direction or quit
    input_key = cv2.waitKey(1) & 0xFF
    if input_key == ord('q'):
        break
    # if direction == 'w':
    #     mo.forward(common_config.SLEEP_TIME)
    # elif direction == 'a':
    #     mo.turn_left(common_config.SLEEP_TIME)
    # elif direction == 'd':
    #     mo.turn_right(common_config.SLEEP_TIME)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
print "Finish recording"

# shutdown the car
# mo.stop()
# mo.shutdown()
print "Car shutdown"

