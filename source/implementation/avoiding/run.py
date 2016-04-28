# -*- coding: utf-8 -*-
import numpy as np
import cv2
from matplotlib import pyplot as plt

import rectify as re
import sys
sys.path.append("../../config")
sys.path.append("../../component")
import common as common_config
import move.move as mv

maxDepth = common_config.MAXDEPTH
minDepth = common_config.MINDEPTH
carWidth = common_config.CAR_REAL_WIDTH
capHeight = common_config.BINCAP_REAL_HEIGHT
sleep_time = common_config.SLEEP_TIME
H, W = (common_config.BINCAP_HEIGHT, common_config.BINCAP_WIDTH)


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


def getWinX(Q, X1, X2, Z):
    f = Q[2][3]
    Q_inv = np.linalg.inv(Q)
    objpoints = np.matrix([[X1, X2], [0, 0], [Z, Z], [1, 1]])
    imgpointsmat = Q_inv*f/Z*np.matrix(objpoints)
    imgpoints = imgpointsmat.tolist()
    winX = [int(imgpoints[0][0] if imgpoints[0][0]>0 else 0),
            int(imgpoints[0][1] if imgpoints[0][1]<W else W)]
    return winX


def getWinY(Q, Y1, Y2, Z):
    f = Q[2][3]
    Q_inv = np.linalg.inv(Q)
    objpoints = np.matrix([[0, 0], [Y1, Y2], [Z, Z], [1, 1]])
    imgpointsmat = Q_inv*f/Z*np.matrix(objpoints)
    imgpoints = imgpointsmat.tolist()
    winY = [int(imgpoints[1][0] if imgpoints[1][0]>0 else 0),
            int(imgpoints[1][1] if imgpoints[1][1]<H else H)]
    return winY


def getDisparityValue(Q, depth):
    f = Q[2][3]
    Q_inv = np.linalg.inv(Q)
    objpoints = np.matrix([[0], [0], [depth], [1]])
    imgpointsmat = Q_inv*f/depth*np.matrix(objpoints)
    imgpoints = imgpointsmat.tolist()
    disValue = int(imgpoints[2][0])
    return disValue


def getWidth_px(Q, realWidth, Z):
    winX = getWinX(Q, 0, realWidth, Z)
    width_px = int(winX[1]-winX[0])
    return width_px


def getWinOfLMRZY(Q, Xl1, Xl2, Xm1, Xm2, Xr1, Xr2, Y1, Y2, Z):
    winL = getWinX(Q, Xl1, Xl2, Z)
    winM = getWinX(Q, Xm1, Xm2, Z)
    winR = getWinX(Q, Xr1, Xr2, Z)
    winY = getWinY(Q, Y1, Y2, Z)
    if __name__=='__main__':
        print 'winL:', winL
        print 'winM:', winM
        print 'winR:', winR
        print 'winY:', winY
    return winL, winM, winR, winY


def obstacle(winX, winY, minDisparity,  maxDisparity, disparity):
    X1 = disparity[winY[0]]
    X2 = disparity[winY[1]]
    # print len([i for i in X1 if i<0])/(len(X1)+0.0), len([i for i in X2 if i<0])/(len(X2)+0.0)
    # if len([i for i in X1 if i<0])/(len(X1)+0.0)>0.7:
    #     return 0 # backward
    # if len([i for i in X2 if i<0])/(len(X2)+0.0)>0.7:
    #     return 0 # backward
    X1 = X1[winX[0]:winX[1]]
    X2 = X2[winX[0]:winX[1]]
    obs_size = 0
    for x in X1:
        if x>minDisparity:
            obs_size += 1
            if obs_size>24:
                return 1 # turn
        else:
            obs_size = 0
    obs_size = 0
    for x in X2:
        if x>minDisparity:
            obs_size += 1
            if obs_size>24:
                return 1 # turn
        else:
            obs_size = 0
    return 2 # forward


def turnTo2(winY, minDisparity, disparity):
    X1 = disparity[winY[0]]
    X2 = disparity[winY[1]]
    spaces = [] #记录无障碍空隙，（left,right,width）
    left = 0
    right = 0
    block_px = 0
    i = 0
    while(i<W):
        if X1[i]>minDisparity or X2[i]>minDisparity:
            block_px += 1
            if block_px>5:
                if right-left> 0:
                    spaces.append([left, right, right-left])
                left = i
                right = i
                block_px = 0
            i += 1
        else:
            right = i
            i += 1
    spaces.append([left, right, right-left])
    spaces.pop(0)
    if (spaces[0][1]-spaces[0][0]) >\
            (spaces[len(spaces)-1][1]-spaces[len(spaces)-1][0]):
        return 0 # turn left
    return 1 # turn right'


def turnTo(winY, minDisparity, disparity):
    X1 = disparity[winY[0]]
    X2 = disparity[winY[1]]
    block = []
    for i in range(W):
        if X1[i]>minDisparity:
            block.append(i)
        if X2[i]>minDisparity:
            block.append(i)
    location = np.average(block)
    print location
    if (location>352):
        return 0 # turn left
    return 1 # turn right'

def run():
    # 得到矫正重映射矩阵
    mapx1, mapy1, mapx2, mapy2, Q, roi1, roi2 = re.init()
    # 得到检测到的最大距离对应的视差值
    minDisparity = getDisparityValue(Q, maxDepth)
    # 得到在maxDepth距离下实际车宽在像素图中对应的像素宽度，用于判断可容小车通过的空隙
    car_width_px = getWidth_px(Q, carWidth, maxDepth)
    winY = getWinY(Q, 0, capHeight, maxDepth)
    winX = getWinX(Q, -carWidth/2, carWidth/2, maxDepth)

    cap0 = initCap(0)
    cap1 = initCap(1)
    stereo = re.readyStereoBM(roi1, roi2)

    while True:
        disparity = getDisparity(cap0, cap1, stereo, mapx1, mapy1, mapx2, mapy2)
        orient = obstacle(winX, winY, minDisparity, maxDisparity, disparity)
        # forward
        if orient==2:
            mv.forward(sleep_time)

        # backward
        while orient==0:
            mv.backward(sleep_time)
            disparity = getDisparity(cap0, cap1, stereo, mapx1, mapy1, mapx2, mapy2)
            orient = obstacle(winX, winY, minDisparity, maxDisparity, disparity)
        # turn right or left
        while orient==1:
            turn = turnTo(winY, minDisparity, disparity)
            # turn left
            if turn==0:
                while orient!=2:
                    mv.turn_left(sleep_time)
                    disparity = getDisparity(cap0, cap1, stereo, mapx1, mapy1, mapx2, mapy2)
                    orient = obstacle(winX, winY, minDisparity, maxDisparity, dispa]rity)
            # turn right
            elif turn==1:
                while orient!=2:
                    mv.turn_right(sleep_time)
                    disparity = getDisparity(cap0, cap1, stereo, mapx1, mapy1, mapx2, mapy2)
                    orient = obstacle(winX, winY, minDisparity, maxDisparity, disparity)
        # end
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break

    cv2.destroyAllWindows()
    cap0.release()
    cap1.release()

if __name__ == '__main__':
    run()





