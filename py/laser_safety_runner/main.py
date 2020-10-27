####################################################################
# main.py - implements the main entry point into the program
####################################################################

# imports
import image_manip as manip
from PIL import Image
import serial
import constants

# constants
IMAGE_DIR = "resources/"
IMAGE_JPG = constants.FAULT_IMG
IMAGE_TO_SHOW = IMAGE_DIR + IMAGE_JPG
COM_PORT = "COM5"

# flag so we don't try and open a port twice
isInit = True

# int main()
if __name__ == '__main__':
    # void loop()
    ser = ""
    num_loops = 0
    while True:
        # try and open the serial port if we haven't done so already
        try:
            if isInit is True:
                ser = serial.Serial(port=COM_PORT, baudrate=9600, bytesize=8, timeout=2)
                isInit = False

        except serial.SerialException:
            if num_loops % 10000 == 0:
                print("Unable to open COM port: " + COM_PORT)
            if isInit is False:
                index = 0
                byte_arr = ser.read(5)
                for b in byte_arr:
                    print("byte" + str(index) + ": " + bin(b))
                    index += 1
                print("\n")
            num_loops += 1
        # manip.display_image(IMAGE_TO_SHOW)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
