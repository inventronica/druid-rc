from roboflowoak import RoboflowOak
from follower import Follower, follower_process

import time
import numpy as np
import signal
import sys
from motors import Motors

from time import sleep
import multiprocessing


class CubeDetection:
    def __init__(self, debug=False):
        self.debug = debug
        if self.debug:
            import cv2
        self.camera = RoboflowOak(model="controled-box", confidence=0.5, 
                overlap=0.5, version="5", api_key="", rgb=True, depth=False, device=None, blocking=True)

    def update_next(self):
        result, frame, raw_frame, depth = self.camera.detect(visualize=self.debug)
        if result is not None and result is not []:
            predictions = result['predictions']
            surface = 0
            next_cube = 'unknown'
            for prediction in predictions:
                cube = prediction.json()
                if cube['width'] * cube['height'] > surface:
                    surface = cube['width'] * cube['height']
                    next_cube = cube['class']
            if surface < 1000:
                next_cube = 'unknown'
            # next_cube: 'UNKNOWN', 'red box', 'green box'

            # if self.debug:
            #     cv2.imshow("frame", frame)

            # if self.debug:
            #     if cv2.waitKey(1) == ord('q'):
            #         break
            # if once:
            #     break

            if self.debug:
                return next_cube, frame
            else:
                return next_cube


def exit_handler(signal, frame):
    global running
    running = False
    sys.exit(0)

if __name__ == '__main__':
    multiprocessing.set_start_method('fork')
    running = True
    signal.signal(signal.SIGINT, exit_handler)
    my_cube = CubeDetection()
    follow_run = multiprocessing.Value('i', 1)
    cube = multiprocessing.Value('i', 2)
    follower_process = multiprocessing.Process(target=follower_process, args=(follow_run, cube))
    try:
        follower_process.start()
        while running:
            # time1 = time.time()
            sleep(0.2)
            next_cube = my_cube.update_next()
            if next_cube == 'green box':
                cube.value = 1
            elif next_cube == 'red box':
                cube.value = 2
            else:
                pass
        my_follower.running.value = 0
        follower_process.join()
    finally:
        motors = Motors()
        motors.set_speed(0)
