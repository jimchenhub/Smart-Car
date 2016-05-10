# -*- coding: utf-8 -*-
import cv2
import numpy as np

import sys
sys.path.append("../../config")
import common as common_config

H, W = (common_config.BINCAP_HEIGHT, common_config.BINCAP_WIDTH)

H, W = (common_config.BINIMG_HEIGHT, common_config.BINIMG_WIDTH)

if __name__=='__main__':
    cap0 = cv2.VideoCapture(1)
    cap0.set(cv2.CAP_PROP_FRAME_WIDTH, W);
    cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, H);
    cap1 = cv2.VideoCapture(0)

if __name__=='__main__':
    cap0 = cv2.VideoCapture(0)
    cap0.set(cv2.CAP_PROP_FRAME_WIDTH, W);
    cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, H);
    cap1 = cv2.VideoCapture(1)

    cap1.set(cv2.CAP_PROP_FRAME_WIDTH, W);
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, H);
    dst = np.zeros((H,2*W,3), np.uint8)
    i = 0
    while True:
        ret0, frame0 = cap0.read()
        ret1, frame1 = cap1.read()
        dst[0:H, 0:W] = frame0
        dst[0:H, W:2*W] = frame1
        cv2.imshow('', dst)

        if cv2.waitKey(1) & 0xFF==ord('a'):
            i += 1
            print i
            cv2.imwrite('data/test0/'+str(i)+'.jpg', frame0)
            cv2.imwrite('data/test1/'+str(i)+'.jpg', frame1)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
    cv2.destroyAllWindows()
    cap0.release()
    cap1.release()

