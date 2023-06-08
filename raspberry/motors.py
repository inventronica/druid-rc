import RPi.GPIO as GPIO
import time
from gpiozero import Servo
from exit_handler import exit_handler
import signal
import pigpio

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)			#disable warnings

class Motors:
    MAX_SPEED = 100
    MIN_SPEED = 5
    MIN_SERVO = -0.75
    MAX_SERVO = 0.75
    #pin for motors
    PWML = 12
    PWMR = 13
    SERVO_PIN = 18

    def __init__(self):
        self.myservo = Servo(self.SERVO_PIN)
        GPIO.setup(self.PWML, GPIO.OUT)
        GPIO.setup(self.PWMR, GPIO.OUT)

        self.left_pwm = GPIO.PWM(self.PWML, 50)		#create PWM instance with frequency
        self.right_pwm = GPIO.PWM(self.PWMR, 50)		#create PWM instance with frequency
        self.left_pwm.start(0)	
        self.right_pwm.start(0)
        self.pi = pigpio.pi()
        self.pi.set_PWM_frequency(self.PWML, 50)
        self.pi.set_PWM_frequency(self.PWMR, 50)
        self.pi.set_mode(self.PWML, pigpio.OUTPUT)
        self.pi.set_mode(self.PWMR, pigpio.OUTPUT)

    def set_speed(self, my_speed):
        if my_speed > self.MAX_SPEED: my_speed = self.MAX_SPEED #
        if my_speed < -self.MAX_SPEED: my_speed = -self.MAX_SPEED
        # my_speed = my_speed*10
        if my_speed > 0:
            # self.pi.pwmWrite(self.PWML, my_speed)
            # self.pi.digitalWrite(self.PWMR, 0)
            self.right_pwm.ChangeDutyCycle(my_speed) 
            self.left_pwm.ChangeDutyCycle(0) 
        elif my_speed < 0:
            # self.pi.pwmWrite(self.PWMR, -my_speed)
            # self.pi.digitalWrite(self.PWML, 0)
            self.right_pwm.ChangeDutyCycle(0) 
            self.left_pwm.ChangeDutyCycle(-my_speed) 
        else:
            # self.pi.digitalWrite(self.PWML, 0)
            # self.pi.digitalWrite(self.PWMR, 0)
            self.right_pwm.ChangeDutyCycle(0) 
            self.left_pwm.ChangeDutyCycle(0) 

    # You can also use the value property to move the servo to a particular position, on a scale from -1 (min) to 1 (max) where 0 is the mid-point:
    # to reduce servo jitler: https://gpiozero.readthedocs.io/en/stable/api_output.html?highlight=Servo#gpiozero.Servo 

    def set_direction(self, position):
        if position < -100: position = -100
        if position > 100: position = 100
        my_map = lambda a, b, c, d, e: (a-b) * (e-d) / (c-b) + d
        position = my_map(position, 100, -100, self.MIN_SERVO, self.MAX_SERVO)
        self.myservo.value = position

    def set_raw_position(self, position):
        self.myservo.value = position

def calibrate_servo(motors):
    position = float(input("Introduce servo position:"))
    motors.set_raw_position(position)

def test_speed(motors):
    speed = int(input("Introduce motor speed:"))
    motors.set_speed(speed)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, exit_handler)
    motors = Motors()
    running = True
    motors.set_speed(0)
    # calibrate servo
    # while running:
    #     calibrate_servo(motors)
    # test motor speed
    while running:
       test_speed(motors)
    motors.set_speed(0)
