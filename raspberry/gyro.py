import multiprocessing
import adafruit_icm20x
import time
import signal
from exit_handler import exit_handler
import board

class Gyro:
    def __init__(self):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self._icm = adafruit_icm20x.ICM20948(i2c)
        self.angle = multiprocessing.Value('f', 0)
        self._last_speed = 0
        self._time = time.time()
        self.running = multiprocessing.Value('i', 1)

    def calculate_angle(self):
        while self.running:
            new_time = time.time()
            delta = new_time - self._time
            self._time = new_time
            x, y, z = self._icm.gyro
            self.angle.value = (self._last_speed + z)*delta/2
            self._last_speed = z


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_handler)
    running = True
    gyro = Gyro()
    gyro_process = multiprocessing.Process(target=gyro.calculate_angle)
    gyro_process.start()
    # gyro_process.join()
    while running:
        print(f'Gyro value: {gyro.angle.value}')
        time.sleep(1)
    gyro_process.running.value = False
    gyro_process.join()