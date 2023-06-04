import RPi.GPIO as GPIO
import VL53L1X
import time
import signal


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)			#disable warnings

class Tof:
    DEFAULT_ADDRESS = 0x29
    def __init__(self, address=0x29, xshut_pin=None):
        # self.xshut_pin = xshut_pin
        if xshut_pin is not None:
            self.reset_address(xshut_pin)
        try:
            self.tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=self.DEFAULT_ADDRESS)
            self.tof.open()
        
            if address != self.DEFAULT_ADDRESS:
                self.change_address(address)
        except RuntimeError:
            self.tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=address)
            self.tof.open()
        self.tof.start_ranging(1)
        self.tof.get_distance()
        self.tof.stop_ranging()
    
    def change_address(self, address):
        self.tof.change_address(address)
        self.tof.close()
        del self.tof
        self.tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=address)
    
    def reset_address(self, xshut_pin):
        GPIO.setup(xshut_pin, GPIO.OUT)
        GPIO.output(xshut_pin, GPIO.LOW)
        GPIO.output(xshut_pin, GPIO.HIGH)

    def get_distance(self):
        time1 = time.time()
        self.tof.start_ranging(0)
        sensor_value = self.tof.get_distance()/10.0
        self.tof.stop_ranging()
        time2 = time.time()
        return sensor_value

    def get_status(self):
        pass # TODO: search for sensor range status (https://github.com/pimoroni/vl53l1x-python/tree/master)

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
    # left_tof = Tof(xshut_pin=17)
    while running:
        right_distance = right_tof.get_distance()
        # left_distance = left_tof.get_distance()
        print(f'right_distance: {right_distance}')
        # time.sleep(0.5)
