import time
import multiprocessing
# from exit_handler import exit_handler
from sensors import Tof
from sensors import Gyro
from sensors import Color
from pid import PID, get_error
from motors import Motors
import math
import signal
import sys

# exit handler -> used to stop the program
def exit_handler(signal, frame):
    global running
    running = False


class Follower:
    def __init__(self):
        # self.color = Color(enable_pin=25)
        self.right_tof = Tof(address=0x33)
        self.left_tof = Tof(address=0x34, xshut_pin=17)
        # self.my_color.power_on()
        self.gyro = Gyro()
        # start gyro process to continously calculate angle
        self.gyro_process = multiprocessing.Process(target=self.gyro.calculate_angle)
        self.gyro_process.start()
        # start color sensor process, so the color lines are not missed 
        # self.color_process = multiprocessing.Process(target=my_color.color_read)
        # self.color_process.start()

        self.motors = Motors()

        self.motors.set_speed(30)

        self.running = multiprocessing.Value('i', 1)
        self.side = multiprocessing.Value('i', 2)
    
    def run_follower(self):
        while self.running:
            gyro_angle = gyro.angle.value
            turn = int(gyro_angle / math.pi/2)
            gyro_angle = gyro_angle - turn*math.pi/2
            if self.side.value == 2:
                error = get_error(self.right_tof.get_distance(), gyro_angle, wall='right', set_point=20)
            else:
                error = get_error(self.left_tof.get_distance(), gyro_angle, wall='left', set_point=20)
            pid_output = pid.get_output(error)
            motors.set_direction(pid_output)
        self.gyro.running = 0
        self.gyro_process.join()
        # self.color.running = 0
        # self.color_process.join()

    def set_speed(self, speed):
        self.motors.set_speed(speed)
        
        
        

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handler) # attach exit handler
    running = True # used to stop program
    try: # gracefully close the program in finall

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
        color_process = multiprocessing.Process(target=my_color.color_read)
        color_process.start()
        # initialise main PID program
        pid = PID(left_tof, right_tof, kp=6, kd=3, ki=0.2, damp=0.5, distance=25)
        # initialise motors
        motors = Motors()
        motors.set_speed(30)
        gyro_turn = 0 # used to count the number of 90 deg turns
        while running:
            gyro_angle = gyro.angle.value
            turn = int(gyro_angle / (math.pi/2))
            gyro_angle = gyro_angle - turn*math.pi/2
            # print(f'{gyro_angle=}, {turn=}')
            # time.sleep(0.5)
            error = get_error(right_tof.get_distance(), gyro_angle, wall='right', set_point=20)
            pid_output = pid.get_output(error)
            # print(f'{gyro_turn=} {right_tof.get_distance()=} {gyro_angle=}, {error=}, {pid_output=}')
            motors.set_direction(pid_output)
    finally:
        # motors.set_speed(0)
        gyro.running.value = 0 
        my_color.running.value = 0 
        gyro_process.join()
        color_process.join()
