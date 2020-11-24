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

    #############################################################################
    # Name: open_port_and_send_call_out
    # Description: tries to open the com port, if successful, a callout is
    #              sent over serial. The arduino looks at the callout, and
    #              if the callout is expected, the arduino returns a reply,
    #              and if the reply is what is expected, the port is considered
    #              open.
    #############################################################################
    async def open_port_and_flag_result(self):
        try:
            # open USB port
            av.ser = Serial(port=av.com_port, baudrate=BAUD_RATE, bytesize=EIGHTBITS,
                                    timeout=SERIAL_TIMEOUT)
            print(av.com_port)

            av.ser.flushInput()

            av.ser.write(RESET_COUNTS)
            av.ser.write(CONTACT_TO_ARD)

            # should get a 6 byte response packet here
            response = av.ser.read()
            print("response: " + str(response))

            # verify response
            if response == b'x/93':
                # write back a magic byte
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
    async def determine_platform_and_connect(self):
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
            is_open = await self.open_port_and_flag_result()
            if is_open:
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
    def start_reading_from_serial(self):
        # signal arduino
        av.ser.write(RESET_COUNTS)
        av.ser.write(CONTACT_TO_ARD)
        # read if there is anything in the input buffer
        while av.ser.in_waiting > 0:
            try:
                # append next byte to data buffer
                av.arduino_data_buffer.append(av.ser.read())
                # if there is 6 bytes and the last one is empty, just clear and return
                if len(av.arduino_data_buffer) == 6 and av.arduino_data_buffer[5] == b'':
                    if not is_input_valid(av.arduino_data_buffer()):
                        av.arduino_data_buffer.clear()
                        return
                # if header bits are set in data bytes or the serial count exceeds the buffer size
                if len(av.arduino_data_buffer) > 5:
                    # copy data buffer
                    av.arduino_data_buffer_copy = av.arduino_data_buffer
                    # clear data buffer
                    av.arduino_data_buffer.clear()
                    # if return_val has 5 elements, clear -- this is arbitrary
                    if len(av.return_val) >= 5:
                        av.return_val.clear()
                    # append a copy of the data buffer to return_val and return
                    av.return_val.append(av.arduino_data_buffer_copy)
                    return
                #     # check if the ard reset counts bit is set, if so, send signal to ard to reset counts
                #     if byte_to_int(av.arduino_data_buffer[5]) & ARD_RESET_MASK > 0:
                #         print("Arduino triggered the watchdog")
                #         # sfv.ser.write(gc.RESET_COUNTS_FLAG_BYTE)
                #
                #     # check if the ard inputs ready bit is set, if so, read in the 6 bytes from the ard
                #     if byte_to_int(av.arduino_data_buffer[5]) & ARD_REPORT_ERROR_MASK > 0:
                #         print("Arduino reporting at least 1 error")
                #
                #     if is_input_valid(av.arduino_data_buffer):
                #         av.inputs_from_ard = byte_arr_to_int(av.arduino_data_buffer)
                #
                #         if av.arduino_data_buffer[0] == av.inputs_from_ard % 128:
                #             print("Checksum matched!")
                #             av.ser.write(av.arduino_data_buffer[0])
                #         else:
                #             print("Checksum didn't match :/")
                #             av.ser.write(av.arduino_data_buffer[0])
                #     else:
                #         av.serial_count = 0
                #         av.ser.reset_input_buffer()
                #
                #     av.arduino_data_buffer.clear()
                #     return
                # else:
                #     av.serial_count += 1
            except SerialException:  # read failed
                # set proper flags to indicate port needs to be re-opened
                self.invalidate_open_port_flags()
