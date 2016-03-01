'''
Get Training Data
~~~~~~~~

Get training data every SLEEP_TIME second
Store the image, named with direction information
'''

## Library
# Standard library
import time
# import Tkinter as tk
import sys

# Third party library
import numpy as np
import cv2

# my library - configuration
sys.path.append("/home/pi/Documents/Github/Smart-Car/source/config")
sys.path.append("/home/pi/Documents/Github/Smart-Car/source/component")
import move
import common as common_config


# main function
def getTrainingData():
    mo = move.Move()
    mo.forward(1)
    time.sleep(1)
    mo.backward(1)
    time.sleep(1)
    mo.turn_left(1)
    time.sleep(1)
    mo.turn_right(1)
    mo.stop()
    mo.shutdown()

getTrainingData()
