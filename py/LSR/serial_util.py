##############################################################################
# File: serial_util.py
# Description: file containing some utility methods that are handy for more than
#              one class in the application
##############################################################################

# imports
import app_vars as av


###########################################################
# Name: byte_to_int
# Description: accepts a byte as a parameter and then
#              converts that byte to a returned integer
###########################################################
def byte_to_int(byte):
    int_frm_byte = 0
    for b in byte:
        int_frm_byte = int_frm_byte * 256 + int(b)
    return int_frm_byte


#################################################################################################
# Name: is_port_set
# Description: returns bool describing whether the port is set and ready to communicate through
#################################################################################################
def is_port_set():
    return av.has_port_connected_before and av.is_com_port_open and av.found_platform



