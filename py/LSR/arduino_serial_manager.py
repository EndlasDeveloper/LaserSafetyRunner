from serial import Serial, SerialException, EIGHTBITS
from constant_serial import *
from serial_util import *
from constant_mask import *
from time import sleep, perf_counter


class ArduinoSerialManager:

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
    def open_port_and_flag_result(self):
        try:
            # open USB port
            av.ser = Serial(port=av.com_port, baudrate=BAUD_RATE, bytesize=EIGHTBITS,
                                    timeout=SERIAL_TIMEOUT)
            av.ser.write(RESET_COUNTS)
            av.ser.write(CONTACT_TO_ARD)
            response = av.ser.read()  # get response
            # cast response into an int
            response = int.from_bytes(response, ENDIAN, signed=False)
            # verify response
            if response == 1:
                # write back a magic byte
                av.ser.write(int.to_bytes(response, length=1, byteorder=ENDIAN, signed=False))
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
                self.set_open_port_flags()
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
    async def start_reading_from_serial(self, event):
        await event.wait()
        while av.ser.in_waiting > 0:
            # signal arduino
            try:
                if len(av.shared_data_buffer) == 0:
                    av.ser.write(RESET_COUNTS)
                    av.ser.write(CONTACT_TO_ARD)
                    sleep(0.5)
                    # give arduino time to clear its vars and send a response
                    response = av.ser.read()
                    av.serial_count = 0
                    if not response == b'\x01':
                        print("arduino didn't send a 1")

                if av.ser.in_waiting >= 6:
                    for i in range(6):
                        av.shared_data_buffer.append(av.ser.read())

                # if header bits are set in data bytes or the serial count exceeds the buffer size
                if len(av.shared_data_buffer) > 5:
                    for i in range(6):
                        print("byte" + str(i) + ": " + (str(bin(int.from_bytes(av.shared_data_buffer[i],
                                                                               byteorder=ENDIAN, signed=False)))))
                    # check if the ard reset counts bit is set, if so, send signal to ard to reset counts
                    if byte_to_int(av.shared_data_buffer[5]) & ARD_RESET_MASK > 0:
                        print("Arduino triggered the watchdog")
                        # sfv.ser.write(gc.RESET_COUNTS_FLAG_BYTE)

                    # check if the ard inputs ready bit is set, if so, read in the 6 bytes from the ard
                    if byte_to_int(av.shared_data_buffer[5]) & ARD_REPORT_ERROR_MASK > 0:
                        print("Arduino reporting at least 1 error")

                    if is_input_valid(av.shared_data_buffer):
                        av.inputs_from_ard = byte_arr_to_int(av.shared_data_buffer)

                        if av.shared_data_buffer[0] == av.inputs_from_ard % 128:
                            print("Checksum matched!")
                            av.ser.write(av.shared_data_buffer[0])
                        else:
                            print("Checksum didn't match :/")
                    else:
                        av.serial_count = 0

                    av.shared_data_buffer.clear()
                elif not len(av.shared_data_buffer) == 0:
                    print("something went wrong in serial manager")
                # # this just prints the read byte array to console
                # debug.Debugger.print_byte_arr(gc.serial_in_buffer)
                # walk through the buffer and verify
            except SerialException:  # read failed
                # set proper flags to indicate port needs to be re-opened
                self.invalidate_open_port_flags()
