import time

class PID:
    def __init__(self, left_tof=None, right_tof=None, kp=5.0, ki=0.05, kd=0.0, damp = 0.7, distance = 25.0):
        self.set_kpid(kp, ki, kd)
        self.set_tof(left_tof, right_tof)
        self.set_distance(distance)
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

    def set_distance(self, distance):
        self.distance = distance
    
    def set_kpid(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

    def set_tof(self, left_tof, right_tof):
        self.left_tof = left_tof
        self.right_tof = right_tof

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



    def get_output(self, gyro=1, wall='left'):
        delta = time.time() - self.last_time
        self.last_time = time.time()
        if self.left_tof is None and self.right_tof is None:
            print("(PID MODULE) ERROR NO SENSOR ATTACHED")
            return None
        
        if self.left_tof == None:
            print("(PID MODULE) WARNING ONLY LEFT SENSOR ATTACHED")
            true_distance = self.tof.get_distance()
            if true_distance is None:
                error = 20
            else:
                error = true_distance - self.distance
        elif self.right_tof == None:
            print("(PID MODULE) WARNING ONLY RIGHT SENSOR ATTACHED")
            true_distance = self.tof.get_distance()
            if true_distance is None:
                error = 20
            else:
                error = self.distance - true_distance
        else: 
            if wall == 'left':
                true_distance = self.left_tof.get_distance()
                if self.right_tof.get_distance() is None:
                    error = 20
                elif true_distance is None:
                    error = -20
                else:
                    error = true_distance - self.distance
            if wall == 'right':
                true_distance = self.right_tof.get_distance()
                if true_distance is None:
                    error = 20
                else:
                    error = self.distance - true_distance
            
        if error > 20: error = 20
        if error < -20: error = -20

        self.integral = self.integral * self.damp + (error+self.last_error)*delta/2
        derivative = (error - self.last_error)/delta
        self.last_error = error

        output = int(error*self.kp + self.integral*self.ki + derivative*self.kd)
        print(f"Distance: {true_distance} output: {output}")
        return output
