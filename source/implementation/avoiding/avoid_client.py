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
ORIENT = 1


class GetFrameLThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.thread_stop = False

    def run(self):
        global retL, frameL
        while not self.thread_stop:
            retL, frameL = capL.read()

    def stop(self):
        self.thread_stop = True


class GetFrameRThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.thread_stop = False

    def run(self):
        global retR, frameR
        while not self.thread_stop:
            retR, frameR = capR.read()

    def stop(self):
        self.thread_stop = True


def getOrient():
    global ORIENT
    return ORIENT


def confirm(s, client_command):
    s.send(client_command)
    data = s.recv(4096)
    if data == 'ready':
        return True


# host = str(raw_input("Input host-ip:"))
host = 'lenovo-pc'
port = 1234
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

capL = cv2.VideoCapture(2)
capL.set(cv2.CAP_PROP_FRAME_WIDTH, BINCAP_W)
capL.set(cv2.CAP_PROP_FRAME_HEIGHT, BINCAP_H)
capR = cv2.VideoCapture(1)
capR.set(cv2.CAP_PROP_FRAME_WIDTH, BINCAP_W)
capR.set(cv2.CAP_PROP_FRAME_HEIGHT, BINCAP_H)
retL, frameL = capL.read()
retR, frameR = capR.read()
ltr = GetFrameLThread()
rtr = GetFrameRThread()
ltr.start()
rtr.start()

encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]

try:
    s.connect((host,port))
    while capL.isOpened() and capR.isOpened():
        T1 = time.time()
        retL, img_encodeL = cv2.imencode('.jpeg', frameL[50:100], encode_param)
        retR, img_encodeR = cv2.imencode('.jpeg', frameR[50:100], encode_param)
        dataL = np.array(img_encodeL)
        stringDataL = dataL.tostring()
        dataR = np.array(img_encodeR)
        stringDataR = dataR.tostring()
        client_commandL = 'put'.ljust(16)
        if confirm(s, client_commandL):
            print client_commandL
            s.send(str(len(stringDataL)).ljust(16))
            s.send(stringDataL)
            s.send(str(len(stringDataR)).ljust(16))
            s.send(stringDataR)
        else:
            print 'server error!'
            exit()
        orient = s.recv(4096)
        print orient
        T2 = time.time()
        print T2-T1
except socket.error,e:
    print "error:",e
finally:
    s.close()
    ltr.stop()
    rtr.stop()
    exit()



