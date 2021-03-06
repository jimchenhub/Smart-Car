# -*- coding: UTF-8 -*-
'''
Final version of run
~~~~~~~~

'''

## Library
# Standard library
import time
import sys
from threading import Thread

# Third party library
import numpy as np
import cv2

# my library - configuration
# sys.path.append("/home/pi/Documents/Github/Smart-Car/source/config")
# sys.path.append("/home/pi/Documents/Github/Smart-Car/source/component")
sys.path.append("../config")
sys.path.append("../component")
sys.path.append("./avoiding")
import move
import network
import image_preprocess as imgprocess
import common as common_config
import avoid_client
import bypass

## Main function
THRESHOLD = 220
# major variables
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
mo = move.Move()
net = network.load("../config/result/0316-93%")
count = 0     # use for get orient

# prepare initiation
avoid_client.init(capL_id=2, capR_id=1)

## Get Frame part
#Continually updates the frame
class GetFrameThread(Thread):
    def __init__(self):  
        Thread.__init__(self)
        self.thread_stop = False  
   
    def run(self):
        global ret, frame
        while not self.thread_stop:  
            ret, frame = cap.read()

    def stop(self):  
        self.thread_stop = True  

def getFrame():
    global ret, frame
    return ret, frame

tr = GetFrameThread()
tr.start()

# main loop
while(cap.isOpened()):
    # Capture frame-by-frame
    # ret, frame = cap.read()
    ret, current_frame = getFrame()

    # Our operations on the frame come here
    # Change frame to gray level image and do some trasition
    gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    img = imgprocess.imageDW(gray,(common_config.CAP_HEIGHT,common_config.CAP_WIDTH),1)
    new_img = np.zeros(img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i][j] = 0 if img[i][j] < THRESHOLD else 255
    new_img = new_img.ravel()
    new_img = [y/255.0 for y in new_img]
    new_img = np.reshape(new_img, (common_config.NETWORK_INPUT_SIZE, 1))

    cv2.imshow("frame", img)
    # decide direction
    direction = np.argmax(net.feedforward(new_img))

    # find obstacle
    if count % 3 == 0    # every 3 loop get one orient
        orient = avoid_client.getOrient()
        count += 1
        count = count % 3
        if orient is not 2:
            bypass.bypass()

    # Choose direction or quit
    input_key = cv2.waitKey(0) & 0xFF
    if input_key == ord('q'):
        break
    if direction == 0:
        mo.forward(common_config.SLEEP_TIME)
        print "forward"
    elif direction == 1:
        mo.turn_left(common_config.SLEEP_TIME)
        print "turn left"
    elif direction == 2:
        mo.turn_right(common_config.SLEEP_TIME)
        print "turn right"

# When everything done, release the capture
tr.stop() # stop the thread 

cap.release()
cv2.destroyAllWindows()
print "Finish recording"

# shutdown the car
mo.stop()
mo.shutdown()
print "Car shutdown"
