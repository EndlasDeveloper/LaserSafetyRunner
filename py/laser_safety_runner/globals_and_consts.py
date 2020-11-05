############################################################################
# globals_and_consts.py - contains most of the constants for the laser_safety_runner
############################################################################

# imports
import pygame
import img_path.img_paths as p
import debug_print as debug

# SYSTEMS
WIN = 'Windows'
RASP = 'raspberrypi'
LIN = 'Linux'

# COM PORT AND PORT SPECS
COM_PORT = "COM5"
BAUD_RATE = 115200
BYTE_SIZE = 8
SERIAL_TIMEOUT = 2
READ_BYTE_SIZE = 6


# LITTLE OR BIG ENDIAN
ENDIAN = "big"
DISPLAY_CAPTION = "LASER SAFETY RUNNER"
# FONT
DISPLAY_FONT = 'freesansbold.ttf'
DISPLAY_FONT_SIZE = 40

WAITING_FOR_INPUT_DEVICE_MSG = "Waiting for input device reply..."
OPENING_COM_PORTS = "Finding open COM port..."

# to get pygame to display full screen, must set display w and h to 640, 480 and set full screen flag
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

py_img_last = None
main_canvas = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)

debug = debug.Debugger()
img = None
