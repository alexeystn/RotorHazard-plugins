'''Serial clock'''

from eventmanager import Evt
import time
import datetime
import Config
import serial
import threading


def clock_thread():
    port = Config.LED['CLOCK_PORT']
    with serial.Serial(port, 115200) as ser:
        new_time = int(time.time())
        while True:        
            prev_time = new_time
            while prev_time == new_time:
                new_time = int(time.time())
                time.sleep(0.1)
            now = datetime.datetime.now()
            string = now.strftime("%H%M%S\n")
            ser.write(string.encode())


def clock_startup(args):    
    thread1 = threading.Thread(target=clock_thread)
    thread1.start()


def initialize(rhapi):
    rhapi.events.on(Evt.ACTIONS_INITIALIZE, clock_startup)
