############################################################################
# globals_and_consts.py - contains most of the constants for the laser_safety_runner
############################################################################

# imports
import pygame
import datetime as dt
import serial
import img_path.img_paths as p
import debug_print as debug

# SYSTEMS
WIN = 'Windows'
RASP = 'raspberrypi'
LIN = 'Linux'

# COM PORT AND PORT SPECS
COM_PORT = "COM5"
MAGIC_BYTE = b'x/80'
CONTACT_TO_ARD_FLAG_BYTE = b'/xAA'
RESET_COUNTS_FLAG_BYTE = b'/x99'

# COM PORT AND PORT SPECS
BAUD_RATE = 115200
BYTE_SIZE = 8
SERIAL_TIMEOUT = 2
READ_BYTE_SIZE = 5


# LITTLE OR BIG ENDIAN
ENDIAN = "big"
DISPLAY_CAPTION = "LASER SAFETY RUNNER"
# FONT
DISPLAY_FONT = 'freesansbold.ttf'
DISPLAY_FONT_SIZE = 40

WAITING_FOR_INPUT_DEVICE_MSG = "Waiting for input device reply..."
OPENING_COM_PORTS_MSG = "Finding open COM port..."

# to get pygame to display full screen, must set display w and h to 640, 480 and set full screen flag
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

debug = debug.Debugger()
img = None
# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (220, 220, 220)
LIGHT_BLUE = (173, 216, 230)
NAVY = (0, 0, 128)
SKY_BLUE = (0, 191, 255)

# not actually constants, but need to be away from main
ser = serial.Serial()

has_port_connected = False
is_com_port_open = False
found_platform = False

py_img_last = None
py_img = ""
# initialize countdown for checking the arduino
last_clock = dt.datetime.now()
serial_in_buffer = []
serial_count = 0
inputs_from_ard = 0
COM_PORT_INDEX = int(1)
main_canvas = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)
