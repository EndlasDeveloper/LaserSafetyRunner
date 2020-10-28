####################################################################
# main.py - implements the main entry point into the program
####################################################################

# imports
import byte_manip as b_manip
import serial
import constants as c
import pygame
import platform
from pygame.locals import *

# default image path to no-load
DEFAULT_IMG = c.NO_LOAD_IMG


def main(canvas, is_com_port_open):
    # init vars
    ser = ""
    img = DEFAULT_IMG
    # initialize pygame

    py_img_last = ""
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
                # print("Unable to open COM port: " + c.COM_PORT)
                return
        # successful port open, so start loop
        elif is_com_port_open is True:
            i = 0
            ser.flushInput()
            # read input from arduino
            try:
                byte_arr = ser.read(5)
            except serial.serialutil.SerialException:
                print("SerialException")
                display_waiting_for_reply(canvas)
                pygame.display.update()
                main(canvas, False)
                return

            ser.flushInput()
            # make sure input is valid
            if b_manip.is_input_valid(byte_arr):
                # input valid, so parse byte array to determine set bits and get appropriate image path str
                img = b_manip.get_display_image_path(b_manip.byte_arr_to_int(byte_arr))
                for b in byte_arr:  # debug
                    print("byte{0}: {1}".format(str(i), (int(b))))
                    i += 1
                print("\n")
            else:
                print("invalid input\n")
        # load image with pygame
        py_img = pygame.image.load(img)
        # scale image to 95% of screen wid and hit
        py_img = pygame.transform.scale(py_img, (int(0.95 * c.DISPLAY_WIDTH), int(0.95 * c.DISPLAY_HEIGHT)))
        rect = py_img.get_rect()
        # recenter rectangle so there is an even amount of border on each side
        rect = rect.move(int(0.05 * c.DISPLAY_WIDTH / 2), int(0.05 * c.DISPLAY_HEIGHT / 2))
        # only update UI if image path changed
        if py_img != py_img_last:
            py_img_last = py_img
            # background color
            canvas.fill(c.BLACK)
            # draw image
            canvas.blit(py_img, rect)
            # render changes
            pygame.display.update()


####################################################################
# Name: determine_platform
# Description: method that sets COM_PORT to system dependent syntax
####################################################################
def determine_platform():
    platform_info = platform.uname()
    if platform_info.system == 'Windows':
        c.COM_PORT = "COM5"
    elif platform_info.system == 'Raspbian':
        c.COM_PORT = "/dev/ttyS0"
    print(platform_info)


# int main()
def display_waiting_for_reply(display_canvas):
    display_canvas.fill(c.SKY_BLUE)
    pygame.init()
    pygame.display.set_caption('LASER SAFETY RUNNER')
    font = pygame.font.Font('freesansbold.ttf', 40)
    text = font.render('Waiting for input device reply...', True, c.LIGHT_BLUE, c.NAVY)
    text_rect = text.get_rect(center=(int(c.DISPLAY_WIDTH / 2), int(c.DISPLAY_HEIGHT / 2)))
    display_canvas.blit(text, text_rect)


if __name__ == '__main__':
    determine_platform()
    val = 99999
    index = 1
    canvas = pygame.display.set_mode((c.DISPLAY_WIDTH, c.DISPLAY_HEIGHT), pygame.FULLSCREEN)
    display_waiting_for_reply(canvas)
    # render changes
    pygame.display.update()
    main(canvas, False)
    while True:
        index += 1
        main(canvas, False)

