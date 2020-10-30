
#############################################################################
# Class: Debugger
# Description: class with mostly static methods for developer to use to help
#              troubleshoot desired sections of code.
#############################################################################
class Debugger:
    # flag to indicate whether console should print debug statements
    is_debug_on = False

    ###################################################
    # Name: ctor
    # Description: constructor that takes a bool as a
    #              flag to indicate whether to print
    #              the debug statements.
    ###################################################
    def __init__(self, is_debug_on):
        self.is_debug_on = is_debug_on

    #########################################################################
    # Name: run_debug_prints_for_inputs
    # Description: debugging method that prints the 4 data bytes in
    #              byte_arr
    #########################################################################
    @staticmethod
    def print_byte_arr(byte_arr):
        i = 0
        for b in byte_arr:  # print the bytes as integers
            print("byte{0}: {1}".format(str(i), (int(b))))
            i += 1
        print("\n")

    ##############################################################################
    # Name: print_serial_exception
    # Description: debugging method that prints a msg indicating a serial message
    ##############################################################################
    @staticmethod
    def print_serial_exception(byte_name_str):
        print("Serial exception on writing " + str(byte_name_str))

    ##############################################################################
    # Name: print_no_com_port_for_platform
    # Description: debugging method that prints a msg indicating com port
    #              failure on a specific platform
    ##############################################################################
    @staticmethod
    def print_no_com_port_for_platform(platform):
        print("Failed to connect to any available com port on platform:" + str(platform))

