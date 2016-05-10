# -*- coding: utf-8 -*-
import numpy as np
import cv2

import doXML
import sys
sys.path.append("../../config")
import common as common_config

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-5)
BINIMG_H, BINIMG_W = (common_config.BINIMG_HEIGHT, common_config.BINIMG_WIDTH)


def rectify(mtx1, dist1, mtx2, dist2, R, T):
    # R：行对准的矫正旋转矩阵；P：3*4的左右投影方程；Q：4*4的重投影矩阵
    R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(
        mtx1, dist1,
        mtx2, dist2,
        (BINIMG_W, BINIMG_H),
        R,
        T,
        flags=cv2.CALIB_ZERO_DISPARITY,
        alpha=-1,
        newImageSize=(BINIMG_W, BINIMG_H)
    )
    if __name__ == '__main__':
        printMat(R1, R2, P1, P2, Q, roi1, roi2)
    # 产生校正图像所需的变换参数（mapx, mapy）
    mapx1, mapy1 = cv2.initUndistortRectifyMap(
        mtx1, dist1,
        R1, P1,
        (BINIMG_W, BINIMG_H),
        cv2.CV_16SC2
    )
    mapx2, mapy2 = cv2.initUndistortRectifyMap(
        mtx2, dist2,
        R2, P2,
        (BINIMG_W, BINIMG_H),
        cv2.CV_16SC2
    )
    return mapx1, mapy1, mapx2, mapy2, Q, roi1, roi2


def init():
    initdict = doXML.parseXML('data/init.xml')
    mtx1 = initdict['mtx1']
    dist1 = initdict['dist1']
    mtx2 = initdict['mtx2']
    dist2 = initdict['dist2']
    R = initdict['R']
    T = initdict['T']
    mapx1, mapy1, mapx2, mapy2, Q, roi1, roi2 = rectify(mtx1, dist1, mtx2, dist2, R, T)
    return mapx1, mapy1, mapx2, mapy2, Q, roi1, roi2


# test function
def printMat(R1, R2, P1, P2, Q, roi1, roi2):
    print 'R1\n', R1
    print 'R2\n', R2
    print 'P1\n', P1
    print 'P2\n', P2
    print 'Q\n', Q
    print 'roi1\n', roi1
    print 'roi2\n', roi2


if __name__ == '__main__':
    mapx1, mapy1, mapx2, mapy2, Q, roi1, roi2= init()
    frame1 = cv2.imread('data/img0/1.jpg')
    frame2 = cv2.imread('data/img1/1.jpg')
    frame1 = cv2.resize(frame1, (BINIMG_W, BINIMG_H), interpolation=cv2.INTER_CUBIC)
    frame2 = cv2.resize(frame2, (BINIMG_W, BINIMG_H), interpolation=cv2.INTER_CUBIC)
    dst1 = cv2.remap(frame1, mapx1, mapy1, cv2.INTER_LINEAR)
    dst2 = cv2.remap(frame2, mapx2, mapy2, cv2.INTER_LINEAR)
    cv2.imshow('rectified1', dst1)
    cv2.imshow('rectified2', dst2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


