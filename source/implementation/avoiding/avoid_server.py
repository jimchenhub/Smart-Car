# -*- coding: UTF-8 -*-

import SocketServer, socket

import numpy as np
import cv2

import util as util
import sys
sys.path.append("../../config")
import common as common_config
BINIMG_H, BINIMG_W = (common_config.BINIMG_HEIGHT, common_config.BINIMG_WIDTH)
BINCAP_H, BINCAP_W = (common_config.BINCAP_HEIGHT, common_config.BINCAP_WIDTH)
class MyHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        print 'get connection from :',self.client_address
        imgL = np.zeros((BINCAP_H, BINCAP_W, 3), np.uint8)
        imgR = np.zeros((BINCAP_H, BINCAP_W, 3), np.uint8)
        while True:
            try:
                data = self.request.recv(16)
                print 'receive data:',data
                if not data:
                    print 'break connection!'
                    break
                else:
                    action = str(data).strip()
                    if action == 'put':
                        self.request.send('ready')
                        stringDataL = self.recvdata()
                        stringDataR = self.recvdata()
                    else:
                        print 'receive error!'
                        continue

                imgL[50:100] = cv2.imdecode(np.fromstring(stringDataL, dtype='uint8'), 1)
                imgL_640_480 = cv2.resize(imgL, (BINIMG_W, BINIMG_H), interpolation=cv2.INTER_CUBIC)
                # cv2.imshow('L', imgL_640_480)
                #
                imgR[50:100] = cv2.imdecode(np.fromstring(stringDataR, dtype='uint8'), 1)
                imgR_640_480 = cv2.resize(imgR, (BINIMG_W, BINIMG_H), interpolation=cv2.INTER_CUBIC)
                # cv2.imshow('R', imgR_640_480)

                disparity = util.getDisparity(imgL_640_480, imgR_640_480)
                # cv2.imshow('disparity',np.uint8(disparity))

                orient = util.getOriention(disparity)
                self.request.send(str(orient))

                if cv2.waitKey(1) & 0xff==ord('q'):
                    self.request.send('end')
                    cv2.destroyAllWindows()
                    break
            except Exception,e:
                print 'error:',e
                break

    def recvdata(self):
        print "start receiving!"
        length = int(self.request.recv(16))
        buf = b''
        while length:
            newbuf = self.request.recv(int(length))
            if not newbuf:break
            buf += newbuf
            length -= len(newbuf)
        print 'recv data success'
        return buf

if __name__ == '__main__':
    print 'host-name:', socket.gethostname()
    host = ''
    port = 1234
    s = SocketServer.TCPServer((host,port), MyHandler)
    s.serve_forever()