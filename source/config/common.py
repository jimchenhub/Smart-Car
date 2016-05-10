'''
 Here are all the common configurations
'''

# Sleep time constance. (s)
# Every SLEEP_TIME second will decide a direction to run
SLEEP_TIME = 0.050

#  Resolution ratio of capture
CAP_WIDTH = 64
CAP_HEIGHT = 48

# network configuration
NETWORK_INPUT_SIZE = 3072  # 64 * 48

# Resolution ratio of binocular camera
<<<<<<< HEAD
BINCAP_WIDTH = 160
BINCAP_HEIGHT = 120

# Resolution ratio of a image pair
BINIMG_WIDTH = 640
BINIMG_HEIGHT = 480

# Real height(mm) of binocular camera
BINCAP_REAL_HEIGHT = 200
=======
BINCAP_WIDTH = 640
BINCAP_HEIGHT = 480

# Real height(mm) of binocular camera
BINCAP_REAL_HEIGHT = 150
>>>>>>> 1d4985d41239348dc923930ea25c923e533ed194

# Real Weight of car
CAR_REAL_WIDTH = 130

# Max distance(mm) of avoiding
MAXDEPTH = 300
<<<<<<< HEAD
MINDEPTH = 200

=======
MINDEPTH = 180
>>>>>>> 1d4985d41239348dc923930ea25c923e533ed194
