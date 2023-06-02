import RPi.GPIO as GPIO
from gpiozero import Servo
from exit_handler import exit_handler
import signal

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)			#disable warnings

class Motors:
    MAX_SPEED = 100
    MIN_SPEED = 60
    MIN_SERVO = -1.0
    MAX_SERVO = 1.0
    #pin for motors
    PWML = 12
    PWMR = 13
    SERVO_PIN = 9

    def __init__(self):
        self.myservo = Servo(SERVO_PIN)
        GPIO.setup(PWML, GPIO.OUT)
        GPIO.setup(PWMR, GPIO.OUT)

        self.left_pwm = GPIO.PWM(PWML, 1000)		#create PWM instance with frequency
        self.right_pwm = GPIO.PWM(PWMR, 1000)		#create PWM instance with frequency
        self.left_pwm.start(0)	
        self.right_pwm.start(0)


    def set_speed(self, my_speed):
        if my_speed > MAX_SPEED: my_speed = MAX_SPEED
        if my_speed < -MAX_SPEED: my_speed = -MAX_SPEED
        if my_speed > 0:
            self.right_pwm.ChangeDutyCycle(my_speed) 
            self.left_pwm.ChangeDutyCycle(0) 
        elif my_speed < 0:
            self.right_pwm.ChangeDutyCycle(0) 
            self.left_pwm.ChangeDutyCycle(-my_speed) 
        else:
            self.right_pwm.ChangeDutyCycle(0) 
            self.left_pwm.ChangeDutyCycle(0) 

    # You can also use the value property to move the servo to a particular position, on a scale from -1 (min) to 1 (max) where 0 is the mid-point:
    # to reduce servo jitler: https://gpiozero.readthedocs.io/en/stable/api_output.html?highlight=Servo#gpiozero.Servo 

    def set_direction(self, position):
        if position < -100: position = -100
        if position > 100: position = 100
        position = map(position, 100, -100, MIN_SERVO, MAX_SERVO)
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
    # calibrate servo
    while running:
        calibrate_servo(motors)
    # test motor speed
    # while running:
    #     test_speed(motors)