# -*- coding: utf-8 -*-
import numpy as np
import cv2

import sys
sys.path.append("../../config")
import common as common_config
import util as util
BINIMG_H, BINIMG_W = (common_config.BINIMG_HEIGHT, common_config.BINIMG_WIDTH)

def run():
    capL = cv2.VideoCapture(1)
    capL.set(cv2.CAP_PROP_FRAME_WIDTH, BINCAP_W)
    capL.set(cv2.CAP_PROP_FRAME_HEIGHT, BINCAP_H)
    capR = cv2.VideoCapture(0)
    capR.set(cv2.CAP_PROP_FRAME_WIDTH, BINCAP_W)
    capR.set(cv2.CAP_PROP_FRAME_HEIGHT, BINCAP_H)
    while True:
        disparity = util.getDisparity(capL.read(), capR.read())
        cv2.imshow('disparity', disparity)
        orient = util.getOriention(disparity)
        if orient == 2:
            print 'forward'
            continue

        while orient == 0:
            print 'backward'
            disparity = util.getDisparity(capL.read(), capR.read())
            cv2.imshow('disparity', disparity)
            orient = util.getOriention(disparity)

        while orient==1:
            turn = turnTo(disparity)
            # turn left
            if turn==3:
                while orient!=2:
                    print 'turn left'
                    disparity = util.getDisparity(capL.read(), capR.read())
                    cv2.imshow('disparity', disparity)
                    orient = util.getOriention(disparity)
            # turn right
            elif turn==4:
                while orient!=2:
                    print 'turn right'
                    disparity = util.getDisparity(capL.read(), capR.read())
                    cv2.imshow('disparity', disparity)
                    orient = util.getOriention(disparity)
        # end
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    cap0.release()
    cap1.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    run()