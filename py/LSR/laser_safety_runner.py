# imports
from threading import Thread
from multiprocessing import Process
from arduino_serial_manager import ArduinoSerialManager
import app_vars as av
import asyncio
import os
from constant_serial import *
from constant_display import WAITING_FOR_INPUT_DEVICE_MSG
from serial_util import is_port_set
from constant_display import BASE_UI_REFRESH_RATE
from time import perf_counter
from display import Display


############################################################################
# Class: LaserSafetyRunner
# Description: manages the multi-threading capability of the app.
############################################################################
class LaserSafetyRunner:

    def init_serial_to_arduino(self):
        flag = False
        while not flag:
            flag = self.ard_listener.determine_platform_and_connect()
            if flag:
                av.is_com_port_open = True
                if av.has_port_connected_before is None:
                    av.has_port_connected_before = False
                else:
                    av.has_port_connected_before = True
                av.found_platform = True
                self.display.display_system_waiting(WAITING_FOR_INPUT_DEVICE_MSG, True)
                print("\nis port set:" + str(is_port_set()))
                print("Connected successfully to com port: " + av.com_port)
            else:
                print("no ard response...")

    def __init__(self):
        self.display = Display()
        self.display.update_pygame_image()
        self.ard_listener = ArduinoSerialManager()

        # initialize the ui and arduino threads
        # initialize the base time reference
        # init arduino listener and UI objects

    def run(self):
        arduino_process = None
        while True:
            if not av.ser.is_open:
                self.init_serial_to_arduino()
            try:
                # self.display.update_display()
                if arduino_process is None or arduino_process.is_alive():
                    arduino_process = Process(name="Arduino Process",
                                              target=self.ard_listener.start_reading_from_serial(),
                                              args=(av.return_val,), daemon=True)

                    arduino_process.start()
                # check to see if serial connection reset flag is set
                else:
                    result = []
                    print("len result val: " + str(len(av.return_val)))
                    if len(av.return_val) > 0:
                        result = av.return_val[len(av.return_val)-1]
                    # self.display.update_display(result)
                    print("return val: "+str(result))
                    arduino_process.join()
                    arduino_process = None
            except BaseException:
                from traceback import print_exc
                print_exc()
                return False

