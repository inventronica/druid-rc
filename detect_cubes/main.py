from roboflowoak import RoboflowOak

import time
import numpy as np

# import serial
from time import sleep

DEBUG = True
if DEBUG:
    import cv2

# arduino_ser = serial.Serial("/dev/ttyS0", 9600)
kp = 3
ki = 0.15
kd = 7.5
red_box_set_point = 30
green_box_set_point = 60

def send_set_point(set_point):
    pass
    # arduino_ser.write(f'{int(set_point*1000)} {int(kp*1000)} {int(ki*1000)} {int(kd*1000)}')

if __name__ == '__main__':
    # instantiating an object (rf) with the RoboflowOak module
    rf = RoboflowOak(model="colored-box", confidence=0.4, overlap=0.5,
    version="5", api_key="MTy84oFDXUhgRs8UfIYZ", rgb=True,
    depth=False, device=None, blocking=True)
    # Running our model and displaying the video output with detections
    while True:
        if DEBUG:
            t0 = time.time()
            
        # The rf.detect() function runs the model inference
        result, frame, raw_frame, depth = rf.detect(visualize=True)
        predictions = result["predictions"]
        surface = 0
        next_cube = 'UNKNOWN'
        for prediction in predictions:
            cube = prediction.json()
            if cube['width'] * cube['height'] > surface:
                surface = cube['width'] * cube['height']
                next_cube = cube['class']
        if next_cube == 'UNKNOWN':
            pass
        elif next_cube == 'red box':
            send_set_point(red_box_set_point)
            if DEBUG:
                print('========  RED BOX NEXT  ==========')
        elif next_cube == 'green box':
            if DEBUG:
                print('========  GREEN BOX NEXT  ========')
            send_set_point(green_box_set_point)

        if DEBUG:
            cv2.imshow("frame", frame)

        if DEBUG:
            if cv2.waitKey(1) == ord('q'):
                break

