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


#########################################################################
# Name: run_debug_prints_for_inputs
# Description: debugging method that prints the 4 data bytes in
#              byte_arr
#########################################################################
def run_debug_prints_for_inputs(byte_arr):
    i = 0
    for b in byte_arr:  # debug
        print("byte{0}: {1}".format(str(i), (int(b))))
        i += 1
    print("\n")


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
        if response == 255:
            c.is_com_port_open = True
            return True
    #  port failed to open
    except serial.SerialException:
        c.is_com_port_open = False
        return False


#######################################################################
# Name: update_image
# Description: helper method to update the image, scale it, center,
#              and render the changes
#######################################################################
def update_image(canvas, img):
    # load image with pygame
    py_img = pygame.image.load(img)
    # scale image to 95% of screen wid and hit
    py_img = pygame.transform.scale(py_img, (int(0.95 * c.DISPLAY_WIDTH), int(0.95 * c.DISPLAY_HEIGHT)))
    rect = py_img.get_rect()
    # recenter rectangle so there is an even amount of border on each side
    rect = rect.move(int(0.05 * c.DISPLAY_WIDTH / 2), int(0.05 * c.DISPLAY_HEIGHT / 2))
    # only update UI if image path changed
    if py_img != c.py_img_last:
        c.py_img_last = py_img
        # background color
        canvas.fill(c.BLACK)
        # draw image
        canvas.blit(py_img, rect)
        # render changes
        pygame.display.update()


#######################################################################
# Name: handle_serial_exception
# Description: routine to execute upon a serial exception being thrown
#######################################################################
def handle_serial_exception(canvas):
    print("SerialException")
    c.is_com_port_open = False
    display_waiting_for_reply(canvas, False)
    pygame.display.update()


#######################################################################
# Name: loop
# Description: main function body to be looped through
#######################################################################
def loop(canvas):
    # init vars
    img = DEFAULT_IMG
    # must handle events in some way
    setup_pygame_events()
    # ports not open yet, so try to open, sent a call, and wait for a response
    if not c.is_com_port_open and not open_port_and_send_callout():
        return
    # successful port open, so start loop
    if c.is_com_port_open is True:
        # read input from arduino
        try:
            byte_arr = c.ser.read(5)
        except serial.serialutil.SerialException:
            handle_serial_exception(canvas)
            return
        # make sure input is valid
        if b_manip.is_input_valid(byte_arr):
            run_debug_prints_for_inputs(byte_arr)
            # input valid, so parse byte array to determine set bits and get appropriate image path str
            img = b_manip.get_display_image_path(b_manip.byte_arr_to_int(byte_arr))
        update_image(canvas, img)


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


############################################################################
# Name: display_waiting_for_reply
# Description: method that takes the display canvas, and whether
#              it is an initial wait display or signal has been interrupted
############################################################################
def display_waiting_for_reply(display_canvas, is_init_screen):
    if is_init_screen:
        display_canvas.fill(c.SKY_BLUE)
    pygame.init()
    pygame.display.set_caption('LASER SAFETY RUNNER')
    font = pygame.font.Font('freesansbold.ttf', 40)
    text = font.render('Waiting for input device reply...', True, c.LIGHT_BLUE, c.NAVY)
    text_rect = text.get_rect(center=(int(c.DISPLAY_WIDTH / 2), int(c.DISPLAY_HEIGHT / 2)))
    display_canvas.blit(text, text_rect)


# int main()
if __name__ == '__main__':
    determine_platform()
    main_canvas = pygame.display.set_mode((c.DISPLAY_WIDTH, c.DISPLAY_HEIGHT), pygame.FULLSCREEN)
    display_waiting_for_reply(main_canvas, True)
    # render changes
    pygame.display.update()
    while True:
        loop(main_canvas)

