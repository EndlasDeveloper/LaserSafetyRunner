#########################################
# Unit tests for opening the serial port
#########################################

# imports
import unittest
from vars_consts import serial_flags_and_vars as sfv
import main


# test class for open port tests
class OpenPortTests(unittest.TestCase):
    def test_is_port_set_all_true(self):
        sfv.HAS_PORT_CONNECTED = True
        sfv.is_com_port_open = True
        sfv.FOUND_PLATFORM = True
        result = main.is_port_set()
        self.assertEqual(True, result)

    def test_is_port_set_all_false(self):
        sfv.HAS_PORT_CONNECTED = False
        sfv.is_com_port_open = False
        sfv.FOUND_PLATFORM = False
        result = main.is_port_set()
        self.assertEqual(False, result)

    def test_is_port_set_found_platform_no_port_connect(self):
        sfv.HAS_PORT_CONNECTED = False
        sfv.is_com_port_open = False
        sfv.FOUND_PLATFORM = True
        result = main.is_port_set()
        self.assertEqual(False, result)


# entry point into test main
if __name__ == '__main__':
    unittest.main()
