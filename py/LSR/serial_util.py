import app_vars as av
from constant_serial import READ_BYTE_SIZE

#######################################################################################
# Name: byte_arr_to_int
# Description: accepts an array of 5 bytes and ors them into their respective relative
#              positions in an integer. That integer is returned.
#######################################################################################
def byte_arr_to_int(byte_arr):
    # only using data bytes to build up an int to evaluate (byte[0] is checksum and byte[5] is magic byte)
    i1 = byte_to_int(bytes(byte_arr[1]))
    i2 = (byte_to_int(bytes(byte_arr[2])) << 4)
    i3 = (byte_to_int(bytes(byte_arr[3])) << 8)
    i4 = (byte_to_int(bytes(byte_arr[4])) << 12)
    return i1 | i2 | i3 | i4


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


#######################################################################################
# Name: is_input_valid
# Description: takes a byte array as a parameter. Method returns whether the byte arr
#              input is a valid input or not as a bool
#######################################################################################
def is_input_valid(input_byte_arr):
    # make sure data bytes don't have header bits set, and vice-versa for the magic byte
    if byte_to_int(bytes(input_byte_arr[1])) > 15 or byte_to_int(bytes(input_byte_arr[2])) > 15 or \
            byte_to_int(bytes(input_byte_arr[3])) > 15 or byte_to_int(bytes(input_byte_arr[4])) > 15:
        print("is_input_valid: data bytes weren't set properly")
        av.arduino_data_buffer.clear()
        return False
    else:
        print("data bytes are valid")
    # check if MSB on terminating byte is set
    if byte_to_int(bytes(input_byte_arr[5])) < 128:
        print("is_input_valid: magic byte wasn't set properly")
        return False
    print("magic byte was set properly")
    return True
