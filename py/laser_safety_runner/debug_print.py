#############################################################################
# Class: Debugger
# Description: class with mostly static methods for developer to use to help
#              troubleshoot desired sections of code.
#############################################################################
class Debugger:
    ###################################################
    # Name: default ctor
    # Description: Constructor that init's debug to off
    ###################################################
    def __init__(self):
        self.is_debug_on = False

    #########################################################################
    # Name: run_debug_prints_for_inputs
    # Description: debugging method that prints the 4 data bytes in
    #              byte_arr
    #########################################################################
    @staticmethod
    def print_byte_arr(byte_arr):
        for index in range(6):  # print the bytes as integers
            temp = bytes(byte_arr[index])
            print((int.from_bytes(temp, 'big', signed=False)))
        print("\n")

    ##############################################################################
    # Name: print_serial_exception
    # Description: debugging method that prints a msg indicating a serial message
    ##############################################################################
    def print_serial_exception(self, byte_name_str):
        if self.is_debug_on is True:
            print("Serial exception on writing " + str(byte_name_str))

    ##############################################################################
    # Name: print_no_com_port_for_platform
    # Description: debugging method that prints a msg indicating com port
    #              failure on a specific platform
    ##############################################################################
    def print_no_com_port_for_platform(self, platform):
        if self.is_debug_on is True:
            print("Failed to connect to any available com port on platform:" + str(platform))

    ##############################################################################
    # Name: print_com_port
    # Description: debugging method that prints a msg indicating com port
    #              passed in as a param
    ##############################################################################
    def print_com_port(self, port):
        if self.is_debug_on is True:
            print("Curr communication port: " + port)

    ##############################################################################
    # Name: print_bad_ard_response
    # Description: debugging method that prints a msg indicating an unexpected
    #              Arduino response and the unexpected response
    ##############################################################################
    def print_bad_ard_response(self, response):
        if self.is_debug_on is True:
            print("Unexpected Arduino response: " + str(response))
