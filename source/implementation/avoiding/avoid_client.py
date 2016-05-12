# -*- coding: UTF-8 -*-
import cv2
import socket
import time
import StringIO
import numpy as np
from threading import Thread
import sys
sys.path.append("../../config")
import common as common_config

BINCAP_H, BINCAP_W = (common_config.BINCAP_HEIGHT, common_config.BINCAP_WIDTH)


class GetFrameLThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.thread_stop = False

    def run(self):
        global frameL, capL
        while not self.thread_stop:
            retL, frameL = capL.read()

    def stop(self):
        self.thread_stop = True


class GetFrameRThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.thread_stop = False

    def run(self):
        global frameR, capR
        while not self.thread_stop:
            retR, frameR = capR.read()

    def stop(self):
        self.thread_stop = True


def init(host='lenovo-pc', port=1234, capL_id=2, capR_id=1):
    global capL, capR, ltr, rtr, sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    capL = cv2.VideoCapture(capL_id)
    capL.set(cv2.CAP_PROP_FRAME_WIDTH, BINCAP_W)
    capL.set(cv2.CAP_PROP_FRAME_HEIGHT, BINCAP_H)
    capR = cv2.VideoCapture(capR_id)
    capR.set(cv2.CAP_PROP_FRAME_WIDTH, BINCAP_W)
    capR.set(cv2.CAP_PROP_FRAME_HEIGHT, BINCAP_H)
    ltr = GetFrameLThread()
    rtr = GetFrameRThread()
    ltr.start()
    rtr.start()


def end():
    global capL, capR, ltr, rtr
    capL.release()
    capR.release()
    ltr.stop()
    rtr.stop()


def getOrient():
    global sock, capL, capR, frameL, frameR
    retL, img_encodeL = cv2.imencode(
        '.jpeg',
        frameL[50:100],
        encode_param
    )
    retR, img_encodeR = cv2.imencode(
        '.jpeg',
        frameR[50:100],
        encode_param
    )
    stringDataL = np.array(img_encodeL).tostring()
    stringDataR = np.array(img_encodeR).tostring()
    client_commandL = 'put'.ljust(16)
    if confirm(sock, client_commandL):
        print client_commandL
        sock.send(str(len(stringDataL)).ljust(16))
        sock.send(stringDataL)
        sock.send(str(len(stringDataR)).ljust(16))
        sock.send(stringDataR)
    else:
        print 'server error!'
        return False
    orient = sock.recv(4096)
    return int(orient)


def confirm(s, client_command):
    s.send(client_command)
    data = s.recv(4096)
    if data == 'ready':
        return True


capL = None
capR = None
frameL = None
frameR = None
ltr = None
rtr = None
sock = None
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY), 90]

if __name__ == '__main__':
    # 获取一次方向的例子
    init(capL_id=0, capR_id=0)
    # 默认参数：
    # host='lenovo-pc',
    # port=1234
    # capL_id=2
    # capR_id=1
    orient = getOrient()
    end()