# imports
from threading import Thread
from arduino_serial_manager import ArduinoSerialManager
import app_vars as av
from constant_serial import *
from serial_util import is_port_set
from constant_display import BASE_UI_REFRESH_RATE
from time import perf_counter, sleep
# from display import Display


############################################################################
# Class: LaserSafetyRunner
# Description: manages the multi-threading capability of the app.
############################################################################
class LaserSafetyRunner:

    def init_serial_to_arduino(self):
        # get mutex so other threads wait their turn
        av.data_buffer_mutex.acquire(blocking=True, timeout=MUTEX_ACQUIRE_TIMEOUT_ARDUINO)
        if self.ard_listener.determine_platform_and_connect():
            print("Connected successfully to com port: " + av.com_port)
        # always release mutex before returning
        av.data_buffer_mutex.release()

    def __init__(self):
        # self.display = Display()
        self.ard_listener = ArduinoSerialManager()

        # initialize the ui and arduino threads
        # initialize the base time reference
        self.t0 = perf_counter()
        # init arduino listener and UI objects

        # self.display.update_display()
        self.init_serial_to_arduino()

    def run(self):
        arduino_thread = None
        while True:
            try:
                if arduino_thread is None or not arduino_thread.is_alive():
                    arduino_thread = Thread(name="Arduino Thread",
                                                 target=self.ard_listener.start_reading_from_serial(), args=(),
                                                 daemon=True)
                    arduino_thread.start()

                arduino_thread.join(0.5)
                if av.reset_serial_connection:
                    self.init_serial_to_arduino()
                    av.reset_serial_connection = False


                # if arduino_thread.is_alive():
                #     print("ard thread is alive")
                # else:
                #     print("ard thread is ded")
                # if not self.display_thread.is_alive() and not self.arduino_thread.is_alive() and\
                #         perf_counter() - self.t0 >= BASE_UI_REFRESH_RATE:
                #     self.t0 = perf_counter()
                #     self.display_thread = Thread(name="Display Thread", target=self.display.update_display(), args=(),
                #     daemon=True)
                #     self.threads.append(self.display_thread)
                #     self.display_thread.start()

                # if self.display_thread.is_alive():
                #     self.display_thread.join(THREAD_JOIN_DISPLAY_TIMEOUT)
            except BaseException:
                from traceback import print_exc
                print_exc()
                return False
