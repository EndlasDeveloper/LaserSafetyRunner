##############################################################
# serial_flags_and_vars.py - vars to hold the serial
#   port flags to indicate whether connection has been make,
#   and other serial related data structures
##############################################################

# imports
import datetime as dt
import serial
import platform

# initialize countdown for checking the arduino
last_clock = dt.datetime.now()
serial_count = 0
inputs_frm_ard = 0
COM_PORT_INDEX = int(1)

# SPECIAL BYTES
CONTACT_TO_ARD_FLAG_BYTE = b'/xAA'
RESET_COUNTS_FLAG_BYTE = b'/x99'
MAGIC_BYTE = (1 << 7)
FOUND_PLATFORM = False
HAS_PORT_CONNECTED = False
CHECK_ARD_TIMEOUT = 1000
IS_SER_EX_HANDLED = False
this_platform = platform.system()

# serial port and flag
ser = serial.Serial()
is_com_port_open = False
