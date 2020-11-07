##########################################################################
# masks.py - script file holding all masks for deciphering bit positions
##########################################################################

# LASER FIRE BYTE MASKS
LASER_FIRE_MASK = 0x1
THRESHOLD_MASK = 0x2
SHUTTER_MASK = 0x4
PROGRAM_MASK = 0x8

# LASER SAFETY BYTE MASKS
ESTOP_MASK = 0x10
SAFETY_CIRCUIT_MASK = 0x20
DEFEAT_SAFETY_MASK = 0x40
WARNING_MASK = 0x80

# LASER STATE BYTE MASKS
FAULT_MASK = 0x100
SLEEP_MASK = 0x200
FIBER_ERROR_MASK = 0x400
