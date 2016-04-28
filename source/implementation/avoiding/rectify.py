# -*- coding: utf-8 -*-
import numpy as np
import cv2
from matplotlib import pyplot as plt

import doXML
import sys
sys.path.append("../../config")
import common as common_config

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-5)
H, W = (common_config.BINCAP_HEIGHT, common_config.BINCAP_WIDTH)

def rectify(mtx1, dist1, mtx2, dist2, R, T):
    # R：行对准的矫正旋转矩阵；P：3*4的左右投影方程；Q：4*4的重投影矩阵
    R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(
        mtx1, dist1, mtx2, dist2, (W, H), R, T, flags=cv2.CALIB_ZERO_DISPARITY, alpha=-1, newImageSize=(W, H))
    if __name__ == '__main__':
        printMat(R1, R2, P1, P2, Q, roi1, roi2)
    # 产生校正图像所需的变换参数（mapx, mapy）
    mapx1, mapy1 = cv2.initUndistortRectifyMap(mtx1, dist1, R1, P1, (W, H), cv2.CV_16SC2)
    mapx2, mapy2 = cv2.initUndistortRectifyMap(mtx2, dist2, R2, P2, (W, H), cv2.CV_16SC2)
    return mapx1, mapy1, mapx2, mapy2, Q, roi1, roi2


def init():
    initdict = doXML.parseXML('data/init.xml')
    ret = initdict['ret']
    mtx1 = initdict['mtx1']
    dist1 = initdict['dist1']
    mtx2 = initdict['mtx2']
    dist2 = initdict['dist2']
    R = initdict['R']
    T = initdict['T']
    E = initdict['E']
    F = initdict['F']
    mapx1, mapy1, mapx2, mapy2, Q, roi1, roi2 = rectify(mtx1, dist1, mtx2, dist2, R, T)
    return mapx1, mapy1, mapx2, mapy2, Q, roi1, roi2


def readyStereoBM(roi1, roi2):
    stereobm = cv2.StereoBM_create(numDisparities=128, blockSize=31)
    stereobm.setPreFilterSize(31)#41
    stereobm.setPreFilterType(cv2.STEREO_BM_PREFILTER_NORMALIZED_RESPONSE)
    stereobm.setPreFilterCap(31)
    stereobm.setTextureThreshold(10)
    stereobm.setMinDisparity(0)
    stereobm.setSpeckleWindowSize(100)
    stereobm.setSpeckleRange(64)
    stereobm.setUniquenessRatio(0)
    stereobm.setROI1(roi1)
    stereobm.setROI1(roi2)
    return stereobm


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
    import glob
    def getDisparityFromCap(cap0, cap1, stereo, mapx1, mapy1, mapx2, mapy2):
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


    def getDisparityFromImg(img1, img2, stereo, mapx1, mapy1, mapx2, mapy2):
        dst1 = cv2.remap(img1, mapx1, mapy1, cv2.INTER_LINEAR)
        dst2 = cv2.remap(img2, mapx2, mapy2, cv2.INTER_LINEAR)
        gray1 = cv2.cvtColor(dst1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(dst2, cv2.COLOR_BGR2GRAY)
        disparity = stereo.compute(gray2, gray1)/16
        disparity = cv2.medianBlur(disparity, 5)
        return disparity


    mapx1, mapy1, mapx2, mapy2, Q, roi1, roi2= init()
    stereo = readyStereoBM(roi1, roi2)
    selector = input('1(img) or 2(cap):')
    if selector == '2':
        cap1 = cv2.VideoCapture(0)
        cap1.set(cv2.CAP_PROP_FRAME_WIDTH,common_config.BINCAP_WIDTH);
        cap1.set(cv2.CAP_PROP_FRAME_HEIGHT,common_config.BINCAP_HEIGHT);
        cap2 = cv2.VideoCapture(1)
        cap2.set(cv2.CAP_PROP_FRAME_WIDTH,common_config.BINCAP_WIDTH);
        cap2.set(cv2.CAP_PROP_FRAME_HEIGHT,common_config.BINCAP_HEIGHT);
        while True:
            disparity = getDisparityFromCap(cap1, cap2, stereo, mapx1, mapy1, mapx2, mapy2)
            disparity[disparity<0] = 0
            # img1 = cv2.resize(cv2.imread('data/test/0x1.jpg'), (W, H), interpolation=cv2.INTER_CUBIC)
            # img2 = cv2.resize(cv2.imread('data/test/1x1.jpg'), (W, H), interpolation=cv2.INTER_CUBIC)
            disparity = cv2.medianBlur(disparity, 5)
            # ret, disparity1 = cv2.threshold(disparity, 30, 255, cv2.THRESH_TOZERO)
            _3dImage = cv2.reprojectImageTo3D(disparity, Q, None, True)
            test(disparity, _3dImage)
            # imshow()
            cv2.imshow('disparity', np.int8(disparity))
            if cv2.waitKey(1) & 0xFF==ord('q'):
                break
    else:
        imgs1 = glob.glob('data/test0/*.jpg')
        imgs2 = glob.glob('data/test1/*.jpg')
        i = 1
        for (fname1,fname2) in zip(imgs1,imgs2):
            img1 = cv2.resize(cv2.imread(fname1), (W, H), interpolation=cv2.INTER_CUBIC)
            img2 = cv2.resize(cv2.imread(fname2), (W, H), interpolation=cv2.INTER_CUBIC)
            disparity = getDisparityFromImg(img1, img2, stereo, mapx1, mapy1, mapx2, mapy2)
            disparity[disparity<0] = 0
            # img1 = cv2.resize(cv2.imread('data/test/0x1.jpg'), (W, H), interpolation=cv2.INTER_CUBIC)
            # img2 = cv2.resize(cv2.imread('data/test/1x1.jpg'), (W, H), interpolation=cv2.INTER_CUBIC)
            disparity = cv2.medianBlur(disparity, 5)
            # ret, disparity1 = cv2.threshold(disparity, 30, 255, cv2.THRESH_TOZERO)
            _3dImage = cv2.reprojectImageTo3D(disparity, Q, None, True)
            test(disparity, _3dImage)
            # imshow()
            plt.subplot(1, len(imgs1), i), plt.imshow(disparity, 'gray')
            i += 1
        plt.show()


