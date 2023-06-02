import time

class PID:
    def __init__(self, tof, gyro, kp=3.0, ki=0.05, kd=0.0, damp = 0.7, distance = 15.0):
        self.set_kpid(kp, ki, kd)
        self.set_tof(tof)
        self.set_distance(distance)
        self.integral = 0
        self.last_error = 0
        self.last_time = time.time()

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

    def set_tof(self, sensor):
        self.tof = tof

    def set_point(self, distance):
        self.distance = distance

    def reset_integral(self):
        self.integral = 0

    def reset_last_error(self):
        self.last_error = 0

    def get_output(self, gyro=1):
        delta = time.time() - self.last_time
        self.last_time = time.time()
        true_distance = self.tof.get_distance()
        error = true_distance - self.distance
        if error > 20: error = 20
        if error < -20: error = -20
        self.integral = self.integral * self.damp + (error+self.last_error)*delta/2
        derivative = (error - self.last_error)/delta
        self.last_error = error

        output = int(error*kp + self.integral*ki + derivative*kd)
        return output