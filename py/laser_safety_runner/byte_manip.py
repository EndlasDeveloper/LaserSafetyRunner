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
    if input_byte_arr[0] >= 16 or input_byte_arr[1] >= 16 or\
            input_byte_arr[2] >= 16 or input_byte_arr[3] >= 16:
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
    states = hash_state(trim_input(input_int))
    if states[c.LASER_FIRE_MASK] is True:
        return c.LASER_FIRE_IMG
    elif states[c.THRESHOLD_MASK] is True:
        return c.LASER_FIRE_IMG
    elif states[c.SHUTTER_MASK] is True:
        return c.LASER_FIRE_IMG
    elif states[c.PROGRAM_MASK] is True:
        return c.LASER_FIRE_IMG
    elif states[c.ESTOP_MASK] is True:
        return c.ESTOP_IMG
    elif states[c.SAFETY_CIRCUIT_MASK] is True:
        return c.SAFETY_CIRCUIT_IMG
    elif states[c.DEFEAT_SAFETY_MASK] is True:
        return c.DEFEAT_SAFETY_IMG
    elif states[c.WARNING_MASK] is True:
        return c.WARNING_IMG
    elif states[c.FAULT_MASK] is True:
        return c.FAULT_IMG
    elif states[c.SLEEP_MASK] is True:
        return c.SLEEP_IMG
    elif states[c.FIBER_ERROR_MASK] is True:
        return c.FIBER_ERROR_IMG
    else:
        return c.NO_LOAD_IMG


def trim_input(input_int):
    mask = 0b111111111111111111111111
    return mask & input_int

######################################################################################
# Name: hash_state
# Description: maps the state mask to a bool indicating whether the bit for that mask
#              was set.
######################################################################################
def hash_state(state):
    hashed_states = {c.LASER_FIRE_MASK: (state & c.LASER_FIRE_MASK) > 0,
                     c.THRESHOLD_MASK: (state & c.THRESHOLD_MASK) > 0, c.SHUTTER_MASK: (state & c.SHUTTER_MASK) > 0,
                     c.PROGRAM_MASK: (state & c.PROGRAM_MASK) > 0, c.ESTOP_MASK: (state & c.ESTOP_MASK) > 0,
                     c.SAFETY_CIRCUIT_MASK: (state & c.SAFETY_CIRCUIT_MASK) > 0,
                     c.DEFEAT_SAFETY_MASK: (state & c.DEFEAT_SAFETY_MASK) > 0,
                     c.WARNING_MASK: (state & c.WARNING_MASK) > 0, c.FAULT_MASK: (state & c.FAULT_MASK) > 0,
                     c.SLEEP_MASK: (state & c.SLEEP_MASK) > 0, c.FIBER_ERROR_MASK: (state & c.FIBER_ERROR_MASK) > 0}
    return hashed_states
