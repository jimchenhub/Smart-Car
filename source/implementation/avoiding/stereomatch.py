# -*- coding: utf-8 -*-
import numpy as np
import cv2

import sys
sys.path.append("../../config")
import common as common_config


criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-5)
BINIMG_H, BINIMG_W = (common_config.BINIMG_HEIGHT, common_config.BINIMG_WIDTH)


def readyStereoBM(roi1, roi2):
    stereobm = cv2.StereoBM_create(numDisparities=112, blockSize=31)
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


def getDisparity(stereo, img1, img2, mapx1, mapy1, mapx2, mapy2):
    dst1 = cv2.remap(img1, mapx1, mapy1, cv2.INTER_LINEAR)
    dst2 = cv2.remap(img2, mapx2, mapy2, cv2.INTER_LINEAR)
    gray1 = cv2.cvtColor(dst1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(dst2, cv2.COLOR_BGR2GRAY)
    disparity = stereo.compute(gray1, gray2)/16
    # disparity = cv2.medianBlur(disparity, 5)
    return disparity



if __name__ == '__main__':
    import rectify as re
    mapx1, mapy1, mapx2, mapy2, Q, roi1, roi2= re.init()
    stereo = readyStereoBM(roi1, roi2)
    img1 = cv2.imread('data/img0/1.jpg')
    img2 = cv2.imread('data/img1/1.jpg')
    img1 = cv2.resize(img1, (BINIMG_W, BINIMG_H), interpolation=cv2.INTER_CUBIC)
    img2 = cv2.resize(img2, (BINIMG_W, BINIMG_H), interpolation=cv2.INTER_CUBIC)
    disparity = getDisparity(stereo, img1, img2, mapx1, mapy1, mapx2, mapy2)
    disparity = cv2.medianBlur(disparity, 5)
    cv2.imshow('disparity', np.uint8(disparity))
    cv2.waitKey(0)
    cv2.destroyAllWindows()


