# imports
from threading import Thread
from arduino_listener import ArduinoListener
import app_vars as av
from constant import *
from time import perf_counter
from ui import UI
import random


############################################################################
# Class: LaserSafetyRunner
# Description: manages the multi-threading capability of the app.
############################################################################
class LaserSafetyRunner:

    def init_serial_to_arduino(self):
        # get mutex so other threads wait their turn
        av.data_buffer_mutex.acquire(blocking=True, timeout=MUTEX_ACQUIRE_TIMEOUT)
        if self.ard_listener.determine_platform_and_connect():
            print("Connected to com successfully")
        # always release mutex before returning
        av.data_buffer_mutex.release()

    ######################################################################
    # Name: update_ui_thread
    # Description: method to point the ui thread at to execute.
    #              Acquires mutex, gets buffer data, releases mutex, then
    #              the data is parsed, evaluated, and the ui is updated
    ######################################################################
    def update_ui_thread(self):
        # 1. always acquire the data buffer mutex lock

        print("data buffer: " + str(av.data_buffer))
        # # DEBUGGING CODE
        # if av.data_buffer_mutex.locked():
        #     print("update_ui_thread: mutex acquired!")
        # else:
        #     print("update_ui_thread: failed to acquire mutex!")
        # 2. get copy of data buffer
        self.ui.update_ui()
        # 3. release the data buffer mutex

        # # DEBUGGING CODE
        # if av.data_buffer_mutex.locked():
        #     print("update_ui_thread: Failed to release mutex!")
        # else:
        #     print("update_ui_thread: Successfully released mutex!")

        ###############################################################
        # 4. parse data from buffer
        # 5. update states using the parsed data
        # 6. update UI if state changed from last time
        ###############################################################

    #######################################################################################################
    # Name: _init_threads
    # Description: initializes the threads with the proper target methods and names
    #######################################################################################################
    def _init_threads(self):
        self.arduino_thread = Thread(name="Arduino Thread", target=self.ard_listener.read_input_bytes(), args=())
        self.threads.append(self.arduino_thread)
        self.ui_thread = Thread(name="UI Thread", target=self.update_ui_thread(), args=())
        self.threads.append(self.ui_thread)

    def __init__(self):
        self.ui = UI()
        self.ard_listener = ArduinoListener()
        self.arduino_thread: Thread = Thread()
        self.ui_thread: Thread = Thread()

        self.threads = []
        self._init_threads()
        # init data buffer arr to size of data packets
        for i in range(DATA_PACKET_SIZE):
            av.data_buffer.append(0)

        # initialize the ui and arduino threads
        # initialize the base time reference
        self.t0 = perf_counter()
        # init arduino listener and UI objects

        self.ui.update_ui()
        self.init_serial_to_arduino()

    def run(self):
        self._init_threads()
        while True:
            try:
                if not self.arduino_thread.is_alive():
                    self.arduino_thread = Thread(name="Arduino Thread", target=self.ard_listener.read_input_bytes(), args=())
                    self.threads.append(self.arduino_thread)
                    self.arduino_thread.start()

                if not self.ui_thread.is_alive() and perf_counter() - self.t0 >= BASE_UI_REFRESH_RATE:
                    self.t0 = perf_counter()
                    self.ui_thread = Thread(name="UI Thread", target=self.update_ui_thread(), args=())
                    self.threads.append(self.ui_thread)
                    self.ui_thread.start()

                if self.arduino_thread.is_alive():
                    self.arduino_thread.join(THREAD_JOIN_TIMEOUT)
                if self.ui_thread.is_alive():

                    self.ui_thread.join(THREAD_JOIN_TIMEOUT)
            except BaseException:
                return False
