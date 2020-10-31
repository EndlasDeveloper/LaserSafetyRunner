####################################################################
# main.py - implements the main entry point into the program
####################################################################

# imports
import byte_manip as b_manip
import serial
import globals_and_consts as c
import pygame
import platform
import serial.tools.list_ports
from pygame.locals import *
import datetime
import os
import sys
import debug_print as debug

# default image path to no-load
DEFAULT_IMG = c.NO_LOAD_IMG


#########################################################################
# Name: setup_pygame_events
# Description: sets up the pygame event handlers
#########################################################################
def setup_pygame_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            c.is_com_port_open = False


#############################################################################
# Name: open_port_and_send_call_out
# Description: tries to open the com port, if successful, a callout is
#              sent over serial. The arduino looks at the callout, and
#              if the callout is expected, the arduino returns a reply,
#              and if the reply is what is expected, the port is considered
#              open.
#############################################################################
def open_port_and_send_callout():
    try:
        # open usb port
        c.ser = serial.Serial(port=c.COM_PORT, baudrate=c.BAUD_RATE, bytesize=c.BYTE_SIZE,
                              timeout=c.SERIAL_TIMEOUT)
        c.ser.write(b'\x80')  # send a call
        response = c.ser.read()  # get response
        c.ser.flushInput()
        # put from bytes to int and check
        response = int.from_bytes(response, c.ENDIAN, signed=False)
        # print(reply) should be 255
        if response != 0:
            c.is_com_port_open = True
            return True
        else:
            debug.Debugger.print_bad_ard_response(response)
    #  port failed to open
    except serial.SerialException:
        c.is_com_port_open = False
        display_system_waiting(c.WAITING_FOR_INPUT_DEVICE_MSG, True)
        return False


#######################################################################
# Name: update_image
# Description: helper method to update the image, scale it, center,
#              and render the changes
#######################################################################
def update_image(img):
    if datetime.datetime.now().microsecond > c.current_millis:
        c.current_millis = datetime.datetime.now().microsecond
        c.ser.write(c.CONTACT_TO_ARD_FLAG_BYTE)

    # load image with pygame
    py_img = pygame.image.load(img)

    # change stuff only if stuff changed
    if py_img != c.py_img_last:
        # scale image to 95% of screen wid and hit
        py_img = pygame.transform.scale(py_img, (int(0.95 * c.DISPLAY_WIDTH), int(0.95 * c.DISPLAY_HEIGHT)))
        # get reference to the image rectangle
        rect = py_img.get_rect()
        # recenter rectangle so there is an even amount of border on each side
        rect = rect.move(int(0.05 * c.DISPLAY_WIDTH / 2), int(0.05 * c.DISPLAY_HEIGHT / 2))
        # only update UI if image path changed
        c.py_img_last = py_img
        # background color
        c.main_canvas.fill(c.BLACK)
        # draw image
        c.main_canvas.blit(py_img, rect)
        # render changes
        pygame.display.update()


#######################################################################
# Name: handle_serial_exception
# Description: routine to execute upon a serial exception being thrown
#######################################################################
def handle_serial_exception():
    # indicate com port is closed
    c.is_com_port_open = False
    # show waiting for device response
    display_system_waiting(c.WAITING_FOR_INPUT_DEVICE_MSG, False)
    # render changes
    pygame.display.update()


####################################################################
# Name: read_input_bytes
# Description: tries to read in 5 bytes over the open serial
#              port. If it fails, a handler is called where
#              values and flags are set to try and re-open
#              the port
####################################################################
def read_input_bytes():
    # try and read the 5 byte array
    try:
        return c.ser.read(5)
    except serial.SerialException:  # read failed
        # set proper flags to indicate port needs to be re-opened
        handle_serial_exception()
        return None


