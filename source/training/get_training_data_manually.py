'''
Get Training Data Manually
~~~~~~~~

something wrong with raspberry pi
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
sys.path.append("../config")
sys.path.append("../component")
import image_preprocess as imgprocess

# save image function
def save_image(direction, image):
    now = int(time.time())
    name = "../data/"+str(now)+"-"+str(direction)+"-"+str(random.randint(1, 1000))+".jpg"
    print "want to save file:"+name
    cv2.imwrite(name, image)


## Main function
# major variables
cap = cv2.VideoCapture(1)

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # Change frame to gray level image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = imgprocess.imageDW(gray,gray.shape,2)

    # Do not display the resulting frame
    cv2.imshow('frame',img)

    # Choose direction or quit
    input_key = cv2.waitKey(1) & 0xFF
    if input_key == ord('q'):
        break
    elif input_key == ord('w'):
        save_image("w", img)
    elif input_key == ord('s'):
        save_image("s", img)
    elif input_key == ord('a'):
        save_image("a", img)
    elif input_key == ord('d'):
        save_image("d", img)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
print "Finish recording"