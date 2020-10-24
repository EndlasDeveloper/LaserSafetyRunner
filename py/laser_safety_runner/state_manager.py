import constants as const

hashed_states = {}


def hash_state(state):
    hashed_states[const.LASER_FIRE_MASK] = (state & const.LASER_FIRE_MASK) > 0
    hashed_states[const.THRESHOLD_MASK] = (state & const.THRESHOLD_MASK) > 0
    hashed_states[const.SHUTTER_MASK] = (state & const.SHUTTER_MASK) > 0
    hashed_states[const.PROGRAM_MASK] = (state & const.PROGRAM_MASK) > 0

    hashed_states[const.ESTOP_MASK] = (state & const.ESTOP_MASK) > 0
    hashed_states[const.SAFETY_CIRCUIT_MASK] = (state & const.SAFETY_CIRCUIT_MASK) > 0
    hashed_states[const.DEFEAT_SAFETY_MASK] = (state & const.DEFEAT_SAFETY_MASK) > 0
    hashed_states[const.WARNING_MASK] = (state & const.WARNING_MASK) > 0

    hashed_states[const.FAULT_MASK] = (state & const.FAULT_MASK) > 0
    hashed_states[const.SLEEP_MASK] = (state & const.SLEEP_MASK) > 0
    hashed_states[const.FIBER_ERROR_MASK] = (state & const.FIBER_ERROR_MASK) > 0


def get_state_image():
    state_img_str = ""
    if hashed_states[const.LASER_FIRE_MASK] is True:
        if hashed_states[const.THRESHOLD] is True:
            state_img_str = const.PILOT_FIRE_IMG
        else:
            state_img_str = const.LASER_FIRE_IMG
    elif hashed_states[const.ESTOP_MASK] is True:
        state_img_str = const.ESTOP_IMG
    elif hashed_states[const.SAFETY_CIRCUIT_MASK] is True:
        state_img_str = const.SAFETY_CIRCUIT_IMG
    elif hashed_states[const.DEFEAT_SAFETY_MASK] is True:
        state_img_str = const.DEFEAT_SAFETY_IMG
    elif hashed_states[const.WARNING_MASK] is True:
        state_img_str = const.WARNING_IMG
    elif hashed_states[const.FAULT_MASK] is True:
        state_img_str = const.FAULT_IMG
    elif hashed_states[const.SLEEP_MASK] is True:
        state_img_str = const.SLEEP_IMG
    elif hashed_states[const.FIBER_ERROR_MASK] is True:
        state_img_str = const.FIBER_ERROR_IMG
    return state_img_str



