# -*- coding: utf-8 -*-
import numpy as np
import cv2
from matplotlib import pyplot as plt

import rectify as re
import sys
sys.path.append("../config")
sys.path.append("../component")
import common as common_config
import move.move as mv

maxDepth = common_config.MAXDEPTH
carWidth = common_config.CAR_REAL_WIDTH
capHeight = common_config.BINCAP_REAL_HEIGHT

def initCap(i):
    cap = cv2.VideoCapture(i)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,common_config.BINCAP_WIDTH);
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,common_config.BINCAP_HEIGHT);
    return cap


def getDisparity(cap0, cap1, stereo, mapx1, mapy1, mapx2, mapy2):
    cap0.grab()
    cap1.grab()
    ret, frame1 = cap0.retrieve()
    ret, frame2 = cap1.retrieve()
    dst1 = cv2.remap(frame1, mapx1, mapy1, cv2.INTER_LINEAR)
    dst2 = cv2.remap(frame2, mapx2, mapy2, cv2.INTER_LINEAR)
    gray1 = cv2.cvtColor(dst1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(dst2, cv2.COLOR_BGR2GRAY)
    disparity = stereo.compute(gray2, gray1)/16
    disparity = cv2.medianBlur(disparity, 5)
    return disparity


def run():
    # 得到矫正重映射矩阵
    mapx1, mapy1, mapx2, mapy2, Q = re.init()
    # 得到检测到的最大距离对应的视差值
    minDisparity = re.getDisparityValue(Q, maxDepth)
    # 得到在maxDepth距离下实际车宽在像素图中对应的像素宽度，用于判断可容小车通过的空隙
    car_width_px = re.getWidth_px(Q, carWidth, maxDepth)
    winY = re.getWinY(Q, 0, capHeight, maxDepth)
    winX = re.getWinX(Q, -carWidth/2, carWidth/2, maxDepth)

    cap0 = initCap(0)
    cap1 = initCap(1)
    stereo = re.readyStereoBM()

    while True:
        disparity = getDisparity(cap0, cap1, stereo, mapx1, mapy1, mapx2, mapy2)
        orient = re.obstacle(winX, winY, minDisparity, disparity)
        # forward
        if orient==2:
            mv.forward()
        # backward
        while orient==0:
            mv.backward()
            disparity = getDisparity(cap0, cap1, stereo, mapx1, mapy1, mapx2, mapy2)
            orient = re.obstacle(winX, winY, minDisparity, disparity)

        while orient==1:
            turn = re.obstacle(car_width_px, winY, minDisparity, disparity)
            if turn==0:
                while orient!=2:
                    mv.turn_left()
                    disparity = getDisparity(cap0, cap1, stereo, mapx1, mapy1, mapx2, mapy2)
                    orient = re.obstacle(winX, winY, minDisparity, disparity)
            elif turn==1:
                while orient!=2:
                    mv.turn_right()
                    disparity = getDisparity(cap0, cap1, stereo, mapx1, mapy1, mapx2, mapy2)
                    orient = re.obstacle(winX, winY, minDisparity, disparity)

    cv2.destroyAllWindows()
    cap0.release()
    cap1.release()

if __name__ == '__main__':
    run()





