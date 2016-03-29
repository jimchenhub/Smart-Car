# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 08:53:34 2014
@author: duan
"""
import numpy as np
import cv2
import glob
from matplotlib import pyplot as plt
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (20,0,0), (40,0,0) ....,(120,100,0)
# 实际上，靶标的方格长宽为20mm
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)*20
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
        cv2.imshow('img',img)
        cv2.waitKey(500)

# objpoints：元素是靶标图的点在点阵中的坐标的集合（以mm为单位）
# imgpoints：元素是靶标图的点在像素坐标系中的坐标的集合

# mtx：摄像机内参数矩阵
# dist：畸变系数(k1,k2,p1,p2[,k3[,k4,k5,k6],[s1,s2,s3,s4]]) k1和k2是径向形变系数，p1和p2是切向形变系数
# rvecs：每一个靶标图片的对应的旋转矢量
# tvecs：每一个靶标图片的对应的平移矢量
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

# print "ret:",ret
# print "mtx:",mtx
# print "dist:",dist
# print "rvecs:",rvecs[0]
# print "tvecs:",tvecs[0]

# for rvec in rvecs:
#     print rvec

img = cv2.imread('left12.jpg')
h, w = img.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

# undistort
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
# crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv2.imshow('calibresult.png',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()