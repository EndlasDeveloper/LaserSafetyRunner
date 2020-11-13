############################################################################
# constant_serial.py - contains the const/finals of the application
############################################################################

# PACKET SIZE
DATA_PACKET_SIZE = 6

# TIMEOUTS
THREAD_JOIN_TIMEOUT = 1.5
MUTEX_ACQUIRE_TIMEOUT_ARDUINO = 2.0
MUTEX_ACQUIRE_TIMEOUT_DISPLAY = 10.0
SERIAL_TIMEOUT = 0.5


# SYSTEMS
WIN = 'Windows'
LIN = 'Linux'

# COM PORT AND PORT SPECS
WIN_COM_PORT_PREFIX = "COM"
LIN_COM_PORT_PREFIX = "/dev/ttyUSB"
CONTACT_TO_ARD = 170
RESET_COUNTS = 153

# COM PORT SPECS
BAUD_RATE = 115200
BYTE_SIZE = 8
READ_BYTE_SIZE = 6

# LITTLE OR BIG ENDIAN
ENDIAN = "big"