####################################################################
# Name: determine_platform
# Description: method that sets COM_PORT to system dependent syntax
####################################################################
def determine_platform_and_connect():
    # see if we're on windows platform
    if c.this_platform == c.WIN and not c.HAS_PORT_CONNECTED:
        for i in range(9):  # iterate through all possible COM ports
            c.COM_PORT = "COM" + str(i)
            debug.Debugger.print_com_port(c.COM_PORT)
            try:
                if open_port_and_send_callout():  # try to connect to each, see if a response from the arduino returns
                    c.HAS_PORT_CONNECTED = True
                    return True
            except ModuleNotFoundError:  # failed to connect to arduino so continue trying other ports
                continue

    # debug statement indicating all windows attempts to open a port failed
    debug.Debugger.print_no_com_port_for_platform(c.WIN)
    if c.this_platform == c.LIN and not c.HAS_PORT_CONNECTED:
        for i in range(9):  # iterate through all possible COM ports
            c.COM_PORT = "/dev/ttyUSB" + str(i)
            debug.Debugger.print_com_port(c.COM_PORT)
            try:
                if open_port_and_send_callout():  # try to connect to each, see if a response from the arduino returns
                    c.HAS_PORT_CONNECTED = True
                    return True
            except ModuleNotFoundError:  # failed to connect to arduino so continue trying other ports
                continue
    return False


############################################################################
# Name: display_waiting_for_reply
# Description: method that takes the display canvas, and whether
#              it is an initial wait display or signal has been interrupted
############################################################################
def display_system_waiting(msg, is_init_screen):
    try:
        # if screen is initialized, background sky blue
        if is_init_screen:
            c.main_canvas.fill(c.SKY_BLUE)
        # initialize pygame
        pygame.init()
        # set window title message
        pygame.display.set_caption(c.DISPLAY_CAPTION)
        # set font for the waiting for reply msg
        font = pygame.font.Font(c.DISPLAY_FONT, c.DISPLAY_FONT_SIZE)
        # set the text str, background color, and text color
        text = font.render(msg, True, c.LIGHT_BLUE, c.NAVY)
        # center the waiting msg
        text_rect = text.get_rect(center=(int(c.DISPLAY_WIDTH / 2), int(c.DISPLAY_HEIGHT / 2)))
        # update canvas and render the waiting for reply msg
        c.main_canvas.blit(text, text_rect)
        pygame.display.update()
        return True
    except pygame.error():
        return False


############################################################################
# Name: initialize_and_contact_ard
# Description: method to send signal to the arduino to reset its counter
#              type variables and ask it for a verification response
############################################################################
def initialize_and_contact_ard():
    # tell arduino to reset its count variables
    try:
        c.ser.write(c.RESET_COUNTS_FLAG_BYTE)
    except serial.SerialException:
        debug.Debugger.print_serial_exception("RESET_COUNTS WRITE EXCEPTION")
        handle_serial_exception()
        return False
    try:
        c.ser.write(c.CONTACT_TO_ARD_FLAG_BYTE)
    except serial.SerialException:
        debug.Debugger.print_serial_exception("CONTACT_TO_ARD")
        handle_serial_exception()
        return False


#######################################################################
# Name: loop
# Description: main function body to be looped through
#######################################################################
def loop():
    # must handle events in some way
    setup_pygame_events()
    # ports not open yet, so try to open, sent a call, and wait for a response
    if not c.is_com_port_open:
        img = DEFAULT_IMG
        setup(c.WAITING_FOR_INPUT_DEVICE_MSG, False)
        if open_port_and_send_callout():
            return
    # successful port open, so start loop
    if c.is_com_port_open is True:
        # read input from arduino
        byte_arr = read_input_bytes()
        if byte_arr is None:
            return
        # make sure input is valid
        if b_manip.is_input_valid(byte_arr):
            debug.Debugger.print_byte_arr(byte_arr)
            # input valid, so parse byte array to determine set bits and get appropriate image path str
            img = b_manip.get_display_image_path(b_manip.byte_arr_to_int(byte_arr))
        update_image(img)


##################################################################################################
# Name: setup
# Description: helper method to initialize counter variables, display a startup msg/img while
#              system finished initializing, and initializes and signals the arduino
##################################################################################################
def setup(display_msg, is_init):
    # display image indicating searching for com ports
    if display_system_waiting(display_msg, is_init):
        # if the local systems platform can be determined
        if determine_platform_and_connect():
            initialize_and_contact_ard()


# int main()
if __name__ == '__main__':
    setup(c.OPENING_COM_PORTS, True)
    # void loop()
    while True:
        loop()
