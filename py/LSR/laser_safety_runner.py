# imports
from arduino_listener import ArduinoListener
import app_vars as av
from mocks_and_stubs import *
from constant_display import WAITING_FOR_INPUT_DEVICE_MSG
from serial_util import is_port_set, byte_arr_to_int
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
        # self.ard_listener = ArduinoListener()

    ########################################################################
    # Name: initialize_to_arduino
    # Description: initializes the serial connection between the RPi and
    #              Arduino
    ########################################################################
    def initialize_to_arduino(self):
        # keep searching for com port till one gives arduino response

        # if successful connect, set flags and display
        if self.ard_listener.determine_platform_and_connect():
            # print("inside init serial to arduino")
            av.is_com_port_open = True
            if av.has_port_connected_before is None:
                av.has_port_connected_before = False
            else:
                av.has_port_connected_before = True
            av.found_platform = True
            return
        else:
            print("no ard response...")

    #########################################################################
    # Name: run
    # Description: the main infinite loop where data is collected from the
    #              serial port and the display is updated with the inputs
    #              from the serial port. This is done in an asynchronous
    #              fashion to speed up the UI.
    #########################################################################
    def run(self):
        """ self.initialize_to_arduino() """
        self.mock.mock_initialize_to_arduino()
        while av.running:
            self.setup_pygame_events()
            # make sure the com port has been successfully opened
            try:
                try:
                    """ self.ard_listener.read_from_serial() """
                    self.mock.mock_read_from_serial()
                except TypeError:
                    print("typeError in ard_listener")
                if av.return_val >= 0:
                    print("return val " + str(av.return_val))
                if self.display.state != av.return_val:
                    self.display.update_display(av.return_val)
                # for safety, a base exception is the catch. To find out what the exception was, traceback is used
            except BaseException:
                from traceback import print_exc
                print_exc()
                return False
        return True

    @staticmethod
    def setup_pygame_events():
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # click a 'q' or the 'esc' key to quit the program
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    av.running = False
