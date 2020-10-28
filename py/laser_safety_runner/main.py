####################################################################
# main.py - implements the main entry point into the program
####################################################################

# imports
import byte_manip as b_manip
import serial
import constants as c
import pygame
from pygame.locals import *

# default image path to no-load
DEFAULT_IMG = c.NO_LOAD_IMG

# flag so we don't try and open a port twice
is_com_port_open = False

# int main()
if __name__ == '__main__':
    # init vars
    ser = ""
    img = DEFAULT_IMG
    # initialize pygame
    pygame.init()

    game_display = pygame.display.set_mode((c.DISPLAY_WIDTH, c.DISPLAY_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption('LASER SAFETY RUNNER')
    py_img = pygame.image.load(img)
    rect = py_img.get_rect(width=570, height=432)
    py_img_last = py_img

    # void loop()
    while True:
        # must handle events in some way
        for event in pygame.event.get():
            if event.type == QUIT:
                is_com_port_open = False
            else:
                continue
        # try and open the serial port if we haven't done so already
        if is_com_port_open is False:
            try:
                # open usb port
                ser = serial.Serial(port=c.COM_PORT, baudrate=c.BAUD_RATE, bytesize=c.BYTE_SIZE,
                                    timeout=c.SERIAL_TIMEOUT)
                ser.write(b'\x80')  # send a call
                ser.flushInput()
                response = ser.read()  # get response
                ser.flushInput()
                # put from bytes to int and check
                response = int.from_bytes(response, c.ENDIAN, signed=False)
                # print(reply) should be 255
                if response == 255:
                    is_com_port_open = True
            #  port failed to open
            except serial.SerialException:
                print("Unable to open COM port: " + c.COM_PORT)
                # stop pygame thread
                pygame.quit()
                # stop the program
                exit()
        # successful port open, so start loop
        elif is_com_port_open is True:
            index = 0
            ser.flushInput()
            # read input from arduino
            byte_arr = ser.read(5)
            ser.flushInput()
            # make sure input is valid
            if b_manip.is_input_valid(byte_arr):
                # input valid, so parse byte array to determine set bits and get appropriate image path str
                img = b_manip.get_display_image_path(b_manip.byte_arr_to_int(byte_arr))
                for b in byte_arr:  # debug
                    print("byte{0}: {1}".format(str(index), (int(b))))
                    index += 1
                print("\n")
            else:
                print("invalid input\n")
        # load image with pygame
        py_img = pygame.image.load(img)
        rect = py_img.get_rect()
        py_img = pygame.transform.scale(py_img, (c.DISPLAY_WIDTH, c.DISPLAY_HEIGHT))
        # only update UI if image path changed
        if py_img != py_img_last:
            game_display.fill((0, 0, 0))
            game_display.blit(py_img, rect)
            pygame.display.update()





