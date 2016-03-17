import RPi.GPIO as gpio
import time

class Wheel(object):
    def __init__(self, in_pin1, in_pin2, enable_pin1, enable_pin2):
        self.pin1 = in_pin1
        self.pin2 = in_pin2

        # Set IO output
        gpio.setup(in_pin1, gpio.OUT)
        gpio.setup(in_pin2, gpio.OUT)
        gpio.setup(enable_pin1, gpio.OUT)
        gpio.setup(enable_pin2, gpio.OUT)

        # Enable wheel
        gpio.output(enable_pin1, True)
        gpio.output(enable_pin2, True)

    def forward(self):
        gpio.output(self.pin1, True)
        gpio.output(self.pin2, False)

    def backward(self):
        gpio.output(self.pin1, False)
        gpio.output(self.pin2, True)

    def stop(self):
        gpio.output(self.pin1, False)
        gpio.output(self.pin2, False)

class Move(object):
    def __init__(self):
        gpio.setmode(gpio.BOARD)

        self.right_wheel = Wheel(11, 12, 16, 18)
        self.left_wheel = Wheel(13, 15, 29, 31)

        print("move initiated")

    def forward(self, tf):
        self.left_wheel.forward()
        self.right_wheel.forward()
        time.sleep(tf)
        #gpio.cleanup()
        self.stop()

    def backward(self, tf):
        self.left_wheel.backward()
        self.right_wheel.backward()
        time.sleep(tf)
        #gpio.cleanup()
        self.stop()

    def turn_left(self, tf):
        self.right_wheel.forward()
        time.sleep(tf)
        #gpio.cleanup()
        self.stop()

    def turn_right(self, tf):
        self.left_wheel.forward()
        time.sleep(tf)
        #gpio.cleanup()
        self.stop()

    def stop(self):
        self.left_wheel.stop()
        self.right_wheel.stop()
        #gpio.cleanup()

    def shutdown(self):
        self.stop()
        gpio.cleanup()


