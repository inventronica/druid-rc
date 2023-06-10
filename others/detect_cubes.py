from roboflowoak import RoboflowOak

import time
import numpy as np
import signal
import sys

from time import sleep
import multiprocessing


class CubeDetection:
    def __init__(self, debug=True):
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
            if surface < 1200:
                next_cube = 'unknown'
            # next_cube: 'UNKNOWN', 'red box', 'green box'

            if self.debug:
                cv2.imshow("frame", frame)
                print(f'{next_cube=}')

            if self.debug:
                if cv2.waitKey(1) == ord('q'):
                    pass
            if once:
                pass

            if self.debug:
                return next_cube, frame
            else:
                return next_cube


def exit_handler(signal, frame):
    global running
    running = False
    sys.exit(0)

if __name__ == '__main__':
    running = True
    signal.signal(signal.SIGINT, exit_handler)
    my_cube = CubeDetection()
    while running:
        time1 = time.time()
        next_cube = my_cube.update_next()
        print(f'{next_cube=}')
        # print(f'{next_cube=}\ttime_between_loops={time.time()-time1}\t{surface=}')
