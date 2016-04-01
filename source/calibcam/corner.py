# -*- coding: utf-8 -*-
import numpy as np
import cv2
from matplotlib import pyplot as plt

def harris(gray):
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)
    dst = cv2.dilate(dst,None)
    return dst

def shi_tomasi(gray):
    # image：源图片
    # maxCorners：最佳角点数量
    # qualityLevel：质量等级，小于此质量等级的角点都会被忽略
    # minDistance：交点之间的最小距离
    corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
    cv2.computeCorrespondEpilines()
    # 返回的结果是 [[ 311., 250.]] 两层括号的数组。
    corners = np.int0(corners)
    return corners

def orb(gray):
    orb = cv2.ORB_create()
    kp, des = orb.detectAndCompute(gray, None)
    return kp,des

def sift(gray):
    pass

def surf(gray):
    pass

def brief(gray):
    pass

def fast(gray):
    pass



if __name__=='__main__':
    gray = cv2.imread('myleft.jpg',0)
    kp,des = orb(gray)
    print kp[1].class_id
    img2 = cv2.drawKeypoints(gray, kp, None,color=(0,255,0), flags=0)
    plt.imshow(img2),plt.show()
    pass






