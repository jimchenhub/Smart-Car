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
# import move
# import network
import image_preprocess as imgprocess
import common as common_config
import rectify as re

# get all the captures
path_cap = cv2.VideoCapture(0)
avoiding_left_cap = cv2.VideoCapture(1)
avoiding_right_cap = cv2.VideoCapture(2)

# global variables -- frames
path_ret, path_frame = path_cap.read()
avoiding_left_ret, avoiding_left_frame = avoiding_left_cap.read()
avoiding_right_ret, avoiding_right_frame = avoiding_right_cap.read()

## Get Frame part
#Continually updates the frame
class GetFrameThread(Thread):
    def __init__(self):  
        Thread.__init__(self)
        self.thread_stop = False  
   
    def run(self):
        global path_ret, path_frame
        global avoiding_left_ret, avoiding_left_frame
        global avoiding_right_ret, avoiding_right_frame

        while not self.thread_stop:  
            path_ret, path_frame = path_cap.read()
            avoiding_left_ret, avoiding_left_frame = avoiding_left_cap.read()
            avoiding_right_ret, avoiding_right_frame = avoiding_right_cap.read()

    def stop(self):  
        self.thread_stop = True

tr = GetFrameThread()
tr.start()


def bypass():
    # do not need to get frame by read function.
    # Directly use global variables

    ###### Prepare #########
    # 得到矫正重映射矩阵
    mapx1, mapy1, mapx2, mapy2, Q, roi1, roi2 = re.init()
    # 得到检测到的最大距离对应的视差值
    minDisparity = getDisparityValue(Q, maxDepth)
    # 得到在maxDepth距离下实际车宽在像素图中对应的像素宽度，用于判断可容小车通过的空隙
    car_width_px = getWidth_px(Q, carWidth, maxDepth)
    winY = getWinY(Q, 0, capHeight, maxDepth)
    winX = getWinX(Q, -carWidth/2, carWidth/2, maxDepth)

    stereo = re.readyStereoBM(roi1, roi2)

    disparity = getDisparity(cap0, cap1, stereo, mapx1, mapy1, mapx2, mapy2)
    orient = obstacle(winX, winY, minDisparity, maxDisparity, disparity)


tr.stop()