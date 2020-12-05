################################################
# File: arduino_listener
# Description: file holding the arduino listener class. This class is in charge of managing the serial port of the Pi
#              side, reading from the arduino,k checking if the read input is valid and then pushing the valid result
#              to a shared piece of memory for the display to use in rendering the UI
################################################
# imports
from serial import Serial, SerialException
from serial_util import *
from platform import system

# SYSTEMS
WIN = 'Windows'
LIN = 'Linux'

# COM PORT AND PORT SPECS
WIN_COM_PORT_PREFIX = "COM"
LIN_COM_PORT_PREFIX = "/dev/ttyACM"

CONTACT_TO_ARD = b'\x93'
REQUEST_FOR_DATA = b'\xAA'
RESET_COUNTS = b'\x99'

# COM PORT SPECS
BAUD_RATE = 115200
BUFFER_SIZE = 30


####################################################################
# Class: ArduinoListener
# Description: Listener object for the serial port connected to the
#              input Arduino.
####################################################################
class ArduinoListener:

    #########################################################################
    # Name: constructor
    # Description: initializes all class variables including the Serial obj
    #              used to communicate with the Arduino
    #########################################################################
    def __init__(self):
        # serial obj
        self.ser = Serial()
        # com port to connect to
        self.com_port = ""
        # string of the os platform
        self.this_platform = system()
        # software buffer to read arduino inputs into
        self.serial_buffer = [0] * BUFFER_SIZE
        # keeps track of number of reads
        self.serial_count = 0
        self.data_packet = None

    #############################################################################
    # Name: open_port_and_send_call_out
    # Description: tries to open the com port, if successful, a callout is
    #              sent over serial. The arduino looks at the callout, and
    #              if the callout is expected, the arduino returns a reply,
    #              and if the reply is what is expected, the port is considered
    #              open.
    #############################################################################
    def open_port_and_flag_result(self):
        try:
            # open USB port
            self.ser = Serial(av.com_port, baudrate=BAUD_RATE, timeout=0)
            # debugging print the successful com port
            print(av.com_port)
            # initialize contact with arduino
            self.ser.write(RESET_COUNTS)
            self.ser.write(CONTACT_TO_ARD)
            # get arduino response
            response = self.ser.read()
            # verify response
            if response == CONTACT_TO_ARD:
                print("response: " + str(response))
                # valid response, so set open port flags and return True
                self.set_open_port_flags()
                return True
            else:
                # invalid response
                self.invalidate_open_port_flags()
                return False
        except SerialException:
            # something went wrong with serial connection, so invalid response
            self.invalidate_open_port_flags()
            return False

    ####################################################################
    # Name: determine_platform
    # Description: method that sets COM_PORT to system dependent syntax
    ####################################################################
    def determine_platform_and_connect(self):
        com_port_prefix = ""
        # see if we're on windows
        if self.this_platform == WIN:
            com_port_prefix = WIN_COM_PORT_PREFIX
            av.found_platform = True
        # see if we're on linux
        elif self.this_platform == LIN:
            com_port_prefix = LIN_COM_PORT_PREFIX
            av.found_platform = True

        # iterate through com prefix with 0-9 numbering to look for the arduino
        for com_num in range(9):
            av.com_port = com_port_prefix + str(com_num)
            # try to connect to each, see if a response from the arduino returns
            if self.open_port_and_flag_result():
                return True
        # no com ports worked, so make sure flags are invalidated, and return False
        self.invalidate_open_port_flags()
        return False

    ####################################################################
    # Name: start_reading_from_serial
    # Description: tries to read in 5 bytes over the open serial
    #              port. If it fails, a handler is called where
    #              values and flags are set to try and re-open
    #              the port
    ####################################################################
    def read_from_serial(self):
        try:
            if self.ser.in_waiting > 0:
                in_byte = self.ser.read()
                self.serial_buffer[self.serial_count] = in_byte[0]
                # print(ardUSB.in_waiting, serialCount, serialBuffer[serialCount])

                if (self.serial_buffer[self.serial_count] > 127) and (self.serial_count > 4):
                    # print(serialBuffer[0:serialCount+1])

                    inputs_from_ard = self.data_bytes_to_int([self.serial_buffer[self.serial_count - 4],
                                                             self.serial_buffer[self.serial_count - 3],
                                                             self.serial_buffer[self.serial_count - 2],
                                                             self.serial_buffer[self.serial_count - 1]])

                    if self.serial_buffer[self.serial_count - 5] == inputs_from_ard % 128:
                        self.ser.write(self.serial_buffer[self.serial_count - 5])
                        print("                  ", inputs_from_ard)
                        return inputs_from_ard
                    else:
                        print("CheckSum didn't Match!")

                    self.serial_count = 0
                else:
                    self.serial_count += 1

            # # read if there is anything in the input buffer
            # try:
            #     while self.ser.in_waiting > 0:
            #         print("inside serial read")
            #         # append next byte to data buffer
            #         in_byte = self.ser.read()
            #         in_int = byte_to_int(in_byte)
            #         av.arduino_data_buffer.append(in_byte)
            #         # if there is 6 bytes and the last one is empty, just clear and return
            #         # if header bits are set in data bytes or the serial count exceeds the buffer size
            #         if len(av.arduino_data_buffer) > 5 and in_int > 127:
            #             if is_input_valid(av.arduino_data_buffer[-6:len(av.arduino_data_buffer)]):
            #                 result = byte_arr_to_int(av.arduino_data_buffer[-6:len(av.arduino_data_buffer)])
            #                 result_arr = []
            #                 result_arr.append(result)
            #                 av.return_val.append(result_arr)
            #                 self.ser.write(0)
            #             return

        except SerialException:  # read failed
            print("Serial ex")
            # set proper flags to indicate port needs to be re-opened
            self.invalidate_open_port_flags()
            return None

    ########################################################################
    # Name: initialize_to_arduino
    # Description: initializes the serial connection between the RPi and
    #              Arduino
    ########################################################################
    def initialize_to_arduino(self):
        # keep searching for com port till one gives arduino response
        # if successful connect, set flags and display
        if self.determine_platform_and_connect():
            # print("inside init serial to arduino")
            av.is_com_port_open = True
            if av.has_port_connected_before is None:
                av.has_port_connected_before = False
            else:
                av.has_port_connected_before = True
            av.found_platform = True
            return True
        else:
            print("no ard response...")
            return False

    #######################################################################################
    # Name: is_input_valid
    # Description: takes a byte array as a parameter. Method returns whether the byte arr
    #              input is a valid input or not as a bool
    #######################################################################################
    def is_input_valid(self, input_byte_arr):
        if input_byte_arr[5] < b'\x80':
            print("is_input_valid: magic byte wasn't set properly")
            return False

        if input_byte_arr[1] > b'\x0F' or input_byte_arr[2] > b'\x0F' or\
                input_byte_arr[3] > b'\x0F' or input_byte_arr[4] > b'\x0F':
            return False

        input_int = self.data_bytes_to_int([input_byte_arr[1], input_byte_arr[2], input_byte_arr[3], input_byte_arr[4]])
        print("checksum: " + str(input_int % 128))
        print("byte arr [0]: " + str(input_byte_arr[0]))
        ck_sum = int.from_bytes(input_byte_arr[0], byteorder='big')
        if (input_int % 128) != ck_sum:
            return False
        else:
            return True

    #######################################################################################
    # Name: byte_arr_to_int
    # Description: accepts an array of 5 bytes and ors them into their respective relative
    #              positions in an integer. That integer is returned.
    #######################################################################################
    @staticmethod
    def data_bytes_to_int(byte_arr):
        # only using data bytes to build up an int to evaluate (byte[0] is checksum and byte[5] is magic byte)
        i1 = byte_to_int(byte_arr[0])
        i2 = (byte_to_int(byte_arr[1]) << 4)
        i3 = (byte_to_int(byte_arr[2]) << 8)
        i4 = (byte_to_int(byte_arr[3]) << 12)
        return i1 | i2 | i3 | i4

    ##############################################################
    # Name: set_open_port_flags
    # Description: helper method that sets the port flags to open
    ##############################################################
    @staticmethod
    def set_open_port_flags():
        av.has_port_connected_before = True
        av.is_com_port_open = True
        av.found_platform = True

    ##################################################################
    # Name: invalidate_open_port_flags
    # Description: helper method that invalidates port flags to open
    ##################################################################
    @staticmethod
    def invalidate_open_port_flags():
        av.has_port_connected_before = False
        av.is_com_port_open = False
        av.found_platform = False
