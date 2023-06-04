import time
import multiprocessing
# from exit_handler import exit_handler
from tof_adafruit import Tof
from gyro import Gyro
from pid import PID
from motors import Motors
import math
import signal
import sys


def exit_handler(signal, frame):
    global running
    running = False

if __name__ == "__main__":
    try:
        global running
        running = True
        signal.signal(signal.SIGINT, exit_handler)
        right_tof = Tof(address=0x33)
        left_tof = Tof(xshut_pin=17)
        gyro = Gyro()
        gyro_process = multiprocessing.Process(target=gyro.calculate_angle)
        gyro_process.start()
        pid = PID(left_tof, right_tof, kp=6, kd=3, ki=0.2, damp=0.5, distance=25)
        motors = Motors()
        time.sleep(1)
        motors.set_speed(0)
        gyro_turn = 0
        while running:
            time1 = time.time()
            gyro_angle = gyro.angle.value
            if gyro.angle.value + gyro_turn > math.pi/2:
                gyro_turn += 1
            elif gyro.angle.value - gyro_turn < math.pi/2:
                gyro_turn -= 1
            pid_output = pid.get_output(math.cos(gyro.angle.value + gyro_turn*math.pi/2), wall='left')
            motors.set_direction(pid_output)
    finally:
        # motors.set_speed(0)
        gyro.running.value = False
        gyro_process.join()
