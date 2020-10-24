###########################################################################################
# byte_manip.py - contains utility methods for manipulating bytes into ints and vice-versa
###########################################################################################

#######################################################################################
# Name: byte_arr_to_int
# Description: accepts an array of 5 bytes and ors them into their respective relative
#              positions in an integer. That integer is returned.
#######################################################################################
def byte_arr_to_int(byte_arr):
    return byte_arr[0] | (byte_arr[1] << 4) | (byte_arr[2] << 8) | (byte_arr[3] << 12)

