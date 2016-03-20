import numpy as np
import cv2
import cPickle
import sys
sys.path.append("../component")
sys.path.append("../config")
import network
import common as common_config

THRESHOLD = 220
DATA_DIR = "../data/expanded/"
available_type = [".gif", ".jpg", ".jpeg", ".bmp", ".png"]
INPUT_SIZE = common_config.NETWORK_INPUT_SIZE
OUTPUT_SIZE = 3

net = network.load("../config/result/0317-95%")

f = open(DATA_DIR+"data.pkl", 'rb')
training_data, validation_data, te_d = cPickle.load(f)
f.close()
test_inputs = [np.reshape(x, (INPUT_SIZE, 1)) for x in te_d[0]]
test_data = zip(test_inputs, te_d[1])

count = 0
for td in test_data:
    tr = np.argmax(net.feedforward(td[0]))
    # print tr, td[1]
    if tr == td[1]:
        count += 1
    else:
        print tr, td[1]
print "accuracy: ", count, "/100", 