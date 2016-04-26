# -*- coding: utf-8 -*-
import numpy as np
import cv2
from matplotlib import pyplot as plt

import doXML
import sys
sys.path.append("../config")
import common as common_config

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-5)
H, W = (common_config.BINCAP_HEIGHT, common_config.BINCAP_WIDTH)

def rectify(mtx1, dist1, mtx2, dist2, R, T):
    # R：行对准的矫正旋转矩阵；P：3*4的左右投影方程；Q：4*4的重投影矩阵
    R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(
        mtx1, dist1, mtx2, dist2, (W, H), R, T, flags=cv2.CALIB_ZERO_DISPARITY, alpha=-1, newImageSize=(W, H))
    printMat(R1, R2, P1, P2, Q, roi1, roi2)
    # 产生校正图像所需的变换参数（mapx, mapy）
    mapx1, mapy1 = cv2.initUndistortRectifyMap(mtx1, dist1, R1, P1, (W, H), cv2.CV_16SC2)
    mapx2, mapy2 = cv2.initUndistortRectifyMap(mtx2, dist2, R2, P2, (W, H), cv2.CV_16SC2)
    return mapx1, mapy1, mapx2, mapy2, Q


def init():
    initdict = doXML.parseXML('data\\init.xml')
    ret = initdict['ret']
    mtx1 = initdict['mtx1']
    dist1 = initdict['dist1']
    mtx2 = initdict['mtx2']
    dist2 = initdict['dist2']
    R = initdict['R']
    T = initdict['T']
    E = initdict['E']
    F = initdict['F']
    mapx1, mapy1, mapx2, mapy2, Q = rectify(mtx1, dist1, mtx2, dist2, R, T)
    return mapx1, mapy1, mapx2, mapy2, Q


def readyStereoBM():
    stereobm = cv2.StereoBM_create(numDisparities=128, blockSize=31)
    stereobm.setPreFilterSize(31)#41
    stereobm.setPreFilterType(cv2.STEREO_BM_PREFILTER_NORMALIZED_RESPONSE)
    stereobm.setPreFilterCap(31)
    stereobm.setTextureThreshold(10)
    stereobm.setMinDisparity(0)
    stereobm.setSpeckleWindowSize(100)
    stereobm.setSpeckleRange(64)
    stereobm.setUniquenessRatio(0)
    return stereobm


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


def obstacle(winX, winY, minDisparity, disparity):
    X1 = disparity[winY[0]]
    X2 = disparity[winY[1]]
    print len([i for i in X1 if i<0])/(len(X1)+0.0), len([i for i in X2 if i<0])/(len(X2)+0.0)
    if len([i for i in X1 if i<0])/(len(X1)+0.0)>0.7:
        return 0 # backward
    if len([i for i in X2 if i<0])/(len(X2)+0.0)>0.7:
        return 0 # backward
    X1 = X1[winX[0]+10:winX[1]-10]
    X2 = X2[winX[0]+10:winX[1]-10]
    obs_size = 0
    for x in X1:
        if x>minDisparity:
            obs_size += 1
            if obs_size>10:
                return 1 # turn
        else:
            obs_size = 0
    obs_size = 0
    for x in X2:
        if x>minDisparity:
            obs_size += 1
            if obs_size>10:
                return 1 # turn
        else:
            obs_size = 0
    return 2 # forward




def moveTo( width_px, winY, minDisparity, disparity):
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
    # max = 0
    # j = 0
    # for i in range(len(spaces)):
    #     if max < spaces[i][2]:
    #         max = spaces[i][2]
    #         j = i
    # if max > width_px:
    #     x = (spaces[i][0]+spaces[i][1])/2
    #     if x>320 and x<340:
    #         return 'straight'
    if (spaces[0][1]-spaces[0][0]) >\
            (spaces[len(spaces)-1][1]-spaces[len(spaces)-1][0]):
        return 0 # turn left
    return 1 # turn right'


# test function
def imshow():
    plt.subplot(321), plt.imshow(cv2.cvtColor(img1, cv2.COLOR_RGB2BGR))
    plt.subplot(322), plt.imshow(cv2.cvtColor(img2, cv2.COLOR_RGB2BGR))
    plt.subplot(323), plt.imshow(cv2.cvtColor(dst1, cv2.COLOR_RGB2BGR))
    plt.subplot(324), plt.imshow(cv2.cvtColor(dst2, cv2.COLOR_RGB2BGR))
    plt.subplot(325), plt.imshow(disparity, 'gray')
    plt.subplot(326), plt.imshow(disparity1, 'gray')
    # plt.subplot(211), plt.imshow(cv2.cvtColor(dst2, cv2.COLOR_RGB2BGR), 'gray')
    # plt.subplot(212), plt.imshow(disparity, 'gray')
    plt.show()


def printMat(R1, R2, P1, P2, Q, roi1, roi2):
    print 'R1\n', R1
    print 'R2\n', R2
    print 'P1\n', P1
    print 'P2\n', P2
    print 'Q\n', Q
    print 'roi1\n', roi1
    print 'roi2\n', roi2


def test(disparity, _3dImage):
    # print disparity[0][0], _3dImage[0][0]
    # print disparity[479][0], _3dImage[479][0]
    # print disparity[0][639], _3dImage[0][639]
    # print disparity[479][639], _3dImage[479][639]
    print disparity[198][327], _3dImage[198][327]
    print disparity[309][473], _3dImage[309][473]


if __name__ == '__main__':
    # test coding
    maxDepth = common_config.MAXDEPTH
    carWidth = common_config.CAR_REAL_WIDTH
    capHeight = common_config.BINCAP_REAL_HEIGHT

    mapx1, mapy1, mapx2, mapy2, Q = init()
    winY = getWinY(Q, 0, capHeight/2, maxDepth)
    winX = getWinX(Q, -carWidth/2, carWidth/2, maxDepth)
    print winX, winY
    minDisparity = getDisparityValue(Q, maxDepth)
    width_px = getWidth_px(Q, 120, maxDepth)
    stereo = readyStereoBM()

    img1 = cv2.resize(cv2.imread('data\\test\\0x1.jpg'), (W, H), interpolation=cv2.INTER_CUBIC)
    img2 = cv2.resize(cv2.imread('data\\test\\1x1.jpg'), (W, H), interpolation=cv2.INTER_CUBIC)
    dst1 = cv2.remap(img1, mapx1, mapy1, cv2.INTER_LINEAR)
    dst2 = cv2.remap(img2, mapx2, mapy2, cv2.INTER_LINEAR)
    gray1 = cv2.cvtColor(dst1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(dst2, cv2.COLOR_BGR2GRAY)
    disparity = stereo.compute(gray2, gray1)/16
    print haveObstacle(winX, winY, minDisparity, disparity)
    # print moveTo(width_px, winY, minDisparity, disparity)

    disparity = cv2.medianBlur(disparity, 5)
    # cv2.imwrite('disparity.jpg', disparity)
    ret, disparity1 = cv2.threshold(disparity, 30, 255, cv2.THRESH_TOZERO)
    _3dImage = cv2.reprojectImageTo3D(disparity, Q, None, True)
    test(disparity, _3dImage)
    imshow()




