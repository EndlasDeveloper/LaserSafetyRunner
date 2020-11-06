####################################################################
# main.py - implements the main entry point into the program
####################################################################

# imports
from vars_consts import serial_flags_and_vars as sfv, globals_and_consts as gc
from manip import byte_manip as b_manip
import serial
import resources.colors as c
import pygame
import serial.tools.list_ports
from pygame.locals import *
import debug_print as debug


#########################################################################
# Name: setup_pygame_events
# Description: sets up the pygame event handlers
#########################################################################
def setup_pygame_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            gc.is_com_port_open = False


#############################################################################
# Name: open_port_and_send_call_out
# Description: tries to open the com port, if successful, a callout is
#              sent over serial. The arduino looks at the callout, and
#              if the callout is expected, the arduino returns a reply,
#              and if the reply is what is expected, the port is considered
#              open.
#############################################################################
def open_port_and_flag_result():
    try:
        # open USB port
        sfv.ser = serial.Serial(port=gc.COM_PORT, baudrate=gc.BAUD_RATE, bytesize=gc.BYTE_SIZE,
                                timeout=gc.SERIAL_TIMEOUT)
        response = sfv.ser.read()  # get response
        # cast response into an int
        response = int.from_bytes(response, gc.ENDIAN, signed=False)
        # verify response
        if response == 255:
            # write back a magic byte
            sfv.ser.write(b'/x1')
            # read serial into an int
            second_response = int.from_bytes(sfv.ser.read(), gc.ENDIAN, signed=False)
            # verify response
            if second_response == 0:
                # device connect success, so set connected flags
                set_open_port_flags()
                return True
        else:
            return False
    # something went wrong with serial com port
    except serial.SerialException:
        # set flag for is port open to false
        invalidate_open_port_flags()
        # update display with a waiting for response from input device
        display_system_waiting(gc.WAITING_FOR_INPUT_DEVICE_MSG, True)
        # failed, so return false
        return False


#######################################################################
# Name: update_image
# Description: helper method to update the image, scale it, center,
#              and render the changes
#######################################################################
def update_image(img):
    # change stuff only if stuff changed
    if img != gc.py_img_last:
        gc.py_img_last = img
        # load image with pygame
        gc.py_img = pygame.image.load(img)
        # scale image to 95% of screen wid and hit
        gc.py_img = pygame.transform.scale(gc.py_img, (int(0.95 * gc.DISPLAY_WIDTH), int(0.95 * gc.DISPLAY_HEIGHT)))
        # get reference to the image rectangle
        rect = gc.py_img.get_rect()
        # recenter rectangle so there is an even amount of border on each side
        rect = rect.move(int(0.05 * gc.DISPLAY_WIDTH / 2), int(0.05 * gc.DISPLAY_HEIGHT / 2))
        # only update UI if image path changed
        gc.py_img_last = gc.py_img
        # background color
        gc.main_canvas.fill(c.BLACK)
        # draw image
        gc.main_canvas.blit(gc.py_img, rect)
        # render changes
        pygame.display.update()


#######################################################################
# Name: handle_serial_exception
# Description: routine to execute upon a serial exception being thrown
#######################################################################
def handle_serial_exception():
    # indicate com port is closed
    invalidate_open_port_flags()
    # show waiting for device response
    display_system_waiting(gc.WAITING_FOR_INPUT_DEVICE_MSG, False)
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
    try:
        # try and read in the correct byte arr size
        sfv.serial_in_buffer = sfv.ser.read(gc.READ_BYTE_SIZE)
        # this just prints the read byte array to console
        debug.Debugger.print_byte_arr(sfv.serial_in_buffer)
        return True
        # walk through the buffer and verify
    except serial.SerialException:  # read failed
        # set proper flags to indicate port needs to be re-opened
        handle_serial_exception()
        return False


