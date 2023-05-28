# from gpiozero import Servo
import signal
import VL53L1X
import sys
import board
import adafruit_icm20x
import RPi.GPIO as GPIO
from time import sleep

# sudo apt-get install python3-rpi.gpio
# sudo pip3 install gpiozero
# sudo pip install smbus2
# sudo pip install vl53l1x
# sudo pip3 install adafruit-circuitpython-icm20x

PWML = 12
PWMR = 13

MAX_SPEED = 100
MIN_SPEED = 60
MIN_SERVO = -1.0
MAX_SERVO = 1.0
SERVO_PIN = 9

set_point = 15.0
kp = 3.0
ki = 0.05
kd = 0.0
damp = 0.5
LOGS = True

# myservo = Servo(25)

i2c = board.I2C()  # uses board.SCL and board.SDA
icm = adafruit_icm20x.ICM20948(i2c)

ledpin = 12				# PWM pin connected to LED
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BCM)		#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)
pi_pwm = GPIO.PWM(ledpin,1000)		#create PWM instance with frequency
pi_pwm.start(0)				#start PWM of required Duty Cycle 

# TODO: check for motors
GPIO.setwarnings(False)			#disable warnings
GPIO.setup(PWML,GPIO.OUT)
# left_pwm = GPIO.PWM(PWML,1000)		#create PWM instance with frequency
# GPIO.setup(PWMR,GPIO.OUT)
# right_pwm = GPIO.PWM(PWMR,1000)		#create PWM instance with frequency
# left_pwm.start(0)	
# right_pwm.start(0)


angle = 0
def get_gyro():
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % (icm.gyro))
    global angle
    x, y, z = icm.gyro   # TODO: find rotation axis
    angle += x

def set_speed(my_speed):
    if my_speed > MAX_SPEED: my_speed = MAX_SPEED
    if my_speed < -MAX_SPEED: my_speed = -MAX_SPEED
    if my_speed > 0:
        right_pwm.ChangeDutyCycle(my_speed) 
        left_pwm.ChangeDutyCycle(0) 
    elif my_speed < 0:
        right_pwm.ChangeDutyCycle(0) 
        left_pwm.ChangeDutyCycle(-my_speed) 
    else:
        right_pwm.ChangeDutyCycle(0) 
        left_pwm.ChangeDutyCycle(0) 

# You can also use the value property to move the servo to a particular position, on a scale from -1 (min) to 1 (max) where 0 is the mid-point:
# to reduce servo jitler: https://gpiozero.readthedocs.io/en/stable/api_output.html?highlight=Servo#gpiozero.Servo 

def set_direction(position):
    if position < -100: position = -100
    if position > 100: position = 100
    position = map(position, 100, -100, MIN_SERVO, MAX_SERVO)
    myservo.value = position

def set_tof():
    xshut_pin = 17 
    GPIO.setup(xshut_pin, GPIO.OUT)
    GPIO.output(xshut_pin, GPIO.HIGH)
    tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
    tof.open()
    tof.change_address(0x33)
    tof.close()
    GPIO.output(xshut_pin, GPIO.LOW)
    GPIO.output(xshut_pin, GPIO.HIGH)
    global left_tof
    global right_tof
    left_tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
    left_tof.open()
    left_tof.start_ranging(1)  # Start ranging
                               # 0 = Unchanged
                               # 1 = Short Range
                               # 2 = Medium Range
                               # 3 = Long Range
    right_tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x33)
    right_tof.open()
    right_tof.start_ranging(1)

def get_error():
    distance_in_mm = tof.get_distance()
    output = 0
    sensor_value = distance_in_mm / 10.0
    # TODO: read sensor status 
    if sensor.ranging_data.range_status != 0: sensor_value = set_point + 20
    elif sensor_value < set_point+20: sensor_value = set_point + 20
    elif sensor_value < set_point-20: sensor_value = set_point - 20
    output = sensor_value - set_point
    return (output)

def PID_output():
    error = get_error()
    integral = 0
    integral = integral * damp + error
    last_error = 0
    derivative = error - last_error
    last_error = error
    output = int(error*kp + integral*ki + derivative*kd)
    # TODO: check pwm pin output
    return output


def setup():
    set_tof()

running = True
def loop():
    while running:
        left_tof_mm = left_tof.get_distance()
        right_tof_mm = right_tof.get_distance()
        print(f'Left distance: {left_tof_mm}, Right distance: {right_tof_mm}')
        x, y, z = icm.gyro
        print(f'Gyro X: {x}, Gyro Y: {y}, Gyro Z: {z}')
        sleep(0.1)
    # TODO: read distance sensors
    # TODO: read imu sensors
    # TODO: communicate between processes to get camera info
    # output = PID_output()
    # set_speed(max(MIN_SPEED, MAX_SPEED-abs(output)))
    # set_direction(output)

def exit_handler(signal, frame):
    global running
    running = False
    left_tof.stop_ranging()
    # left_tof.close()
    right_tof.stop_ranging()
    # right_tof.close()
    print()
    sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)

if __name__ == "__main__":
    setup()
    loop()
