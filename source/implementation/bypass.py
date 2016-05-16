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

# get all the captures
path_cap = cv2.VideoCapture(0)

# global variables -- frames
path_ret, path_frame = path_cap.read()

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
    while(True): #在没找到地上的路之前
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
        # 获取地上的路
        # .....

    # 找到路之后，往回转一下即可
    mo.turn_left(common_config.SLEEP_TIME) if first_dir is 3
    mo.turn_right(common_config.SLEEP_TIME) if first_dir is 4

if __name__ == '__main__':
    mo = move.Move()
    tr = GetFrameThread()
    tr.start()

    bypass(path_cap, avoiding_left_cap, avoiding_right_cap, path_frame, avoiding_left_frame, avoiding_right_frame)

    tr.stop()