####################################################################
# Name: determine_platform
# Description: method that sets COM_PORT to system dependent syntax
####################################################################
def determine_platform_and_connect():
    if sfv.this_platform == gc.WIN:
        gc.COM_PORT = "COM5"
        if open_port_and_flag_result():
            return True
        # com 5 didn't work, so try 'em all
        if not gc.found_platform:
            for com_num in range(9):
                gc.COM_PORT = "COM" + str(com_num)
                try:
                    # try to connect to each, see if a response from the arduino returns
                    if open_port_and_flag_result():
                        return True
                except ModuleNotFoundError:  # failed to connect to arduino so continue trying other ports
                    continue

    if sfv.this_platform == gc.LIN:
        if is_port_set():
            for i in range(9):  # iterate through all possible COM ports
                gc.COM_PORT = "/dev/ttyUSB" + str(i)
                try:
                    # try to connect to each, see if a response from the arduino returns
                    if open_port_and_flag_result():
                        return True
                except ModuleNotFoundError:  # failed to connect to arduino so continue trying other ports
                    handle_serial_exception()
                    continue
    return False


#########################################################
# Name: set_open_port_flags
# Description: helper method that sets the port flags to open
#########################################################
def set_open_port_flags():
    sfv.HAS_PORT_CONNECTED = True
    sfv.is_com_port_open = True
    sfv.FOUND_PLATFORM = True


##################################################################
# Name: invalidate_open_port_flags
# Description: helper method that invalidates port flags to open
##################################################################
def invalidate_open_port_flags():
    sfv.HAS_PORT_CONNECTED = False
    sfv.is_com_port_open = False
    sfv.FOUND_PLATFORM = False


#################################################################################################
# Name: is_port_set
# Description: returns bool describing whether the port is set and ready to communicate through
#################################################################################################
def is_port_set():
    return sfv.HAS_PORT_CONNECTED & sfv.is_com_port_open & sfv.FOUND_PLATFORM


############################################################################
# Name: display_waiting_for_reply
# Description: method that takes the display canvas, and whether
#              it is an initial wait display or signal has been interrupted
############################################################################
def display_system_waiting(msg, is_init_screen):
    try:
        # if screen is initialized, background sky blue
        if is_init_screen:
            gc.main_canvas.fill(c.SKY_BLUE)
        # initialize pygame
        pygame.init()
        # set window title message
        pygame.display.set_caption(gc.DISPLAY_CAPTION_MSG)
        # set font for the waiting for reply msg
        font = pygame.font.Font(gc.DISPLAY_FONT, gc.DISPLAY_FONT_SIZE)
        # set the text str, background color, and text color
        text = font.render(msg, True, c.LIGHT_BLUE, c.NAVY)
        # center the waiting msg
        text_rect = text.get_rect(center=(int(gc.DISPLAY_WIDTH / 2), int(gc.DISPLAY_HEIGHT / 2)))
        # update canvas and render the waiting for reply msg
        gc.main_canvas.blit(text, text_rect)
        pygame.display.update()
    except pygame.error():
        return


#######################################################################
# Name: loop
# Description: main function body to be looped through
#######################################################################
def loop():
    setup_pygame_events()
    # check if the port is open, if not try and set it up
    if not is_port_set():
        setup(gc.WAITING_FOR_INPUT_DEVICE_MSG, False)
        set_open_port_flags()
        if not open_port_and_flag_result():  # open port failed, so make sure flag is set and return
            handle_serial_exception()
    # successful port open, so start loop
    else:
        # read input from input device (fills s.serial_in_buffer)
        if read_input_bytes():
            debug.Debugger.print_byte_arr(sfv.serial_in_buffer)
            # make sure there's a buffer and the input is valid
            if b_manip.is_input_valid(sfv.serial_in_buffer):
                image = b_manip.get_display_image_path(b_manip.byte_arr_to_int(sfv.serial_in_buffer))
                print("image: " + image)
                update_image(image)


##################################################################################################
# Name: setup
# Description: helper method to initialize counter variables, display a startup msg/img while
#              system finished initializing, and initializes and signals the arduino
##################################################################################################
def setup(display_msg, is_initial_setup):
    # display image indicating searching for com ports
    if is_initial_setup:
        display_system_waiting(display_msg, is_initial_setup)

    open_port_and_flag_result()
    # if the local systems platform can be determined
    if is_port_set():
        if determine_platform_and_connect():
            set_open_port_flags()
            print("determine plat and connect true")


# int main()
if __name__ == '__main__':
    setup(gc.OPENING_COM_PORTS_MSG, True)
    # void loop()
    while True:
        loop()
