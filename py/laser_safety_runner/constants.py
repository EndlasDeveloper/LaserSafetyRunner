###################################################################
# constants.py - contains most of the constants for the entire app
###################################################################

# LITTLE OR BIG ENDIAN
ENDIAN = "big"

# COM PORT AND PORT SPECS
COM_PORT = "COM5"
BAUD_RATE = 115200
BYTE_SIZE = 8
SERIAL_TIMEOUT = 2

# LASER FIRE BYTE
LASER_FIRE_MASK = 0b1
THRESHOLD_MASK = 0b10
SHUTTER_MASK = 0b100
PROGRAM_MASK = 0b1000

# LASER SAFETY BYTE
ESTOP_MASK = 256
SAFETY_CIRCUIT_MASK = 512
DEFEAT_SAFETY_MASK = 1024
WARNING_MASK = 2048

# LASER STATE BYTE
FAULT_MASK = 65536
SLEEP_MASK = 131072
FIBER_ERROR_MASK = 262144

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
