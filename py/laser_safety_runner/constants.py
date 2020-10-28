###################################################################
# constants.py - contains most of the constants for the entire app
###################################################################

# COM PORT AND PORT SPECS
COM_PORT = "COM5"
BAUD_RATE = 115200
BYTE_SIZE = 8
SERIAL_TIMEOUT = 2

# LASER FIRE BYTE MASKS
LASER_FIRE_MASK = 0b1
THRESHOLD_MASK = 0b10
SHUTTER_MASK = 0b100
PROGRAM_MASK = 0b1000

# LASER SAFETY BYTE MASKS
ESTOP_MASK = 0b10000
SAFETY_CIRCUIT_MASK = 0b100000
DEFEAT_SAFETY_MASK = 0b1000000
WARNING_MASK = 0b10000000

# LASER STATE BYTE MASKS
FAULT_MASK = 0b100000000
SLEEP_MASK = 0b1000000000
FIBER_ERROR_MASK = 0b10000000000

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

# LITTLE OR BIG ENDIAN
ENDIAN = "big"

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
