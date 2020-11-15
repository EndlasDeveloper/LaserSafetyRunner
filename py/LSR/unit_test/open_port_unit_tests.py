#########################################
# Unit tests for opening the serial port
#########################################

# imports
import unittest
import arduino_listener as asm
import app_vars as av


# test class for open port tests
class OpenPortTests(unittest.TestCase):
    def test_is_port_set_all_true(self):
        av.has_port_connected_before = True
        av.is_com_port_open = True
        av.found_platform = True
        result = asm.is_port_set()
        self.assertEqual(True, result)

    def test_is_port_set_all_false(self):
        av.has_port_connected_before = False
        av.is_com_port_open = False
        av.found_platform = False
        result = asm.is_port_set()
        self.assertEqual(False, result)

    def test_is_port_set_found_platform_no_port_connect(self):
        av.has_port_connected_before = False
        av.is_com_port_open = False
        av.found_platform = True
        result = asm.is_port_set()
        self.assertEqual(False, result)


# entry point into test main
if __name__ == '__main__':
    unittest.main()
