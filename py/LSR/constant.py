############################################################################
# constant.py - contains the const/finals of the application
############################################################################

# PACKET SIZE
DATA_PACKET_SIZE = 6

# TIMEOUTS
THREAD_JOIN_TIMEOUT = 1.5
MUTEX_ACQUIRE_TIMEOUT = 4
SERIAL_TIMEOUT = 0.5
BASE_UI_REFRESH_RATE = 1.0

# SYSTEMS
WIN = 'Windows'
RASP = 'raspberrypi'
LIN = 'Linux'

# COM PORT AND PORT SPECS
WIN_COM_PORT_PREFIX = "COM"
LIN_COM_PORT_PREFIX = "/dev/ttyUSB"
CONTACT_TO_ARD_FLAG_BYTE = b'/xAA'
RESET_COUNTS_FLAG_BYTE = b'/x99'

# COM PORT SPECS
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



