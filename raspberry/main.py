import time
import multiprocessing
# from exit_handler import exit_handler
from sensors import Tof
from sensors import Gyro
from sensors import Color
from pid import PID
from motors import Motors
import math
import signal
import sys

# exit handler -> used to stop the program
def exit_handler(signal, frame):
    global running
    running = False


running = True # used to stop program
if __name__ == "__main__":
    try: # gracefully close the program in finall
        signal.signal(signal.SIGINT, exit_handler) # attach exit handler

        # initialise sensors
        my_color = Color(enable_pin=25)
        right_tof = Tof(address=0x33)
        left_tof = Tof(address=0x34, xshut_pin=17)
        left_tof.change_address(0x32)
        my_color.power_on()
        gyro = Gyro()
        # start gyro process to continously calculate angle
        gyro_process = multiprocessing.Process(target=gyro.calculate_angle)
        gyro_process.start()
        # start color sensor process, so the color lines are not missed 
        color_process = multiprocessing.Process(target=color_sensor.color_read)
        color_process.start()
        # initialise main PID program
        pid = PID(left_tof, right_tof, kp=6, kd=3, ki=0.2, damp=0.5, distance=25)
        # initialise motors
        motors = Motors()
        motors.set_speed(30)
        gyro_turn = 0 # used to count the number of 90 deg turns
        while running:
            gyro_angle = gyro.angle.value
            if gyro.angle.value + gyro_turn > math.pi/2:
                gyro_turn += 1
            elif gyro.angle.value - gyro_turn < math.pi/2:
                gyro_turn -= 1
            pid_output = pid.get_output(math.cos(gyro.angle.value + gyro_turn*math.pi/2), wall='left')
            motors.set_direction(pid_output)


    finally:
        # motors.set_speed(0)
        gyro.running.value = 0 
        color.running.value = 0 
        gyro_process.join()
