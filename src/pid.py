import time
import math

class PID:
    def __init__(self, kp=5.0, ki=0.05, kd=0.0, damp = 0.7):
        self.set_kpid(kp, ki, kd)
        self.integral = 0
        self.last_error = 0
        self.last_time = time.time()
        self.set_damp(damp)

    def set_kp(self, kp):
        self.kp = kp

    def set_ki(self, ki):
        self.ki = ki

    def set_kd(self, kd):
        self.kd = kd

    def set_damp(self, damp):
        self.damp = damp

    def set_kpid(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def set_point(self, distance):
        self.distance = distance

    def reset_integral(self):
        self.integral = 0

    def reset_last_error(self):
        self.last_error = 0

    def get_output(self, error):
        current_time = time.time()
        delta = current_time  - self.last_time
        self.last_time = current_time
        
        self.integral = self.integral * self.damp + (error+self.last_error)*delta/2
        derivative = (error - self.last_error)/delta
        self.last_error = error

        output = int(error*self.kp + self.integral*self.ki + derivative*self.kd)
        return output



def get_error(distance, gyro=0, wall='left', set_point=20):
    gyro = 0
    if distance is not None:
        distance = distance * math.cos(gyro)
    if wall == 'left':
        if distance is None:
            error = i20
        else:
            error = set_point - distance * math.cos(gyro)
    if wall == 'right':
        if distance is None:
            error = 20
        else:
            error = distance * math.cos(gyro) - set_point
    if wall == 'gyro':
        error = distance-set_point
        
    if error > 20: error = 20
    if error < -20: error = -20

    return error 
