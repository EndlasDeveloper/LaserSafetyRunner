#########################################################
# File: app_vars.py
# Description: holds shared variables for the python app
#########################################################
import pygame

arduino_data_buffer = []
laser_safety_runner = None
com_port = ""
shared_state = -1

running = True
has_port_connected_before = False
is_com_port_open = False
found_platform = False
serial_count = 0
inputs_from_ard = 0

py_img_last = ""
py_img = None
last_py_img_path = ""

close_app = False

# to get pygame to display full screen, must set display w and h to 640, 480 and set full screen flag
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
main_canvas = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)
