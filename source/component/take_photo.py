# -*- coding: <encoding name> -*-

# standard library
import time
import random

# third party library
import numpy as np
import cv2

# my library - configuration
import sys
sys.path.append("../config")
import common as common_config
# print common_config.SLEEP_TIME


cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # Change frame to gray level image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # save image to data divectory named by corresponding direction instruction
    # For now, the direction is simulated by random. The accurate direction will be gotten later by manual operation
    direction = random.randint(1,4)
    now = time.time()
    name = "../data/"+str(now)+"---"+str(direction)+"---"+str(random.randint(1,1000))+'.jpg'
    cv2.imwrite(name, gray)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Wait for a while
    time.sleep(common_config.SLEEP_TIME)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
