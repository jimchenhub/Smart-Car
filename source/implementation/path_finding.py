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

THRESHOLD = 220

## Main function
# major variables
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FPS, 60) # sety fps
# mo = move.Move()
net = network.load("../config/result/0316-93%")

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # Change frame to gray level image and do some trasition
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = imgprocess.imageDW(gray,(common_config.CAP_HEIGHT,common_config.CAP_WIDTH),1)
    new_img = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i][j] = 0 if img[i][j] < THRESHOLD else 255
    new_img = new_img.ravel()
    new_img = [y/255.0 for y in new_img]
    new_img = np.reshape(new_img, (common_config.NETWORK_INPUT_SIZE, 1))

    # decide direction
    direction = np.argmax(net.feedforward(new_img))

    # Choose direction or quit
    input_key = cv2.waitKey(0) & 0xFF
    if input_key == ord('q'):
        break
    if direction == 0:
        mo.forward(common_config.SLEEP_TIME)
        print "forward"
    elif direction == 1:
        mo.turn_left(common_config.SLEEP_TIME)
        print "turn left"
    elif direction == 2:
        mo.turn_right(common_config.SLEEP_TIME)
        print "turn right"

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
print "Finish recording"

# shutdown the car
mo.stop()
mo.shutdown()
print "Car shutdown"

