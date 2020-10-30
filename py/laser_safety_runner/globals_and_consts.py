############################################################################
# globals_and_consts.py - contains most of the constants for the laser_safety_runner
############################################################################

# imports
import serial
import datetime as dt
import pygame

# COM PORT AND PORT SPECS
COM_PORT = "COM5"
BAUD_RATE = 115200
BYTE_SIZE = 8
SERIAL_TIMEOUT = 2

# LASER FIRE BYTE MASKS
LASER_FIRE_MASK = 0x1
THRESHOLD_MASK = 0x2
SHUTTER_MASK = 0x4
PROGRAM_MASK = 0x8

# LASER SAFETY BYTE MASKS
ESTOP_MASK = 0x10
SAFETY_CIRCUIT_MASK = 0x20
DEFEAT_SAFETY_MASK = 0x40
WARNING_MASK = 0x80

# LASER STATE BYTE MASKS
FAULT_MASK = 0x100
SLEEP_MASK = 0x200
FIBER_ERROR_MASK = 0x400

# IMAGE FILES AND PATH
IMG_PATH = "resources/"
ESTOP_IMG = IMG_PATH + "estop_active.jpg"
SAFETY_CIRCUIT_IMG = IMG_PATH + "safety_circuit_error.jpg"
DEFEAT_SAFETY_IMG = IMG_PATH + "defeat_safety.jpg"
LASER_FIRE_IMG = IMG_PATH + "laser_fire.jpg"
PILOT_FIRE_IMG = IMG_PATH + "pilot_laser.jpg"
WARNING_IMG = IMG_PATH + "warning.jpg"
FIBER_ERROR_IMG = IMG_PATH + "fiber_error.jpg"
FAULT_IMG = IMG_PATH + "fault.jpg"
SLEEP_IMG = IMG_PATH + "sleep.jpg"
NO_LOAD_IMG = IMG_PATH + "no_load.jpg"
WAITING_ON_INPUT_IMG = IMG_PATH + "waiting_for_input_device.jpg"

# LITTLE OR BIG ENDIAN
ENDIAN = "big"
CHECK_ARD_TIMEOUT = 1000

# to get pygame to display full screen, must set display w and h to 640, 480 and set full screen flag
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480

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
is_com_port_open = False
py_img_last = None

# initialize countdown for checking the arduino
last_millis = type(dt.datetime)
COM_PORT_INDEX = int(1)
CONTACT_TO_ARD_FLAG_BYTE = b'/xAA'
RESET_COUNTS_FLAG_BYTE = b'/x99'

main_canvas = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)
current_millis = 0
