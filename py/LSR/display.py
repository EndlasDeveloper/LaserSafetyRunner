from constant_serial import *
from constant_mask import *
from const_img_paths import *
from constant_display import *
import app_vars as av
import pygame
from serial_util import *
from time import sleep


class Display:
    def __init__(self):
        self.buffer = []
        self.state = 0
        self.img_path = ""
        self._setup_pygame_events()

    @staticmethod
    def display_system_waiting(msg, is_init_screen):
        try:
            # if screen is initialized, background sky blue
            if is_init_screen:
                av.main_canvas.fill(SKY_BLUE)
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
            av.main_canvas.blit(text, text_rect)
            pygame.display.update()
        except pygame.error():
            return

    def update_display(self, state):
        self.state = state
        print("Display state: "+str(self.state))
        # display waiting message if com port connection failure
        print("is_com_port_open, has_port_connected_before: " + str(av.is_com_port_open) + ", " + str(av.has_port_connected_before))
        if not av.is_com_port_open and not av.has_port_connected_before:
            self.display_system_waiting(WAITING_FOR_INPUT_DEVICE_MSG, True)
        elif not av.is_com_port_open and av.has_port_connected_before and av.found_platform:
            self.display_system_waiting(OPENING_COM_PORTS_MSG, False)
        else:

            self.update_pygame_image()
        # release the data buffer mutex

    #######################################################################################
    # Name: _get_display_image_path
    # Description: takes an integer as a parameter. Method returns the appropriate image
    #              path as a string.
    #######################################################################################
    def _get_display_image_path(self):
        states = self._hash_state()
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
    def _hash_state(self):
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
        self.img_path = self._get_display_image_path()
        print(self.img_path)
        # display waiting message if com port connection failure
        if not av.is_com_port_open and not av.has_port_connected_before:
            self.display_system_waiting(OPENING_COM_PORTS_MSG, True)
        elif not av.is_com_port_open and av.has_port_connected_before:
            self.display_system_waiting(OPENING_COM_PORTS_MSG, False)
        else:
            print("img path: " + self.img_path)
            # change stuff only if stuff changed
            if av.last_py_img_path != self.img_path:
                av.py_img_last = self.img_path
                # load image with pygame
                # scale image to 95% of screen wid and hit
                av.py_img = pygame.image.load(self.img_path)
                av.py_img = pygame.transform.scale(av.py_img, (int(0.95 * DISPLAY_WIDTH), int(0.95 * DISPLAY_HEIGHT)))
                # get reference to the image rectangle
                rect = av.py_img.get_rect()
                # recenter rectangle so there is an even amount of border on each side
                rect = rect.move(int(0.05 * DISPLAY_WIDTH / 2), int(0.05 * DISPLAY_HEIGHT / 2))
                # background color
                av.main_canvas.fill(BLACK)
                # draw image
                av.main_canvas.blit(av.py_img, rect)
                # render changes
                pygame.display.update()

    @staticmethod
    def _setup_pygame_events():
        # get all events
        for event in pygame.event.get():
            # when a key is pressed
            if event.type == pygame.KEYDOWN:
                # if the key is esc or q, the program exits gracefully
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    exit(0)


