from threading import Thread
from arduino_listener import ArduinoListener
import globals as g
from constant import THREAD_JOIN_TIMEOUT, MUTEX_ACQUIRE_TIMEOUT
import time
from ui import UI


class LaserSafetyRunner:

    @staticmethod
    def start_processing_arduino_data():
        from globals import data_buffer_mutex as mutex
        # 1. always acquire the mutex lock
        mutex.acquire(blocking=True, timeout=1.0)
        ###################################
        # read data into data buffer
        # CODE FOR READING DATA HERE
        ###################################

        # DEBUGGING CODE
        if g.data_buffer_mutex.locked():
            print("start_processing_arduino_data: Got buffer mutex!")
        else:
            print("start_processing_arduino_data: Failed to acquire buffer mutex!")

        # release the data buffer mutex
        mutex.release()

        # DEBUGGING CODE
        if mutex.locked():
            print("start_processing_arduino_data: Failed to release buffer mutex!")
        else:
            print("start_processing_arduino_data: Released buffer mutex!")
        pass

    @staticmethod
    def update_ui_thread():
        from globals import data_buffer_mutex as mutex
        # 1. always acquire the data buffer mutex lock
        mutex.acquire(blocking=True, timeout=MUTEX_ACQUIRE_TIMEOUT)
        # DEBUGGING CODE
        if mutex.locked():
            print("update_ui_thread: mutex acquired!")
        else:
            print("update_ui_thread: failed to acquire mutex!")
        # 2. get copy of data buffer
        buffer = g.data_buffer
        # 3. release the data buffer mutex
        mutex.release()
        if mutex.locked():
            print("update_ui_thread: Failed to release mutex!")
        else:
            print("update_ui_thread: Successfully released mutex!")

        # 4. parse data from buffer
        # 5. update states using the parsed data
        # 6. update UI if state changed from last time

    def _init_threads(self):
        g.arduino_thread = Thread(name="Arduino Thread", target=self.start_processing_arduino_data(),
                                  args=())
        g.threads.append(g.arduino_thread)
        g.ui_thread = Thread(name="UI Thread", target=LaserSafetyRunner.update_ui_thread(), args=())
        g.threads.append(g.ui_thread)

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
                if not g.arduino_thread.is_alive():
                    g.arduino_thread.start()
                # if enough time has elapsed and the thread isn't alive, spin up a ui thread update
                if time.perf_counter() - self.t0 >= 1.5 and not g.ui_thread.is_alive():
                    g.ui_thread.start()
                while g.arduino_thread.is_alive():
                    g.arduino_thread.join(THREAD_JOIN_TIMEOUT)
                while g.ui_thread.is_alive():
                    g.ui_thread.join(THREAD_JOIN_TIMEOUT)
            except BaseException:
                return False
