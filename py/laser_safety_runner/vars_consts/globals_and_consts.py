############################################################################
# globals_and_consts.py - contains most of the constants for the laser_safety_runner
############################################################################

# imports
import pygame
import datetime as dt
import serial

# SYSTEMS
WIN = 'Windows'
RASP = 'raspberrypi'
LIN = 'Linux'

# COM PORT AND PORT SPECS
COM_PORT = ""
CONTACT_TO_ARD_FLAG_BYTE = b'/xAA'
RESET_COUNTS_FLAG_BYTE = b'/x99'

# COM PORT AND PORT SPECS
BAUD_RATE = 115200
BYTE_SIZE = 8
SERIAL_TIMEOUT = 2
READ_BYTE_SIZE = 6


# LITTLE OR BIG ENDIAN
ENDIAN = "big"

# FONT
DISPLAY_FONT = 'freesansbold.ttf'
DISPLAY_FONT_SIZE = 40

# MSG
DISPLAY_CAPTION_MSG = "LASER SAFETY RUNNER"
WAITING_FOR_INPUT_DEVICE_MSG = "Waiting for input device reply..."
OPENING_COM_PORTS_MSG = "Finding open COM port..."

# to get pygame to display full screen, must set display w and h to 640, 480 and set full screen flag
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

img = None

# not actually constants, but need to be away from main
ser = serial.Serial()
has_port_connected = False
is_com_port_open = False
found_platform = False

# initialize countdown for checking the arduino
last_clock = dt.datetime.now()
serial_in_buffer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
serial_count = 0
inputs_from_ard = 0
COM_PORT_INDEX = int(1)
COM_PORT_PREFIX = ""
main_canvas = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)
py_img_last = None
py_img = ""
