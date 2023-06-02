import time
import multiprocessing
from exit_handler import exit_handler
from tof import Tof
from gyro import Gyro
from pid import PID
from motors import Motors
import math

# LOGS = True

# def setup():
#     set_tof()

# running = True
# def loop():
#     while running:
#         pass
#     # TODO: communicate between processes to get camera info
#     # output = PID_output()


if __name__ == "__main__":
    running = True
    signal.signal(signal.SIGINT, exit_handler)
    right_tof = Tof(address=0x33)
    left_tof = Tof(xshut_pin=17)
    gyro = Gyro()
    gyro_process = multiprocessing.Process(target=gyro.calculate_angle)
    gyro_process.start()
    pid = PID(right_tof)
    motors = Motors()
    motors.set_speed(60)
    while running:
        motors.set_direction(pid.get_output(math.cos(gyro.angle.value)))

    setup()
    loop()