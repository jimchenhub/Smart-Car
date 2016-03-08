# -*- coding: UTF-8 -*-
'''
Data Loader
~~~~~~~~~~~~

A common component to load image data. The input dimensional number is 76800 (320 * 240)
, the output dimensional number is 3 (forward, turn left, turn right)
'''

## Libraries
# Standard library
import cPickle
import gzip
import os

# Third-party libraries
import numpy as np
import cv2

# static variables
DATA_DIR = "../data/"
available_type = [".gif", ".jpg", ".jpeg", ".bmp", ".png"]
INPUT_SIZE = 76800

# 从pkl或其他类型的文件中反序列化出训练数据
def load_data():
    f = open('../data/data.pkl', 'rb')
    training_data, validation_data, test_data = cPickle.load(f)
    f.close()
    return (training_data, validation_data, test_data)

def load_data_wrapper():
    """
    Return a tuple containing ``(training_data, validation_data,
    test_data)``. Based on ``load_data``, but the format is more
    convenient for use in our implementation of neural networks.
    """
    tr_d, va_d, te_d = load_data()
    training_inputs = [np.reshape(x, (INPUT_SIZE, 1)) for x in tr_d[0]]
    training_results = [vectorized_result(y) for y in tr_d[1]]
    training_data = zip(training_inputs, training_results)
    validation_inputs = [np.reshape(x, (INPUT_SIZE, 1)) for x in va_d[0]]
    validation_data = zip(validation_inputs, va_d[1])
    test_inputs = [np.reshape(x, (INPUT_SIZE, 1)) for x in te_d[0]]
    test_data = zip(test_inputs, te_d[1])
    return (training_data, validation_data, test_data)

# 将某个文件夹下的图片进行序列化成pkl等类型的文件
def generate_data():
    # 读取文件夹下所有图片
    fileList = os.listdir(DATA_DIR)
    # 计算文件夹内的文件数量
    count = 0
    for file in fileList:
        if file_extension(file) not in available_type:
            continue
        count += 1
    # 初始化结果
    images=np.ndarray((count, INPUT_SIZE), dtype=np.float32)
    results = np.ndarray(count, dtype=np.int64)
    count = 0
    # 对每个文件进行处理
    for file in fileList:
        if file_extension(file) not in available_type:
            continue
        fullfile = os.path.join(DATA_DIR, file)
        # read image
        img = cv2.imread(fullfile)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = gray.ravel() # 平展化
        gray = [y/255.0 for y in gray] # 将每个值都变成小于1的灰度比例
        # calculate result. this value will be read from file name
        result = 0
        # save data 
        images[count] = gray
        results[count] = result
        count += 1
    # 构建pkl文件的内容
    training_data = (images, results)
    # 暂时使用training数据代替validation数据,暂时使用training数据代替test数据
    datas = (training_data, training_data, training_data)
    print datas
    # save to file
    cPickle.dump(datas, open(DATA_DIR+"data.pkl","wb"))

def file_extension(path): 
    return os.path.splitext(path)[1]

def vectorized_result(j):
    """Return a 3-dimensional unit vector with a 1.0 in the jth
    position and zeroes elsewhere.  This is used to convert a digit
    (0...2) into a corresponding desired output from the neural
    network."""
    e = np.zeros((3, 1))
    e[j] = 1.0
    return e

# training_data, validation_data, test_data = load_data_wrapper()
# print training_data,"\n\n", validation_data,"\n\n", test_data