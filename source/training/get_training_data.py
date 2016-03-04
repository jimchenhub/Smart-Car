'''
Get Training Data
~~~~~~~~

Get training data every SLEEP_TIME second
Store the image, named with direction information
'''

## Library
# Standard library
import time
import sys
import random

# Third party library
import numpy as np
import cv2

# my library - configuration
sys.path.append("/home/pi/Documents/Github/Smart-Car/source/config")
sys.path.append("/home/pi/Documents/Github/Smart-Car/source/component")
import move
import image_preprocess as imgprocess
import common as common_config

# save image function
def save_image(direction, image):
    now = int(time.time())
    name = "/home/pi/Documents/Github/Smart-Car/source/data/"+str(now)+"-"+str(direction)+"-"+str(random.randint(1, 1000))+".jpg"
    print "want to save file:"+name
    cv2.imwrite(name, image)


## Main function
# major variables
cap = cv2.VideoCapture(0)
mo = move.Move()

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # Change frame to gray level image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = imgprocess.imageDW(gray,gray.shape,4)

    # Display the resulting frame
    cv2.imshow('frame',frame)

    # Choose direction or quit
    input_key = cv2.waitKey(1) & 0xFF
    if input_key == ord('q'):
        break
    elif input_key == ord('w'):
        mo.forward(common_config.SLEEP_TIME)
        save_image("w", gray)
    elif input_key == ord('s'):
        mo.backward(common_config.SLEEP_TIME)
        save_image("s", gray)
    elif input_key == ord('a'):
        mo.turn_left(common_config.SLEEP_TIME)
        save_image("a", gray)
    elif input_key == ord('d'):
        mo.turn_right(common_config.SLEEP_TIME)
        save_image("d", gray)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
print "Finish recording"

# shutdown the car
mo.stop()
mo.shutdown()
print "Car shutdown"

