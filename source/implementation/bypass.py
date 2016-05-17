# -*- coding: UTF-8 -*-
'''
Bypass the obstacles
~~~~~~~~

'''

## Library
# Standard library
import time
import sys
from threading import Thread

# Third party library
import numpy as np
import cv2

# my library
sys.path.append("../config")
sys.path.append("../component")
sys.path.append("./avoiding")
import move
import image_preprocess as imgprocess
import common as common_config
import avoid_client
import util

# get all the captures
path_cap = cv2.VideoCapture(0)

# global variables -- frames
path_ret, path_frame = path_cap.read()

def process_img(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = imgprocess.imageDW(gray,(common_config.CAP_HEIGHT,common_config.CAP_WIDTH),1)
    new_img = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i][j] = 0 if img[i][j] < THRESHOLD else 255
    new_img = new_img.ravel()
    new_img = [y/255.0 for y in new_img]
    new_img = np.reshape(new_img, (common_config.NETWORK_INPUT_SIZE, 1))
    return new_img

def bypass(path_cap, path_frame):
    # do not need to get frame by read function.
    # Directly use global variables
    global path_frame

    ###### Prepare #########
    avoid_client.init(capL_id=2, capR_id=1)

    # get direction
    direction = avoid_client.getOrient()
    first_dir = direction ''' first direction. important variable'''

    # 先离开障碍物面前
    while direction is not 2:
        if first_dir is 3:
            # 左转，前进，右转
            mo.turn_left(common_config.SLEEP_TIME)
            mo.forward(common_config.SLEEP_TIME)
            mo.turn_right(common_config.SLEEP_TIME)
        elif first_dir is 4:
            mo.turn_right(common_config.SLEEP_TIME)
            mo.forward(common_config.SLEEP_TIME)
            mo.turn_left(common_config.SLEEP_TIME)
        direction = avoid_client.getOrient()

    # 试探性地前进
    flag = False
    while(!util.hasRoad(process_img(path_frame))): #在没找到地上的路之前
        if first_dir is 3:
            mo.turn_right(common_config.SLEEP_TIME) if flag is False
            direction = avoid_client.getOrient()
            if direction is not 2:
                mo.turn_left(common_config.SLEEP_TIME)
                mo.forward(common_config.SLEEP_TIME)
                flag = False
            else:
                mo.forward(common_config.SLEEP_TIME)
                flag = True
        elif first_dir is 4:
            mo.turn_left(common_config.SLEEP_TIME) if flag is False
            direction = avoid_client.getOrient()
            if direction is not 2:
                mo.turn_right(common_config.SLEEP_TIME)
                mo.forward(common_config.SLEEP_TIME)
                flag = False
            else:
                mo.forward(common_config.SLEEP_TIME)
                flag = True

    # 找到路之后，往回转一下即可
    mo.turn_left(common_config.SLEEP_TIME) if first_dir is 3
    mo.turn_right(common_config.SLEEP_TIME) if first_dir is 4

if __name__ == '__main__':
    mo = move.Move()
    tr = GetFrameThread()
    tr.start()

    bypass(path_cap, path_frame)

    tr.stop()

