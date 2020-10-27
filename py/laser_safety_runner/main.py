####################################################################
# main.py - implements the main entry point into the program
####################################################################

# imports
import image_manip as i_manip
import byte_manip as b_manip
import serial
import constants as c

# file constants
IMAGE_TO_SHOW = c.FAULT_IMG
COM_PORT = "COM5"
BAUD_RATE = 115200
BYTE_SIZE = 8
SERIAL_TIMEOUT = 2
ENDIAN = "big"

# flag so we don't try and open a port twice
is_com_port_open = False

# int main()
if __name__ == '__main__':
    # void loop()
    ser = ""
    img = IMAGE_TO_SHOW
    while True:
        # try and open the serial port if we haven't done so already
        if is_com_port_open is False:
            try:
                ser = serial.Serial(port=COM_PORT, baudrate=BAUD_RATE, bytesize=BYTE_SIZE, timeout=SERIAL_TIMEOUT)
                ser.write(b'\x80')
                ser.flushInput()
                reply = ser.read()
                ser.flushInput()
                reply = int.from_bytes(reply, ENDIAN, signed=False)
                print(reply)
                if reply == 255:
                    is_com_port_open = True

            except serial.SerialException:
                print("Unable to open COM port: " + COM_PORT)
        elif is_com_port_open is True:
            index = 0
            ser.flushInput()
            byte_arr = ser.read(5)
            ser.flushInput()
            b_manip.is_input_valid(byte_arr)
            img = b_manip.get_display_image_path(byte_arr)
            for b in byte_arr:
                print("byte{0}: {1}".format(str(index), (int(b))))
                index += 1
            print("\n")
        # i_manip.display_image(img)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/





