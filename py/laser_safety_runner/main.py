####################################################################
# main.py - implements the main entry point into the program
####################################################################

# imports
import image_manip as manip
from PIL import Image
import serial

# constants
IMAGE_DIR = "resources/"
IMAGE_JPG = "fault.jpg"
IMAGE_TO_SHOW = IMAGE_DIR + IMAGE_JPG
COM_PORT = 'COM5'

isInit = True

# int main()
if __name__ == '__main__':

    while True:
        try:
            if isInit is True:
                isInit = False
                ser = serial.Serial(port=COM_PORT, baudrate=9600, bytesize=8, timeout=2)

            input_byte0 = ser.read(1)
            print(bin(int.from_bytes(input_byte0, byteorder="big", signed=False)))

            input_byte1 = ser.read(1)
            print(bin(int.from_bytes(input_byte1, byteorder="big", signed=False)))

            input_byte2 = ser.read(1)
            print(bin(int.from_bytes(input_byte2, byteorder="big", signed=False)))

            input_byte3 = ser.read(1)
            print(bin(int.from_bytes(input_byte3, byteorder="big", signed=False)))

            input_byte4 = ser.read(1)
            print(bin(int.from_bytes(input_byte4, byteorder="big", signed=False)))

            print("\n")
            # manip.display_image(IMAGE_TO_SHOW)

        except serial.SerialException:
            print("Unable to open COM port: " + COM_PORT)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
