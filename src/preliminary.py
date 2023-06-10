import time
import multiprocessing
# from exit_handler import exit_handler
from sensors import Tof
from sensors import Gyro, gyro_process, color_process
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
    raise Exception


class Follower:
    def __init__(self):
        self.distance = 25
        self.pid = PID(kp=5, kd=2, ki=0.1, damp=0.5)
        self.gyro_pid = PID(kp=700, kd=0, ki=0, damp=0)

        self.right_tof = Tof(address=0x33)
        self.left_tof = Tof(address=0x34, xshut_pin=17)
        self.angle = multiprocessing.Value('f', 0)
        self.gyro_run = multiprocessing.Value('i', 1)
        self.gyro_process = multiprocessing.Process(target=gyro_process, args=(self.gyro_run, self.angle))
        self.gyro_process.start()

        self.motors = Motors()

        time.sleep(1)
        self.motors.set_speed(50)

    
    def run_follower(self):
        # gyro_angle = 0
        gyro_angle = self.angle.value
        time.sleep(0.01)
        turn = int(gyro_angle /(math.pi/2))
        gyro_angle = gyro_angle - turn*math.pi/2
        error = get_error(-self.right_tof.get_distance()+self.left_tof.get_distance(), gyro_angle, wall='right', set_point=0)
        print(f'{self.right_tof.get_distance()}\t{self.left_tof.get_distance()}')
        print(f'{self.right_tof.get_distance()-self.left_tof.get_distance()=}, {error=}')
        pid_output = self.pid.get_output(error)
        self.motors.set_direction(pid_output)

    def stop_gyro(self):
        self.gyro_run.value = 0
        self.gyro_process.join()

    def set_speed(self, speed):
        self.motors.set_speed(speed)

    def run_gyro_follower(self, angle):
        current_angle = self.angle.value
        time.sleep(0.01)
        self.motors.set_speed(0)
        while current_angle == 0:
            current_angle = self.angle.value
            time.sleep(0.01)
        self.motors.set_speed(30)
        while current_angle - angle > 0.09 or current_angle - angle < -0.09:
            current_angle = self.angle.value
            time.sleep(0.01)
            error = get_error(current_angle, wall='gyro', set_point=angle)
            output = self.gyro_pid.get_output(error)
            self.motors.set_direction(output)

    def change_lane(self, lane):
        current_angle = self.angle.value
        turn = int(current_angle /(math.pi/2))
        base_angle = turn * math.pi/2
        base_turn = math.pi/4
        if lane == 2: # go to right lane
            self.run_gyro_follower(base_angle-base_turn)
            self.run_gyro_follower(base_angle)
        elif lane == 1: # go to left lane
            self.run_gyro_follower(base_angle+base_turn)
            self.run_gyro_follower(base_angle)


def follower_process(running, wall):
    my_follower = Follower()
    # my_follower.run_gyro_follower(0)
    while running.value == 1:
        my_follower.run_follower(wall.value)
    my_follower.set_speed(0)
    my_follower.stop_gyro()
        

if __name__ == "__main__":
    my_follower = Follower()
    running = True
    while running:
        my_follower.run_follower()
