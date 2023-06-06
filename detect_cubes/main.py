from roboflowoak import RoboflowOak

import time
import numpy as np
import signal
import sys

# import serial
from time import sleep
import multiprocessing


class CubeDetection:
    def __init__(self, debug=False):
        self.debug = debug
        self.next_cube = multiprocessing.Value('i', 0)
        self.running = multiprocessing.Value('i', 1)
        if self.debug:
            import cv2

    def update_next(self, once=False):
        print("update next entry")
        self.camera = RoboflowOak(model="controled-box", confidence=0.5, 
                overlap=0.5, version="5", api_key="", rgb=True, depth=False, device=None, blocking=True)
        while self.running.value == 1:
            print("update next loop")
            result, frame, raw_frame, depth = self.camera.detect(visualize=self.debug)
            print(result)
            predictions = result['predictions']
            surface = 0
            next_cube = 'unknown'
            for prediction in predictions:
                cube = prediction.json()
                if cube['width'] * cube['height'] > surface:
                    surface = cube['width'] * cube['height']
                    next_cube = cube['class']
            if next_cube == 'unknown':
                self.next_cube.value = 0
            elif next_cube == 'green box':
                self.next_cube.value = 1
            elif next_cube == 'red box':
                self.next_cube.value = 2
            else:
                self.next_cube.value = -1
            # next_cube: 'UNKNOWN', 'red box', 'green box'

            if self.debug:
                cv2.imshow("frame", frame)
                print(f'{next_cube=}')

            if self.debug:
                if cv2.waitKey(1) == ord('q'):
                    break
            if once:
                break

def exit_handler(signal, frame):
    global running
    running = False
    sys.exit(0)

if __name__ == '__main__':
    running = True
    signal.signal(signal.SIGINT, exit_handler)
    my_cube = CubeDetection()
    cube_process = multiprocessing.Process(target=my_cube.update_next)
    cube_process.start()
    while running:
        next_cube = my_cube.next_cube.value
        if next_cube == 0:
            pass
            # print("Unknown")
        elif next_cube == 1:
            print("Green")
        elif next_cube == 2:
            print("Red")
        else:
            print(f"ERROR: UNKNOWN DETECTION?!! CODE: {next_cube.value}")
        sleep(1)
    my_cube.running.value = 0
    cube_process.join()


