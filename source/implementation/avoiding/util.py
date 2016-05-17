# -*- coding: utf-8 -*-
import time

import numpy as np
import cv2

import sys
sys.path.append("../../config")
import common as common_config
import rectify
import stereomatch as sm
BINIMG_H, BINIMG_W = (common_config.BINIMG_HEIGHT, common_config.BINIMG_WIDTH)
maxDepth = common_config.MAXDEPTH
minDepth = common_config.MINDEPTH
carWidth = common_config.CAR_REAL_WIDTH
capHeight = common_config.BINCAP_REAL_HEIGHT
sleep_time = common_config.SLEEP_TIME

    
def getWinX(Q, X1, X2, Z):
    f = Q[2][3]
    Q_inv = np.linalg.inv(Q)
    objpoints = np.matrix([[X1, X2], [0, 0], [Z, Z], [1, 1]])
    imgpointsmat = Q_inv*f/Z*np.matrix(objpoints)
    imgpoints = imgpointsmat.tolist()
    winX = [int(imgpoints[0][0] if imgpoints[0][0]>0 else 0),
            int(imgpoints[0][1] if imgpoints[0][1]<BINIMG_W else BINIMG_W)]
    return winX


def getWinY(Q, Y1, Y2, Z):
    f = Q[2][3]
    Q_inv = np.linalg.inv(Q)
    objpoints = np.matrix([[0, 0], [Y1, Y2], [Z, Z], [1, 1]])
    imgpointsmat = Q_inv*f/Z*np.matrix(objpoints)
    imgpoints = imgpointsmat.tolist()
    winY = [int(imgpoints[1][0] if imgpoints[1][0]>0 else 0),
            int(imgpoints[1][1] if imgpoints[1][1]<BINIMG_H*3/4 else BINIMG_H*3/4)]
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


mapx1, mapy1, mapx2, mapy2, Q, roi1, roi2 = rectify.init()
# 得到检测到的最大距离对应的视差值
minDisparity = getDisparityValue(Q, maxDepth)
maxDisparity = getDisparityValue(Q, minDepth)
# 得到在maxDepth距离下实际车宽在像素图中对应的像素宽度，用于判断可容小车通过的空隙
car_width_px = getWidth_px(Q, carWidth, maxDepth)
winY = getWinY(Q, 0, capHeight, maxDepth)
winX = getWinX(Q, -carWidth/2, carWidth/2, maxDepth)
stereo = sm.readyStereoBM(roi1, roi2)
print 'Q:\n'.ljust(13), Q
print 'minDisparity:\n'.ljust(13), minDisparity
print 'maxDisparity:\n'.ljust(13), maxDisparity
print 'car_width_px:\n'.ljust(13), car_width_px
print 'winY:\n'.ljust(13), winY
print 'winX:\n'.ljust(13), winX


def getDisparity(img1, img2):
    return sm.getDisparity(stereo, img1, img2, mapx1, mapy1, mapx2, mapy2)


def obstacle(disparity):
    X1 = disparity[winY[0]]
    X2 = disparity[winY[1]]
    X1 = X1[winX[0]:winX[1]]
    X2 = X2[winX[0]:winX[1]]
    obs_size = 0
    for x in X1:
        if x>maxDisparity:
            obs_size += 1
            if obs_size>24:
                return 0 # backward
        else:
            obs_size = 0
    obs_size = 0
    for x in X2:
        if x>maxDisparity:
            obs_size += 1
            if obs_size>24:
                return 0 # backward
        else:
            obs_size = 0
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


def turnTo(disparity):
    X1 = disparity[winY[0]]
    X2 = disparity[winY[1]]
    block = [i for i in range(len(X1)) if X1[i]>minDisparity] + \
            [i for i in range(len(X2)) if X2[i]>minDisparity]
    location = np.average(block)
    if (location>400):
        return 3 # turn left
    return 4 # turn right'


def getOriention(disparity):
    orient = obstacle(disparity)
    if orient == 0 or orient == 2:
        return orient
    return turnTo(disparity)


def hasRoad(img):
    S = img.shape[0]*img.shape[1]+0.0
    S1 = len([i for i in np.reshape(img, S) if i>254])
    if S1/S > 0.02:
        return True
    return False


if __name__ == '__main__':
    BINCAP_H, BINCAP_W = (common_config.BINCAP_HEIGHT, common_config.BINCAP_WIDTH)
    capL = cv2.VideoCapture(1)
    capL.set(cv2.CAP_PROP_FRAME_WIDTH, BINCAP_W)
    capL.set(cv2.CAP_PROP_FRAME_HEIGHT, BINCAP_H)
    capR = cv2.VideoCapture(0)
    capR.set(cv2.CAP_PROP_FRAME_WIDTH, BINCAP_W)
    capR.set(cv2.CAP_PROP_FRAME_HEIGHT, BINCAP_H)
    while True:
        retL, frameL = capL.read()
        retR, frameR = capR.read()
        imgL = cv2.resize(frameL, (BINIMG_W, BINIMG_H), interpolation=cv2.INTER_LINEAR)
        imgR = cv2.resize(frameR, (BINIMG_W, BINIMG_H), interpolation=cv2.INTER_LINEAR)
        disparity = getDisparity(imgL, imgR)
        cv2.imshow('disparity', np.uint8(disparity))
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
        orient = obstacle(disparity)
        if orient == 2:
            print 'forward'
            continue

        while orient is not 1 and orient is not 2:
            print 'backward'
            retL, frameL = capL.read()
            retR, frameR = capR.read()
            imgL = cv2.resize(frameL, (BINIMG_W, BINIMG_H), interpolation=cv2.INTER_LINEAR)
            imgR = cv2.resize(frameR, (BINIMG_W, BINIMG_H), interpolation=cv2.INTER_LINEAR)
            disparity = getDisparity(imgL, imgR)
            cv2.imshow('disparity', np.uint8(disparity))
            if cv2.waitKey(1) & 0xFF==ord('q'):
                exit()
            orient = obstacle(disparity)

        while orient==1:
            turn = turnTo(disparity)
            # turn left
            if turn==3:
                while orient is not 0 and orient is not 2:
                    print 'turn left'
                    retL, frameL = capL.read()
                    retR, frameR = capR.read()
                    imgL = cv2.resize(frameL, (BINIMG_W, BINIMG_H), interpolation=cv2.INTER_LINEAR)
                    imgR = cv2.resize(frameR, (BINIMG_W, BINIMG_H), interpolation=cv2.INTER_LINEAR)
                    disparity = getDisparity(imgL, imgR)
                    cv2.imshow('disparity', np.uint8(disparity))
                    if cv2.waitKey(1) & 0xFF==ord('q'):
                        exit()
                    orient = obstacle(disparity)
            # turn right
            elif turn==4:
                while orient is not 0 and orient is not 2:
                    print 'turn right'
                    retL, frameL = capL.read()
                    retR, frameR = capR.read()
                    imgL = cv2.resize(frameL, (BINIMG_W, BINIMG_H), interpolation=cv2.INTER_LINEAR)
                    imgR = cv2.resize(frameR, (BINIMG_W, BINIMG_H), interpolation=cv2.INTER_LINEAR)
                    disparity = getDisparity(imgL, imgR)
                    cv2.imshow('disparity', np.uint8(disparity))
                    if cv2.waitKey(1) & 0xFF==ord('q'):
                        exit()
                    orient = obstacle(disparity)
        # end
    capL.release()
    capR.release()
    cv2.destroyAllWindows()










