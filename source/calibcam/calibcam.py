# -*- coding: utf-8 -*-
import numpy as np
import cv2
import glob
from matplotlib import pyplot as plt
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# objpoints：靶标图的点世界坐标系中的坐标（以mm为单位）
# imgpoints：靶标图的点在像素坐标系中的坐标
# 实际上，靶标的方格长宽为20mm，(0,0,0), (20,0,0), (40,0,0) ....,(120,100,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)*20
objpoints = []
imgpoints = []

images = glob.glob('*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # 检测棋盘方格
    ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
        cv2.imshow('img',img)
        cv2.waitKey(500)

# mtx：摄像机内参数矩阵
# dist：畸变系数(k1,k2,p1,p2[,k3[,k4,k5,k6],[s1,s2,s3,s4]]) k1和k2是径向形变系数，p1和p2是切向形变系数
# rvecs：每一个靶标图片的对应的旋转矢量，旋转矢量可转换成旋转向量
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
# 矫正
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv2.imshow('calibresult.png',dst)
cv2.waitKey(0)
cv2.destroyAllWindows()