##########################################################
# File: laser_safety_runner.py
# Description: Class in charge of controlling the
#              flow of the program. Nothing too detailed
#              should be implemented in this class
#########################################################

# imports
from mocks_and_stubs import *
from display import Display
import pygame


############################################################################
# Class: LaserSafetyRunner
# Description: manages the multi-threading capability of the app.
############################################################################
class LaserSafetyRunner:

    #########################################################################
    # Name: constructor
    # Description: LaserSafetyRunner constructor that initializes Display obj
    #              and the ArduinoListener obj. It also initializes the
    #              display canvas with a waiting msg screen.
    #########################################################################
    def __init__(self):
        # init display obj
        self.display = Display()
        # init display with waiting msg
        # initialize the arduino listener
        self.mock = MockArdListener()
        self.running = False
        # self.ard_listener = ArduinoListener()

    #########################################################################
    # Name: run
    # Description: the main infinite loop where data is collected from the
    #              serial port and the display is updated with the inputs
    #              from the serial port. This is done in an asynchronous
    #              fashion to speed up the UI.
    #########################################################################
    def run(self):
        # real initialization
        """self.running = self.ard_listener.initialize_to_arduino() """
        # mocked initialization
        self.running = self.mock.mock_initialize_to_arduino()

        while self.running:
            # sets up button-press/mouse-click to quit program from pygame
            self.setup_pygame_events()
            state = None
            # make sure the com port has been successfully opened
            try:
                try:
                    # real read
                    """state = self.ard_listener.read_from_serial() """
                    # mocked read
                    state = self.mock.mock_read_from_serial()
                except TypeError:
                    print("typeError in ard_listener")

                # if the new state is different than the one currently in display, update display
                print("display.state, state: " + str(self.display.state) + ", " + str(state))

                if state is not None:
                    # update pygame display
                    self.display.update_display(state)

                # for safety, a base exception is the catch. To find out what the exception was, traceback is used
            except BaseException:
                from traceback import print_exc
                print_exc()
                return False
        return True

    ###################################################################
    # Name: setup_pygame_events
    # Description: sets up a few event handlers for pygame. Right now,
    #              the program crashes when buttons are clicked. This
    #              is suspected to stem from the inherent complexity
    #              using async methods
    ###################################################################
    def setup_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # press 'q', 'esc', or mouse-click to quit the program
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q or event.key == pygame.MOUSEBUTTONDOWN:
                    # gets laser safety runner .run to exit the loop
                    self.running = False
