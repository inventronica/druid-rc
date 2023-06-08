import multiprocessing
import adafruit_icm20x
import time
import signal
from exit_handler import exit_handler
import board
import math
import RPi.GPIO as GPIO
import adafruit_vl53l1x
import sys
import adafruit_tcs34725 as col_lib

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)			#disable warnings
i2c = board.I2C()


class Color:
    def __init__(self, enable_pin=25):
        self.enable_pin = enable_pin
        GPIO.setup(self.enable_pin, GPIO.OUT)
        self.sensor = None
        self.power_off()
        self.running = multiprocessing.Value('i', 1)
        self.color = multiprocessing.Value('i', 1) # 0 = Unknown -- 1 = Orange -- 2 = Blue

    def color_read(self):
        if self.sensor is None:
            return
        while self.running.value == 1:
            r, g, b = self.sensor.color_rgb_bytes
            if(b > r+g):
                self.color.value = 2
            elif(r > g+b):
                self.color.value = 1
            else:
                self.color.value = 0

    def power_off(self):
        GPIO.output(self.enable_pin, GPIO.HIGH)
        if self.sensor is not None:
            self.sensor = None
    
    def power_on(self):
        GPIO.output(self.enable_pin, GPIO.LOW)
        self.sensor = col_lib.TCS34725(i2c)


class Gyro:
    def __init__(self):
        self._icm = adafruit_icm20x.ICM20948(i2c)
        self._icm.GyroRange = 500
        self.angle = 0
        self._last_speed = 0
        self._time = time.time()

    def calculate_angle(self):
        new_time = time.time()
        delta = new_time - self._time
        self._time = new_time
        x, y, z = self._icm.gyro
        z = round((z - 0.001395504677919364), 3)
        self.angle = self.angle +(self._last_speed + z)*delta/2
        self._last_speed = z 
        return self.angle

class Tof:
    DEFAULT_ADDRESS = 0x29
    def __init__(self, address = 0x29, xshut_pin=None):
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

def exit_handler(signal, frame):
    global running
    running = False
    sys.exit(0)


def tof_test():
    running = True
    signal.signal(signal.SIGINT, exit_handler)
    my_color = Color()
    right_tof = Tof(address=0x33)
    left_tof = Tof(xshut_pin=17)
    left_tof.change_address(0x32)
    my_color.power_on()
    # color_process.start()
    while running:
        right_distance = right_tof.get_distance()
        # left_distance = left_tof.get_distance()

def color_test():
    running = True
    signal.signal(signal.SIGINT, exit_handler)
    my_color = Color()
    color_process = multiprocessing.Process(target=my_color.color_read)
    color_process.start()
    while running:
        time.sleep(1)
    my_color.running.value = 0
    color_process.join()

def gyro_process(running, angle):
    gyro = Gyro()
    while running.value == 1:
        angle.value = gyro.calculate_angle()

def gyro_test():
    signal.signal(signal.SIGINT, exit_handler)
    running = True
    gyro = Gyro()
    gyro_process = multiprocessing.Process(target=gyro.calculate_angle)
    gyro_process.start()
    # gyro_process.join()
    while running:
        # if gyro.n.value > 0:
        time.sleep(1)
    gyro.running.value = 0
    gyro_process.join()


if __name__ == '__main__':
    tof_test()
