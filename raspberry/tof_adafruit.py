import RPi.GPIO as GPIO
import board
import VL53L1X
import adafruit_vl53l1x
import time
import signal
import sys


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)			#disable warnings

i2c = board.I2C()

class Tof:
    DEFAULT_ADDRESS = 0x29
    def __init__(self, address=0x29, xshut_pin=None):
        # self.xshut_pin = xshut_pin
        if xshut_pin is not None:
            self.reset_address(xshut_pin)
        try:
            self.tof = adafruit_vl53l1x.VL53L1X(i2c)
            if address != self.DEFAULT_ADDRESS:
                self.change_address(address)
        except:
            self.tof = adafruit_vl53l1x.VL53L1X(i2c, address=address)
        self.tof.start_ranging()
    
    def change_address(self, address):
        self.tof.set_address(address)
    
    def reset_address(self, xshut_pin):
        GPIO.setup(xshut_pin, GPIO.OUT)
        GPIO.output(xshut_pin, GPIO.LOW)
        GPIO.output(xshut_pin, GPIO.HIGH)

    def get_distance(self):
        while not self.tof.data_ready:
            pass
        sensor_value = self.tof.distance
        self.tof.clear_interrupt()
        return sensor_value

    # def __del__(self):
    #     self.tof.stop_ranging()

def exit_handler(signal, frame):
    global running
    running = False
    sys.exit(0)

if __name__ == '__main__':
    running = True
    signal.signal(signal.SIGINT, exit_handler)
    right_tof = Tof(address=0x33)
    left_tof = Tof(xshut_pin=17)
    while running:
        right_distance = right_tof.get_distance()
        left_distance = left_tof.get_distance()
        print(f'{right_distance=}, {left_distance=}')
