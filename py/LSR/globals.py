import constant as c
from threading import Thread, Lock

data_buffer = [] * c.DATA_PACKET_SIZE
data_buffer_mutex = Lock()
laser_safety_runner = None
arduino_thread: Thread
ui_thread: Thread
threads = []

