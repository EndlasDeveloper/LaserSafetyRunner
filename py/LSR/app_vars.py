from serial import Serial
from threading import Thread, Lock
from platform import system
from pygame import display, FULLSCREEN
from constant import DISPLAY_WIDTH, DISPLAY_HEIGHT

this_platform = system()
data_buffer = []
data_buffer_mutex = Lock()
laser_safety_runner = None
com_port = ""

has_port_connected_before = False
is_com_port_open = False
found_platform = False
ser = Serial()
serial_count = 0
inputs_from_ard = 0
main_canvas = display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), FULLSCREEN)

py_img_last = ""
py_img = None
last_py_img_path = ""
