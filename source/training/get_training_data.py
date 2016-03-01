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
sys.path.append("../config")
import common as common_config
sys.path.append("../component")
import move.Move as Move


# main function
def getTrainingData():
    movement = Move()


getTrainingData()