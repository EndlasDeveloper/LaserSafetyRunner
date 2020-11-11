# imports
from threading import Thread
from arduino_listener import ArduinoListener
import app_vars as av
from constant_serial import *
from constant_display import BASE_UI_REFRESH_RATE
from time import perf_counter
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
        self.ard_listener = ArduinoListener()
        self.arduino_thread: Thread = Thread()
        self.display_thread: Thread = Thread()
        self.threads = []
        # init data buffer arr to size of data packets
        for i in range(DATA_PACKET_SIZE):
            av.data_buffer.append(0)

        # initialize the ui and arduino threads
        # initialize the base time reference
        self.t0 = perf_counter()
        # init arduino listener and UI objects

        # self.display.update_display()
        self.init_serial_to_arduino()

    def run(self):
        while True:
            try:
                if not self.arduino_thread.is_alive() or self.arduino_thread is None:
                    self.arduino_thread = Thread(name="Arduino Thread",
                                                 target=self.ard_listener.start_reading_from_serial(), args=())
                    self.threads.append(self.arduino_thread)
                    self.arduino_thread.start()

                # if not self.display_thread.is_alive() and not self.arduino_thread.is_alive() and\
                #         perf_counter() - self.t0 >= BASE_UI_REFRESH_RATE:
                #     self.t0 = perf_counter()
                #     self.display_thread = Thread(name="Display Thread", target=self.display.update_display(), args=())
                #     self.threads.append(self.display_thread)
                #     self.display_thread.start()

                if self.arduino_thread.is_alive():
                    self.arduino_thread.join(THREAD_JOIN_ARDUINO_TIMEOUT)
                # if self.display_thread.is_alive():
                #     self.display_thread.join(THREAD_JOIN_DISPLAY_TIMEOUT)
            except BaseException:
                return False
