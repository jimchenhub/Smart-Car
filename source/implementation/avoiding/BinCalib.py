# -*- coding: utf-8 -*-
import numpy as np
import cv2
import glob
from matplotlib import pyplot as plt

import doXML
import sys
sys.path.append("../../config")
import common as common_config

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-5)
H, W = (common_config.BINCAP_HEIGHT, common_config.BINCAP_WIDTH)
def bincalib():
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)*30
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints1 = [] # 2d points in image plane.
    imgpoints2 = [] # 2d points in image plane.
    images1 = glob.glob('data/img0/*.jpg')
    images2 = glob.glob('data/img1/*.jpg')
    for (fname1, fname2) in zip(images1,images2):
        img1 = cv2.resize(cv2.imread(fname1), (W, H), interpolation=cv2.INTER_CUBIC)
        img2 = cv2.resize(cv2.imread(fname2), (W, H), interpolation=cv2.INTER_CUBIC)
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        # ret, gray1=cv2.threshold(gray1,50,255,cv2.THRESH_BINARY)
        # ret, gray2=cv2.threshold(gray2,50,255,cv2.THRESH_BINARY)
        # Find the chess board corners
        ret1, corners1 = cv2.findChessboardCorners(gray1, (7, 6), None)
        ret2, corners2 = cv2.findChessboardCorners(gray2, (7, 6), None)
        # If found, add object points, image points (after refining them)
        print ret1 & ret2
        if ret1==True and ret2==True:
            objpoints.append(objp)
            corners21 = cv2.cornerSubPix(gray1, corners1, (11,11), (-1,-1), criteria)
            corners22 = cv2.cornerSubPix(gray2, corners2, (11,11), (-1,-1), criteria)
            imgpoints1.append(corners21)
            imgpoints2.append(corners22)
            # img = cv2.drawChessboardCorners(img1, (7,6), corners21, ret1)
            # cv2.imshow('img', img)
            # cv2.waitKey(300)

    # mtx：摄像机内参数矩阵
    # dist：畸变系数(k1,k2,p1,p2[,k3[,k4,k5,k6],[s1,s2,s3,s4]]) k1和k2是径向形变系数，p1和p2是切向形变系数
    # rvecs：每一个靶标图片的对应的旋转矢量
    # tvecs：每一个靶标图片的对应的平移矢量grayL.shape[::-1]gray2.shape[::-1]
    ret1, mtx1, dist1, rvecs1, tvecs1 = cv2.calibrateCamera(
        objpoints, imgpoints1,(W, H), None, None, flags=cv2.CALIB_FIX_K3)
    ret2, mtx2, dist2, rvecs2, tvecs2 = cv2.calibrateCamera(
        objpoints, imgpoints2,(W, H), None, None, flags=cv2.CALIB_FIX_K3)
    # 双目立体标定
    # R：旋转矩阵；T：平移矩阵；E：本征矩阵；F：基础矩阵；
    # ret, mtx1, dist1, mtx2, dist2, R, T, E, F = cv2.stereoCalibrate(
    #     objpoints, imgpoints1, imgpoints2, mtx1, dist1, mtx2, dist2,
    #     (w, h),None, None, None, flags=cv2.CALIB_FIX_K3, criteria=criteria)
    ret, mtx1, dist1, mtx2, dist2, R, T, E, F = cv2.stereoCalibrate(
         objpoints, imgpoints1, imgpoints2, mtx1, dist1, mtx2, dist2,
         (W, H), None, None, None, flags=cv2.CALIB_FIX_INTRINSIC, criteria=criteria)
    T = -T
    doXML.createXML( 'data/init.xml', ret, mtx1, dist1, mtx2, dist2, R, T, E, F)

if __name__=='__main__':
    bincalib()