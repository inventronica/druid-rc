from gpiozero import Servo
import VL53L1X
import board
import adafruit_icm20x
import RPi.GPIO as GPIO
from time import sleep

# sudo apt-get install python3-rpi.gpio
# sudo pip3 install gpiozero
# sudo pip install smbus2
# sudo pip install vl53l1x
# sudo pip3 install adafruit-circuitpython-icm20x



S0 = 40
S1 = 41
S2 = 42
S3 = 43
Color_Out = 44

PWML = 5
PWMR = 6

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

myservo = Servo(25)
tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof.open()
tof.start_ranging(1)  # Start ranging
                      # 0 = Unchanged
                      # 1 = Short Range
                      # 2 = Medium Range
                      # 3 = Long Range

i2c = board.I2C()  # uses board.SCL and board.SDA
icm = adafruit_icm20x.ICM20948(i2c)

ledpin = 12				# PWM pin connected to LED
GPIO.setwarnings(False)			#disable warnings
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)
pi_pwm = GPIO.PWM(ledpin,1000)		#create PWM instance with frequency
pi_pwm.start(0)				#start PWM of required Duty Cycle 

# TODO: update for motors


angle = 0
def get_gyro():
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f rads/s" % (icm.gyro))
    global angle
    x, y, z = icm.gyro   # TODO: find rotation axis
    angle += x


def setup():
    # TODO: define all pins
    pass

def set_speed(my_speed):
    if my_speed > MAX_SPEED: my_speed = MAX_SPEED
    if my_speed < -MAX_SPEED: my_speed = -MAX_SPEED
    if my_speed > 0:
        # TODO: control motors
        pass
    elif my_speed < 0:
        pass
    else:
        pass

# You can also use the value property to move the servo to a particular position, on a scale from -1 (min) to 1 (max) where 0 is the mid-point:
# to reduce servo jitler: https://gpiozero.readthedocs.io/en/stable/api_output.html?highlight=Servo#gpiozero.Servo 

def set_direction(position):
    if position < -100: position = -100
    if position > 100: position = 100
    position = map(position, 100, -100, MIN_SERVO, MAX_SERVO)
    myservo.value = position



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

while True:
    # TODO: read distance sensors
    # TODO: read imu sensors
    # TODO: communicate between processes to get camera info
    output = PID_output()
    set_speed(max(MIN_SPEED, MAX_SPEED-abs(output)))
    set_direction(output)

