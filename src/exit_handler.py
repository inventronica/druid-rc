import signal
import sys

def exit_handler(signal, frame):
    global running
    running = False
    sys.exit(0)
