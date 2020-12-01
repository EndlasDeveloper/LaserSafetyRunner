############################################################################
# constant_serial.py - contains the const/finals of the application
############################################################################

# SYSTEMS
WIN = 'Windows'
LIN = 'Linux'

# COM PORT AND PORT SPECS
WIN_COM_PORT_PREFIX = "COM"
LIN_COM_PORT_PREFIX = "/dev/ttyACM"

CONTACT_TO_ARD = b'\x93'
REQUEST_FOR_DATA = b'\xAA'
RESET_COUNTS = b'\x99'

# COM PORT SPECS
BAUD_RATE = 115200

