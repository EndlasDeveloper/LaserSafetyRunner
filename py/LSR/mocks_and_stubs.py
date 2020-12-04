from time import *
import app_vars as av

# preset sleep time between state changes
SLEEP_TIME = 1.0


##########################################################
# Class: MockArdListener
# Description: holds method stubs for mocking the arduino
#              listener portion of the application. This
#              allows for easier testing of the display
#########################################################
class MockArdListener:

    def __init__(self):
        self.cur_num = 1

    ################################################################################
    # Name: mock_read_from_serial
    # Description: mocks the behavior or the arduino listener's read method
    ################################################################################
    def mock_read_from_serial(self):
        if self.cur_num >= 65536:
            self.cur_num = 1
        else:
            self.cur_num <<= 1
        sleep(SLEEP_TIME)
        return self.cur_num

    ################################################################################
    # Name: mock_initialize_to_arduino
    # Description: mocks the successful connection of the Pi to the Arduino
    ################################################################################
    @staticmethod
    def mock_initialize_to_arduino():
        # just set all port open flags
        av.found_platform = True
        av.is_com_port_open = True
        av.has_port_connected_before = True
        return True
