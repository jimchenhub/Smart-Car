# -*- coding: UTF-8 -*-
'''
Expand the data
~~~~~~~~~~~~

horizontal transfomation first, double the data size
'''

## Libraries
# Standard library
import os

# Third-party libraries
import numpy as np
import cv2

# static variables
DATA_DIR = "../data/"
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

# 将某个文件夹下的图片进行水平变换
def expand_data():
    # 读取文件夹下所有图片
    fileList = os.listdir(DATA_DIR)
    # 对每个文件进行处理
    for file in fileList:
        if file_extension(file) not in available_type:
            continue
        fullfile = os.path.join(DATA_DIR, file)
        # read image
        img = cv2.imread(fullfile)
        # 水平转换
        new_name, new_img = horizontal_trans(file, img)
        # save image
        cv2.imwrite(os.path.join(OUTPUT_DIR, new_name), new_img)

def file_extension(path): 
    return os.path.splitext(path)[1]

expand_data()