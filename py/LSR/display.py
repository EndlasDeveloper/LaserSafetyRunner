############################################################
# File: display.py
# Description: file holding the display object for the program.
#              This object is in charge of accepting new input
#              states, comparing to the current one, and changing
#              the display if necessary
############################################################

# imports
from constant_masks import *
from constant_img_paths import *
from constant_display import *
import pygame
from serial_util import *

# to get pygame to display full screen, must set display w and h to 640, 480 and set full screen flag
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480


###############################################################
# Class: Display
# Description: Display object that handles updating the
#              display monitor thread
###############################################################
class Display:

    ####################################################################
    # Name: constructor
    # Description: initializes a buffer to hold a copy of result_var,
    #              the state (the half bytes converted into an int).
    #              image path and a flag for setting up pygame events.
    ####################################################################
    def __init__(self):
        # the current state of the system
        self.state = 0

        # pygame images
        self.py_img_last = ""
        self.py_img_obj = None
        self.last_py_img_path = ""
        self.img_path = ""
        self.last_img_path = ""

        # initialize pygame
        pygame.init()
        # setup canvas
        self.main_canvas = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)
        # render initial waiting to connect message
        self.display_system_waiting(OPENING_COM_PORTS_MSG, True)

    ####################################################################
    # Name: display_system_waiting
    # Description: handles setting up the waiting screen and rendering
    ####################################################################
    def display_system_waiting(self, msg, is_init_screen):
        try:
            # if screen is initialized, background sky blue
            if is_init_screen:
                self.main_canvas.fill(SKY_BLUE)
            # initialize pygame
            pygame.init()
            # set window title message
            pygame.display.set_caption(DISPLAY_CAPTION_MSG)
            # set font for the waiting for reply msg
            font = pygame.font.Font(DISPLAY_FONT, DISPLAY_FONT_SIZE)
            # set the text str, background color, and text color
            text = font.render(msg, True, LIGHT_BLUE, NAVY)
            # center the waiting msg
            text_rect = text.get_rect(center=(int(DISPLAY_WIDTH / 2), int(DISPLAY_HEIGHT / 2)))
            # update canvas and render the waiting for reply msg
            self.main_canvas.blit(text, text_rect)
            pygame.display.update()
        except BaseException:
            from traceback import print_exc
            print_exc()
            return

    ###############################################################################
    # Name: update_display
    # Description: looks if the ports are still open. If not, waiting msg is
    #              rendered. Otherwise, the new state is hashed, and the image
    #              updated based on the hashed flags
    ###############################################################################
    def update_display(self, state):
        # state is same as before, so just return
        if state == self.state:
            return
        self.state = state
        if self.display_determine_waiting() is not True:
            # display laser safety image
            self.update_pygame_image()

    #######################################################################################
    # Name: _get_display_image_path
    # Description: Uses state to decide image path. Method returns the appropriate image
    #              path as a string.
    #######################################################################################
    def get_display_image_path(self):
        states = self.hash_state()
        if states[LASER_FIRE_MASK]:
            return LASER_FIRE_IMG
        elif states[THRESHOLD_MASK]:
            return LASER_FIRE_IMG
        elif states[SHUTTER_MASK]:
            return LASER_FIRE_IMG
        elif states[PROGRAM_MASK]:
            return LASER_FIRE_IMG
        elif states[ESTOP_MASK]:
            return ESTOP_IMG
        elif states[SAFETY_CIRCUIT_MASK]:
            return SAFETY_CIRCUIT_IMG
        elif states[DEFEAT_SAFETY_MASK]:
            return DEFEAT_SAFETY_IMG
        elif states[WARNING_MASK]:
            return WARNING_IMG
        elif states[FAULT_MASK]:
            return FAULT_IMG
        elif states[SLEEP_MASK]:
            return SLEEP_IMG
        elif states[FIBER_ERROR_MASK]:
            return FIBER_ERROR_IMG
        else:
            return NO_LOAD_IMG

    ######################################################################################
    # Name: hash_state
    # Description: maps the state mask to a bool indicating whether the bit for that mask
    #              was set and returns the dict
    ######################################################################################
    def hash_state(self):
        return {LASER_FIRE_MASK: (self.state & LASER_FIRE_MASK) > 0,
                THRESHOLD_MASK: (self.state & THRESHOLD_MASK) > 0, SHUTTER_MASK: (self.state & SHUTTER_MASK) > 0,
                PROGRAM_MASK: (self.state & PROGRAM_MASK) > 0, ESTOP_MASK: (self.state & ESTOP_MASK) > 0,
                SAFETY_CIRCUIT_MASK: (self.state & SAFETY_CIRCUIT_MASK) > 0,
                DEFEAT_SAFETY_MASK: (self.state & DEFEAT_SAFETY_MASK) > 0,
                WARNING_MASK: (self.state & WARNING_MASK) > 0, FAULT_MASK: (self.state & FAULT_MASK) > 0,
                SLEEP_MASK: (self.state & SLEEP_MASK) > 0, FIBER_ERROR_MASK: (self.state & FIBER_ERROR_MASK) > 0}

    #######################################################################
    # Name: _update_pygame_image
    # Description: helper method to update the image, scale it, center,
    #              and render the changes
    #######################################################################
    def update_pygame_image(self):
        self.img_path = self.get_display_image_path()
        # display waiting message if com port connection failure
        if self.display_determine_waiting() is not True:
            print("av last py img path: " + self.last_py_img_path)
            print("img path: " + self.img_path)
            # change stuff only if stuff changed
            if self.last_py_img_path != self.img_path:
                self.py_img_last = self.img_path
                # load image with pygame
                # scale image to 95% of screen wid and hit
                self.py_img_obj = pygame.image.load(self.img_path)
                self.py_img_obj = pygame.transform.scale(self.py_img_obj, (int(0.95 * DISPLAY_WIDTH),
                                                                           int(0.95 * DISPLAY_HEIGHT)))
                # get reference to the image rectangle
                rect = self.py_img_obj.get_rect()
                # recenter rectangle so there is an even amount of border on each side
                rect = rect.move(int(0.05 * DISPLAY_WIDTH / 2), int(0.05 * DISPLAY_HEIGHT / 2))
                # background color
                self.main_canvas.fill(BLACK)
                # draw image
                self.main_canvas.blit(self.py_img_obj, rect)
                # render changes
                pygame.display.update()

    #######################################################################
    # Name: display_determine_waiting
    # Description: helper method to avoid code copying
    #######################################################################
    def display_determine_waiting(self):
        if not av.is_com_port_open and not av.has_port_connected_before:
            self.display_system_waiting(OPENING_COM_PORTS_MSG, True)
            return True
        elif not av.is_com_port_open and av.has_port_connected_before:
            self.display_system_waiting(OPENING_COM_PORTS_MSG, False)
            return True
        else:
            return False

