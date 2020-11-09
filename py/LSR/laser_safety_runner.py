# imports
from threading import Thread
from arduino_listener import ArduinoListener
import app_vars as av
from constant import THREAD_JOIN_TIMEOUT, MUTEX_ACQUIRE_TIMEOUT
import time
from ui import UI


############################################################################
# Class: LaserSafetyRunner
# Description: manages the multi-threading capability of the app.
############################################################################
class LaserSafetyRunner:
    ######################################################################
    # Name: start_processing_arduino_data
    # Description: method to point the arduino thread at to execute.
    #              Acquires mutex, gets ard data, then releases the mutex
    ######################################################################
    @staticmethod
    def start_processing_arduino_data():
        # 1. always acquire the mutex lock
        av.data_buffer_mutex.acquire(blocking=True, timeout=1.0)
        ###################################
        # read data into data buffer
        # CODE FOR READING DATA HERE
        ###################################

        # DEBUGGING CODE
        if av.data_buffer_mutex.locked():
            print("start_processing_arduino_data: Got buffer mutex!")
        else:
            print("start_processing_arduino_data: Failed to acquire buffer mutex!")

        # release the data buffer mutex
        av.data_buffer_mutex.release()

        # DEBUGGING CODE
        if av.data_buffer_mutex.locked():
            print("start_processing_arduino_data: Failed to release buffer mutex!")
        else:
            print("start_processing_arduino_data: Released buffer mutex!")

    ######################################################################
    # Name: update_ui_thread
    # Description: method to point the ui thread at to execute.
    #              Acquires mutex, gets buffer data, releases mutex, then
    #              the data is parsed, evaluated, and the ui is updated
    ######################################################################
    @staticmethod
    def update_ui_thread():
        # 1. always acquire the data buffer mutex lock
        av.data_buffer_mutex.acquire(blocking=True, timeout=MUTEX_ACQUIRE_TIMEOUT)
        # DEBUGGING CODE
        if av.data_buffer_mutex.locked():
            print("update_ui_thread: mutex acquired!")
        else:
            print("update_ui_thread: failed to acquire mutex!")
        # 2. get copy of data buffer
        buffer = av.data_buffer
        # 3. release the data buffer mutex
        av.data_buffer_mutex.release()
        if av.data_buffer_mutex.locked():
            print("update_ui_thread: Failed to release mutex!")
        else:
            print("update_ui_thread: Successfully released mutex!")

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
        av.arduino_thread = Thread(name="Arduino Thread", target=self.start_processing_arduino_data(),
                                   args=())
        av.threads.append(av.arduino_thread)
        av.ui_thread = Thread(name="UI Thread", target=LaserSafetyRunner.update_ui_thread(), args=())
        av.threads.append(av.ui_thread)

    def __init__(self):
        self._init_threads()
        self.t0 = time.perf_counter()
        # init the mutex for the data buffer
        # init arduino listener and UI objects
        self.ard_listener = ArduinoListener()
        self.ui = UI()

    def run(self):
        while True:
            try:
                self._init_threads()
                # if arduino listener thread isn't alive, spin one up
                if not av.arduino_thread.is_alive():
                    av.arduino_thread.start()
                # if enough time has elapsed and the thread isn't alive, spin up a ui thread update
                if time.perf_counter() - self.t0 >= 1.5 and not av.ui_thread.is_alive():
                    # reset base time reference
                    self.t0 = time.perf_counter()
                    av.ui_thread.start()
                if av.arduino_thread.is_alive():
                    av.arduino_thread.join(THREAD_JOIN_TIMEOUT)
                if av.ui_thread.is_alive():
                    av.ui_thread.join(THREAD_JOIN_TIMEOUT)

            except BaseException:
                return False
