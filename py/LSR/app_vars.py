from serial import Serial
from platform import system
from pygame import display, FULLSCREEN
from constant_display import DISPLAY_WIDTH, DISPLAY_HEIGHT
from asyncio import *


this_platform = system()
arduino_data_buffer = []
arduino_data_buffer_copy = []
data_buffer_mutex = Lock()
laser_safety_runner = None
com_port = ""
return_val = -1

running = True
has_port_connected_before = False
is_com_port_open = False
found_platform = False
reset_serial_connection = False
ser = Serial()
serial_count = 0
inputs_from_ard = 0


serialBuffer = [0]*30
serialCount = 0

py_img_last = ""
py_img = None
last_py_img_path = ""

close_app = False
