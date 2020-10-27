###########################################################################################
# byte_manip.py - contains utility methods for manipulating bytes into ints and vice-versa
###########################################################################################
import constants as c


#######################################################################################
# Name: byte_arr_to_int
# Description: accepts an array of 5 bytes and ors them into their respective relative
#              positions in an integer. That integer is returned.
#######################################################################################
def byte_arr_to_int(byte_arr):
    return byte_arr[0] | (byte_arr[1] << 4) | (byte_arr[2] << 8) | (byte_arr[3] << 12)


#######################################################################################
# Name: is_input_valid
# Description: takes a byte array as a parameter. Method returns whether the byte arr
#              input is a valid input or not as a bool
#######################################################################################
def is_input_valid(input_byte_arr):
    if input_byte_arr[0] >= 16 or input_byte_arr[1] >= 16 or input_byte_arr[2] >= 16 or input_byte_arr[3] >= 16:
        return False
    if input_byte_arr[4] < 16:
        return False
    return True


#######################################################################################
# Name: get_display_image_path
# Description: takes an integer as a parameter. Method returns the appropriate image
#              path as a string.
#######################################################################################
def get_display_image_path(input_int):
    if c.LASER_FIRE_MASK & input_int != 0:
        return c.LASER_FIRE_IMG
    elif c.THRESHOLD_MASK & input_int != 0:
        return c.LASER_FIRE_IMG
    elif c.SHUTTER_MASK & input_int != 0:
        return c.LASER_FIRE_IMG
    elif c.PROGRAM_MASK & input_int != 0:
        return c.LASER_FIRE_IMG
    elif c.ESTOP_MASK & input_int != 0:
        return c.ESTOP_IMG
    elif c.SAFETY_CIRCUIT_MASK & input_int != 0:
        return c.SAFETY_CIRCUIT_IMG
    elif c.DEFEAT_SAFETY_MASK & input_int != 0:
        return c.DEFEAT_SAFETY_IMG
    elif c.WARNING_MASK & input_int != 0:
        return c.WARNING_IMG
    elif c.FAULT_MASK & input_int != 0:
        return c.FAULT_IMG
    elif c.SLEEP_MASK & input_int != 0:
        return c.SLEEP_IMG
    elif c.FIBER_ERROR_MASK & input_int != 0:
        return c.FIBER_ERROR_IMG
    else:
        return c.NO_LOAD_IMG
