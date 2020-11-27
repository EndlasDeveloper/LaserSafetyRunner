# imports
from arduino_listener import ArduinoListener
import app_vars as av
from constant_display import WAITING_FOR_INPUT_DEVICE_MSG
from serial_util import is_port_set, byte_arr_to_int
from display import Display


############################################################################
# Class: LaserSafetyRunner
# Description: manages the multi-threading capability of the app.
############################################################################
class LaserSafetyRunner:

    ########################################################################
    # Name: init_serial_to_arduino
    # Description: initializes the serial connection between the RPi and
    #              Arduino
    ########################################################################
    def init_serial_to_arduino(self):
        # keep searching for com port till one gives arduino response
        while True:
            # if successful connect, set flags and display
            if self.ard_listener.determine_platform_and_connect():
                print("inside init serial to arduino")
                av.is_com_port_open = True
                if av.has_port_connected_before is None:
                    av.has_port_connected_before = False
                else:
                    av.has_port_connected_before = True
                av.found_platform = True
                break
                # try:
                #     self.display.display_system_waiting(WAITING_FOR_INPUT_DEVICE_MSG, True)
                # except TypeError:
                #     print("TypeError: await self.display.display_system_waiting(WAITING_FOR_INPUT_DEVICE_MSG, True)")
                # print("\nis port set:" + str(is_port_set()))
                # print("Connected successfully to com port: " + av.com_port)
            else:
                print("no ard response...")

    #########################################################################
    # Name: constructor
    # Description: LaserSafetyRunner constructor that initializes Display obj
    #              and the ArduinoListener obj. It also initializes the
    #              display canvas with a waiting msg screen.
    #########################################################################
    def __init__(self):
        # init display obj
        # self.display = Display()
        # init display with waiting msg
        # self.display.update_pygame_image()
        # initialize the arduino listener
        self.ard_listener = ArduinoListener()

    #########################################################################
    # Name: run
    # Description: the main infinite loop where data is collected from the
    #              serial port and the display is updated with the inputs
    #              from the serial port. This is done in an asynchronous
    #              fashion to speed up the UI.
    #########################################################################
    async def run(self):

        # initialize pygame events synchronously
        # loop forever
        while True:
            # make sure the com port has been successfully opened
            if not av.ser.is_open:
            #    print(av.ser.is_open)
                self.init_serial_to_arduino()
            try:
                try:
                    self.ard_listener.read_from_serial()
                # sometimes throws this, if ignored, the system seems
                # to go on without problems
                except TypeError:
                    print("typeError in ard_listener")
                # init result arr
                result = []
                # if there is something return_val
                if len(av.return_val) > 0:
                    # get the most recent return_val
                    result = av.return_val
                # make sure not empty array
                    try:
                        print(result)
                        x = 1
                        # async call to update the display canvas with the new input
                        # await self.display.update_display(result)
                    # don't care, keep going
                    except TypeError:
                        print("typeError")
            # for safety, a base exception is the catch. To find out what the exception was, traceback is used
            except BaseException:
                from traceback import print_exc
                print_exc()
                return False


