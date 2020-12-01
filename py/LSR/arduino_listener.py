################################################
# File: arduino_listener
# Description: file holding the arduino listener class. This class is in charge of managing the serial port of the Pi
#              side, reading from the arduino,k checking if the read input is valid and then pushing the valid result
#              to a shared piece of memory for the display to use in rendering the UI
################################################
# imports
from serial import Serial, SerialException
from constant_serial import *
from serial_util import *
from platform import system


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
        self.ser = Serial()
        self.com_port = ""
        self.this_platform = system()
        self.serial_buffer = [0] * 30
        self.serial_count = 0
        self.arduino_data_buffer = []
        self.arduino_data_buffer_copy = []

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

            print(av.com_port)

            self.ser.write(RESET_COUNTS)
            self.ser.write(CONTACT_TO_ARD)

            print("before read")
            response = self.ser.read()
            print("after read")
            # verify response
            if response == CONTACT_TO_ARD:
                print("response: " + str(response))
                self.set_open_port_flags()
                return True
            else:
                self.invalidate_open_port_flags()
                return False
        except SerialException:
            self.invalidate_open_port_flags()
            return False

    ####################################################################
    # Name: determine_platform
    # Description: method that sets COM_PORT to system dependent syntax
    ####################################################################
    def determine_platform_and_connect(self):
        com_port_prefix = ""
        if self.this_platform == WIN:
            com_port_prefix = WIN_COM_PORT_PREFIX
            av.found_platform = True
        if self.this_platform == LIN:
            com_port_prefix = LIN_COM_PORT_PREFIX
            av.found_platform = True

        for com_num in range(9):
            av.com_port = com_port_prefix + str(com_num)
            # try to connect to each, see if a response from the arduino returns
            if self.open_port_and_flag_result():
                return True

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

                if (self.serial_buffer[av.serial_count] > 127) and (self.serial_count > 4):
                    # print(serialBuffer[0:serialCount+1])

                    inputs_from_ard = self.serial_buffer[self.serial_count - 1] << 12 | \
                                    self.serial_buffer[self.serial_count - 2] << 8 | \
                                    self.serial_buffer[self.serial_count - 3] << 4 | \
                                    self.serial_buffer[self.serial_count - 4]

                    if self.serial_buffer[self.serial_count - 5] == inputs_from_ard % 128:
                        self.ser.write(self.serial_buffer[self.serial_count - 5])
                        print("                  ", inputs_from_ard)
                        av.shared_state = inputs_from_ard
                    else:
                        print("CheckSum didnt Match!")
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

    #########################################################
    # Name: set_open_port_flags
    # Description: helper method that sets the port flags to open
    #########################################################
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
