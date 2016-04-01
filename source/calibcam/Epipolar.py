# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib as plt
import corner

def drawlines(img1,img2,lines,pts1,pts2):
    ''' img1 - image on which we draw the epilines for the points in img2
    lines - corresponding epilines '''
    r,c = img1.shape
    img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR)
    for r,pt1,pt2 in zip(lines,pts1,pts2):
        color = tuple(np.random.randint(0,255,3).tolist())
        x0,y0 = map(int, [0, -r[2]/r[1] ])
        x1,y1 = map(int, [c, -(r[2]+r[0]*c)/r[1] ])
        img1 = cv2.line(img1, (x0,y0), (x1,y1), color,1)
        img1 = cv2.circle(img1,tuple(pt1),5,color,-1)
        img2 = cv2.circle(img2,tuple(pt2),5,color,-1)
    return img1,img2

def calpolar(lines):
   for i in range(len(lines)-1):
        L1 = lines[i]
        L2 = lines[i+1]
        D =  L1[0]*L2[1] - L2[0]*L1[1]
        x = (L1[1]*L2[2] - L2[1]*L1[2])/D
        y = (L1[2]*L2[0] - L2[2]*L1[0])/D
        print x,y

img1 = cv2.imread('image\\myleft.jpg', 0)
img2 = cv2.imread('image\\myright.jpg', 0)

# ORB找到关键点和描述符
kp1, des1 = corner.orb(img1)
kp2, des2 = corner.orb(img2)

# FLANN parameters
# FLANN_INDEX_KDTREE = 0
# index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
# search_params = dict(checks=50)
# flann = cv2.FlannBasedMatcher(index_params,search_params)
# matches = flann.knnMatch(des1,des2,k=2)

bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)
good = []
pts1 = []
pts2 = []
# 得到匹配点列表
for i,(m,n) in enumerate(matches):
    if m.distance < 0.8*n.distance:
        good.append(m)
        pts2.append(kp2[m.trainIdx].pt) #Dmatch.trainIdx 训练图像的特征描述的索引
        pts1.append(kp1[m.queryIdx].pt) #Dmatch.queryIdx 查询图像的特征描述的索引

# 通过匹配点列表计算基础矩阵
pts1 = np.int32(pts1)
pts2 = np.int32(pts2)
F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_LMEDS)
E, mask = cv2.findEssentialMat(pts1, pts2, cv2.FM_RANSAC)
# 选择内点,0:外点，1：内点
pts1 = pts1[mask.ravel()==1]
pts2 = pts2[mask.ravel()==1]
# 在右图中找到极线
# pts2.reshape(-1,1,2)：从一维点数组转化为1*N的矩阵
lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1,1,2), 2, F)
# 从1*N线矩阵转化为1*N的线数组,线(a, b, c)：ax + by + c=0
lines1 = lines1.reshape(-1, 3)
img5,img6 = drawlines(img1, img2, lines1, pts1, pts2)

# 在左图中找到极线
lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1,1,2), 1, F)
lines2 = lines2.reshape(-1, 3)
img3,img4 = drawlines(img2, img1, lines2, pts2, pts1)

print 'lines1:'
calpolar(lines1)
print 'lines2:'
calpolar(lines2)

cv2.imshow('5', img5)
cv2.imshow('3', img3)
cv2.waitKey(0)
cv2.destroyAllWindows()




