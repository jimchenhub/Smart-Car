# -*- coding: UTF-8 -*-
'''
Expand the data
~~~~~~~~~~~~

horizontal transfomation first, double the data size
---
0311
图像增强，增加几倍图像数据量
'''

## Libraries
# Standard library
import os

# Third-party libraries
import numpy as np
import cv2

# static variables
DATA_DIR = "../data/expanded"
available_type = [".gif", ".jpg", ".jpeg", ".bmp", ".png"]
OUTPUT_DIR = "../data/expanded/"

# 水平转换图像来扩充数据
def horizontal_trans(name, img):
    # flip the image
    new_img = cv2.flip(img, 1)
    # choose new name
    name_part = name.split("-")
    direction = name_part[1]
    new_direction = "w"
    if direction == "a":
        new_direction = "d"
    elif direction == "d":
        new_direction = "a"
    new_name = name_part[0] + "-" + new_direction + "-" + str(int(name_part[2].split(".")[0]) + 1) + "." + name_part[2].split(".")[1]
    return (new_name, new_img)

def color_enhancement(name, img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    new_img = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i][j] = 0 if img[i][j] < 220 else 255
    name_part = name.split("-")
    new_name = name_part[0] + "-" + name_part[1] + "-" + str(int(name_part[2].split(".")[0]) + 2) + "." + name_part[2].split(".")[1]
    return (new_name, new_img)

# 将某个文件夹下的图片进行水平变换
def expand_data():
    # 读取文件夹下所有图片
    fileList = os.listdir(DATA_DIR)
    # 对每个文件进行图像增强处理
    # for file in fileList:
    #     if file_extension(file) not in available_type:
    #         continue
    #     fullfile = os.path.join(DATA_DIR, file)
    #     # read image
    #     img = cv2.imread(fullfile)
    #     # 增强处理
    #     new_names, new_imgs = horizontal_trans(file, img)
    #     for new_name, new_img in zip(new_names, new_imgs):
    #         cv2.imwrite(os.path.join(OUTPUT_DIR, new_name), new_img)
    # 对每个文件进行水平变换处理
    for file in fileList:
        if file_extension(file) not in available_type:
            continue
        fullfile = os.path.join(DATA_DIR, file)
        # read image
        img = cv2.imread(fullfile)
        # 水平转换
        new_name, new_img = horizontal_trans(file, img)
        cv2.imwrite(os.path.join(OUTPUT_DIR, new_name), new_img)
        # 图像增强
        # new_name, new_img = color_enhancement(file, img)
        # cv2.imwrite(os.path.join(OUTPUT_DIR, new_name), new_img)

def file_extension(path): 
    return os.path.splitext(path)[1]

expand_data()