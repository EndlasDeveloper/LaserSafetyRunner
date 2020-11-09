####################################################################
# main.py - implements the main entry point into the program
####################################################################

# imports
import serial_flags_and_vars as sfv
import globals_and_consts as gc
import byte_manip as b_manip
import masks as m
import serial
import colors as c
import pygame
import serial.tools.list_ports
from pygame.locals import *
import time
import debug_print as debug


#########################################################################
# Name: setup_pygame_events
# Description: sets up the pygame event handlers
#########################################################################
def setup_pygame_events():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                pygame.quit()
                exit()


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

        print(gc.COM_PORT)
        response = sfv.ser.read()  # get response
        # cast response into an int
        response = int.from_bytes(response, gc.ENDIAN, signed=False)
        print(response)
        # verify response
        if response == 1:
            # write back a magic byte
            sfv.ser.write(int.to_bytes(response, length=1, byteorder=gc.ENDIAN, signed=False))
            set_open_port_flags()
            return True
        else:
            return False
    except serial.SerialException:
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
    while sfv.ser.in_waiting > 0:
        if gc.serial_count == 6:
            gc.serial_count = 0
        try:
            # try and read in the next byte
            gc.serial_in_buffer[gc.serial_count] = sfv.ser.read()
            # if header bits are set in data bytes or the serial count exceeds the buffer size
            if gc.serial_count >= 5:
                # check if the ard reset counts bit is set, if so, send signal to ard to reset counts
                if b_manip.byte_to_int(gc.serial_in_buffer[gc.serial_count]) & m.ARD_RESET_MASK > 0:
                    print("Arduino triggered the watchdog")
                    # sfv.ser.write(gc.RESET_COUNTS_FLAG_BYTE)

                # check if the ard inputs ready bit is set, if so, read in the 6 bytes from the ard
                if b_manip.byte_to_int(gc.serial_in_buffer[gc.serial_count]) & m.ARD_REPORT_ERROR_MASK > 0:
                    print("Arduino reporting at least 1 error")
                gc.inputs_from_ard = b_manip.byte_arr_to_int(gc.serial_in_buffer)

                if gc.serial_in_buffer[0] == gc.inputs_from_ard % 128:
                    print("Checksum matched!")
                    sfv.ser.write(gc.serial_in_buffer[0])
                else:
                    print("Checksum didn't match :/")
            else:
                gc.serial_count += 1
            # # this just prints the read byte array to console
            # debug.Debugger.print_byte_arr(gc.serial_in_buffer)
            # walk through the buffer and verify
        except serial.SerialException:  # read failed
            # set proper flags to indicate port needs to be re-opened
            handle_serial_exception()


####################################################################
# Name: determine_platform
# Description: method that sets COM_PORT to system dependent syntax
####################################################################
def determine_platform_and_connect():
    if sfv.this_platform == gc.WIN:
        gc.COM_PORT_PREFIX = "COM"
        sfv.FOUND_PLATFORM = True
    if sfv.this_platform == gc.LIN:
        gc.COM_PORT_PREFIX = "/dev/ttyUSB"
        sfv.FOUND_PLATFORM = True
    for com_num in range(9):
        gc.COM_PORT = gc.COM_PORT_PREFIX + str(com_num)
        # try to connect to each, see if a response from the arduino returns
        if open_port_and_flag_result():
            set_open_port_flags()
            return True
        else:
            continue
    return False


#########################################################
# Name: set_open_port_flags
# Description: helper method that sets the port flags to open
#########################################################
def set_open_port_flags():
    sfv.HAS_PORT_CONNECTED = True
    sfv.is_com_port_open = True


##################################################################
# Name: invalidate_open_port_flags
# Description: helper method that invalidates port flags to open
##################################################################
def invalidate_open_port_flags():
    sfv.HAS_PORT_CONNECTED = False
    sfv.is_com_port_open = False


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


def check_time_for_ard():
    gc.last_clock = time.perf_counter()

    if gc.last_clock - gc.init_clock >= 1:
        gc.init_clock = time.perf_counter()
        gc.last_clock = time.perf_counter()
        try:
            # sfv.ser.write(170)
            read_input_bytes()
            print("checksum: " + str(b_manip.byte_to_int(bytes(gc.serial_in_buffer[0]))))
            print("modded ard input: " + str(gc.inputs_from_ard % 128))
            if b_manip.byte_to_int(bytes(gc.serial_in_buffer[1])) == gc.inputs_from_ard % 128:
                sfv.ser.write(gc.serial_in_buffer[1])
                return True
            else:
                print("Checksum didn't match.")
                temp = []
                for index in range(6):
                    temp.append(b_manip.byte_to_int(bytes(gc.serial_in_buffer[index])))
                print(temp)
        except serial.SerialException:
            return False
    return False


def check_and_update_img():
    if b_manip.is_input_valid(gc.serial_in_buffer):
        print("is valid input")
        image = b_manip.get_display_image_path(b_manip.byte_arr_to_int(gc.serial_in_buffer))
        print("image: " + image)
        update_image(image)
    print("invalid input")
    # sfv.ser.flushInput()


#######################################################################
# Name: loop
# Description: main function body to be looped through
#######################################################################
def loop():
    setup_pygame_events()
    # check if the port is open, if not try and set it up
    if not is_port_set():
        setup(gc.WAITING_FOR_INPUT_DEVICE_MSG, False)

    # successful port open, so start loop
    if is_port_set() and check_time_for_ard():
        check_and_update_img()
        debug.Debugger.print_byte_arr(gc.serial_in_buffer)
        # make sure there's a buffer and the input is valid
        # time.sleep(0.5)


##################################################################################################
# Name: setup
# Description: helper method to initialize counter variables, display a startup msg/img while
#              system finished initializing, and initializes and signals the arduino
##################################################################################################
def setup(display_msg, is_initial_setup):
    # display image indicating searching for com ports
    if is_initial_setup:
        display_system_waiting(display_msg, is_initial_setup)

    if determine_platform_and_connect():
        set_open_port_flags()
        print("Connected to com: " + gc.COM_PORT)


# int main()
if __name__ == '__main__':
    gc.init_clock = time.perf_counter()
    setup(gc.OPENING_COM_PORTS_MSG, True)
    # void loop()
    while True:
        loop()
