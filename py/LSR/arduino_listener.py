from serial import Serial, SerialException, EIGHTBITS
from constant_serial import *
from serial_util import *
from time import sleep


####################################################################
# Class: ArduinoListener
# Description: Listener object for the serial port connected to the
#              input Arduino.
####################################################################
class ArduinoListener:

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
            av.ser = Serial('/dev/ttyACM0', 500000, timeout=0)

            print(av.com_port)

            av.ser.write(RESET_COUNTS)
            av.ser.write(CONTACT_TO_ARD)

            sleep(0.02)

            response = av.ser.read()

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
        if av.this_platform == WIN:
            com_port_prefix = WIN_COM_PORT_PREFIX
            av.found_platform = True
        if av.this_platform == LIN:
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
            if av.ser.in_waiting > 0:
                in_byte = av.ser.read()
                av.serialBuffer[av.serialCount] = in_byte[0]
                # print(ardUSB.in_waiting, serialCount, serialBuffer[serialCount])

                if (av.serialBuffer[av.serialCount] > 127) and (av.serialCount > 4):
                    # print(serialBuffer[0:serialCount+1])

                    inputs_from_ard = av.serialBuffer[av.serialCount - 1] << 12 | \
                                    av.serialBuffer[av.serialCount - 2] << 8 | \
                                    av.serialBuffer[av.serialCount - 3] << 4 | \
                                    av.serialBuffer[av.serialCount - 4]

                    if av.serialBuffer[av.serialCount - 5] == inputs_from_ard % 128:
                        av.ser.write(av.serialBuffer[av.serialCount - 5])
                        print("                  ", inputs_from_ard)
                        av.return_val = inputs_from_ard
                    else:
                        print("CheckSum didnt Match!")
                    av.serialCount = 0
                else:
                    av.serialCount += 1

            # # read if there is anything in the input buffer
            # try:
            #     while av.ser.in_waiting > 0:
            #         print("inside serial read")
            #         # append next byte to data buffer
            #         in_byte = av.ser.read()
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
            #                 av.ser.write(0)
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

    ##################################################################
    # Name: invalidate_open_port_flags
    # Description: helper method that invalidates port flags to open
    ##################################################################
    @staticmethod
    def invalidate_open_port_flags():
        av.has_port_connected_before = False
        av.is_com_port_open = False
