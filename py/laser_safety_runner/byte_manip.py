###########################################################################################
# byte_manip.py - contains utility methods for manipulating bytes into ints and vice-versa
###########################################################################################
import masks as m
import serial_flags_and_vars as s
import globals_and_consts as c
import img_path.img_paths as path


#######################################################################################
# Name: byte_arr_to_int
# Description: accepts an array of 5 bytes and ors them into their respective relative
#              positions in an integer. That integer is returned.
#######################################################################################
def byte_arr_to_int(byte_arr):
    # print("byte_manip.byte_arr_to_int")
    # only using data bytes to build up an int to evaluate (byte[0] is checksum and byte[5] is magic byte)
    return int(byte_arr[0]) | int((byte_arr[1]) << 4) | int((byte_arr[2]) << 8) | int((byte_arr[3]) << 12)


#######################################################################################
# Name: is_input_valid
# Description: takes a byte array as a parameter. Method returns whether the byte arr
#              input is a valid input or not as a bool
#######################################################################################
def is_input_valid(input_byte_arr):
    # make sure
    if len(input_byte_arr) != c.READ_BYTE_SIZE:
        return False
    # make sure data bytes don't have header bits set
    if input_byte_arr[0] > 15 or input_byte_arr[1] > 15 or input_byte_arr[2] > 15 or\
       input_byte_arr[3] > 15 or input_byte_arr[4] < s.MAGIC_BYTE:
        return False
    # print("byte_manip.is_input_valid")
    return True


#######################################################################################
# Name: get_display_image_path
# Description: takes an integer as a parameter. Method returns the appropriate image
#              path as a string.
#######################################################################################
def get_display_image_path(input_int):
    # print("byte_manip.get_display_image_path")
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
#              was set.
######################################################################################
def hash_state(state):
    # print("byte_manip.hash_state")
    return {m.LASER_FIRE_MASK: (state & m.LASER_FIRE_MASK) > 0,
            m.THRESHOLD_MASK: (state & m.THRESHOLD_MASK) > 0, m.SHUTTER_MASK: (state & m.SHUTTER_MASK) > 0,
            m.PROGRAM_MASK: (state & m.PROGRAM_MASK) > 0, m.ESTOP_MASK: (state & m.ESTOP_MASK) > 0,
            m.SAFETY_CIRCUIT_MASK: (state & m.SAFETY_CIRCUIT_MASK) > 0,
            m.DEFEAT_SAFETY_MASK: (state & m.DEFEAT_SAFETY_MASK) > 0,
            m.WARNING_MASK: (state & m.WARNING_MASK) > 0, m.FAULT_MASK: (state & m.FAULT_MASK) > 0,
            m.SLEEP_MASK: (state & m.SLEEP_MASK) > 0, m.FIBER_ERROR_MASK: (state & m.FIBER_ERROR_MASK) > 0}
