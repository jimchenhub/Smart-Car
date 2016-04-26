# -*- coding: utf-8 -*-
import cv2
import numpy as np

import sys
sys.path.append("../config")
import common as common_config

H, W = (common_config.BINCAP_HEIGHT, common_config.BINCAP_WIDTH)
if __name__=='__main__':
    cap0 = cv2.VideoCapture(0)
    cap0.set(cv2.CAP_PROP_FRAME_WIDTH, W);
    cap0.set(cv2.CAP_PROP_FRAME_HEIGHT,H);
    cap1 = cv2.VideoCapture(1)
    cap1.set(cv2.CAP_PROP_FRAME_WIDTH, W);
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, H);
    dst = np.zeros((H,2*W,3), np.uint8)
    i = 0
    j = 0
    while True:
        ret0, frame0 = cap0.read()
        ret1, frame1 = cap1.read()
        dst[0:H, 0:W] = frame0
        dst[0:H, W:2*W] = frame1
        cv2.imshow('', dst)
        j += 1
        if j%50 == 0:
            i += 1
            print i
            cv2.imwrite('data\\img0\\'+str(i)+'.jpg', frame0)
            cv2.imwrite('data\\img1\\'+str(i)+'.jpg', frame1)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break

    cv2.destroyAllWindows()
    cap0.release()
    cap1.release()


