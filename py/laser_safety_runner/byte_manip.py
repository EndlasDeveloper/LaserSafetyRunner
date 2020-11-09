###########################################################################################
# byte_manip.py - contains utility methods for manipulating bytes into ints and vice-versa
###########################################################################################
import masks as m
import globals_and_consts as c
import img_paths as path


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


#######################################################################################
# Name: is_input_valid
# Description: takes a byte array as a parameter. Method returns whether the byte arr
#              input is a valid input or not as a bool
#######################################################################################
def is_input_valid(input_byte_arr):
    # make sure input arr is the right size
    if len(input_byte_arr) != c.READ_BYTE_SIZE:
        print("is_input_valid: the size of the byte array is not c.READ_BYTE_SIZE")
        return False
    # make sure data bytes don't have header bits set, and vice-versa for the magic byte
    if byte_to_int(bytes(input_byte_arr[1])) > 15 or byte_to_int(bytes(input_byte_arr[2])) > 15 or \
            byte_to_int(bytes(input_byte_arr[3])) > 15 or byte_to_int(bytes(input_byte_arr[4])) > 15:
        print("is_input_valid: data bytes weren't set properly")
        return False
    # check if MSB on terminating byte is set
    if byte_to_int(bytes(input_byte_arr[5])) < 128:
        print("is_input_valid: magic byte wasn't set properly")
        return False
    return True


#######################################################################################
# Name: get_display_image_path
# Description: takes an integer as a parameter. Method returns the appropriate image
#              path as a string.
#######################################################################################
def get_display_image_path(input_int):
    states = hash_state(input_int)
    if states[m.LASER_FIRE_MASK]:
        return path.LASER_FIRE_IMG
    elif states[m.THRESHOLD_MASK]:
        return path.LASER_FIRE_IMG
    elif states[m.SHUTTER_MASK]:
        return path.LASER_FIRE_IMG
    elif states[m.PROGRAM_MASK]:
        return path.LASER_FIRE_IMG
    elif states[m.ESTOP_MASK]:
        return path.ESTOP_IMG
    elif states[m.SAFETY_CIRCUIT_MASK]:
        return path.SAFETY_CIRCUIT_IMG
    elif states[m.DEFEAT_SAFETY_MASK]:
        return path.DEFEAT_SAFETY_IMG
    elif states[m.WARNING_MASK]:
        return path.WARNING_IMG
    elif states[m.FAULT_MASK]:
        return path.FAULT_IMG
    elif states[m.SLEEP_MASK]:
        return path.SLEEP_IMG
    elif states[m.FIBER_ERROR_MASK]:
        return path.FIBER_ERROR_IMG
    else:
        return path.NO_LOAD_IMG


######################################################################################
# Name: hash_state
# Description: maps the state mask to a bool indicating whether the bit for that mask
#              was set and returns the dict
######################################################################################
def hash_state(state):
    return {m.LASER_FIRE_MASK: (state & m.LASER_FIRE_MASK) > 0,
            m.THRESHOLD_MASK: (state & m.THRESHOLD_MASK) > 0, m.SHUTTER_MASK: (state & m.SHUTTER_MASK) > 0,
            m.PROGRAM_MASK: (state & m.PROGRAM_MASK) > 0, m.ESTOP_MASK: (state & m.ESTOP_MASK) > 0,
            m.SAFETY_CIRCUIT_MASK: (state & m.SAFETY_CIRCUIT_MASK) > 0,
            m.DEFEAT_SAFETY_MASK: (state & m.DEFEAT_SAFETY_MASK) > 0,
            m.WARNING_MASK: (state & m.WARNING_MASK) > 0, m.FAULT_MASK: (state & m.FAULT_MASK) > 0,
            m.SLEEP_MASK: (state & m.SLEEP_MASK) > 0, m.FIBER_ERROR_MASK: (state & m.FIBER_ERROR_MASK) > 0}
