###################################################################################################
# byte_manip_test.py - python test file for implementing unit tests for methods from byte_manip.py
###################################################################################################

# imports
import unittest
from byte_manip import *


class ByteManipTestsFirstByte(unittest.TestCase):
    def test_byte_arr_to_int_with_first_byte_set(self):
        byte_arr = [1, 0, 0, 0, 240]
        result = byte_arr_to_int(byte_arr)
        self.assertEqual(1, result)


class ByteManipTestsSecondByte(unittest.TestCase):
    def test_byte_arr_to_int_with_second_byte_set(self):
        byte_arr = [0, 1, 0, 0, 240]
        result = byte_arr_to_int(byte_arr)
        self.assertEqual(16, result)


class ByteManipTestsThirdByte(unittest.TestCase):
    def test_byte_arr_to_int_with_third_byte_set(self):
        byte_arr = [0, 0, 1, 0, 240]
        result = byte_arr_to_int(byte_arr)
        self.assertEqual(256, result)


class ByteManipTestsFourthByte(unittest.TestCase):
    def test_byte_arr_to_int_with_fourth_byte_set(self):
        byte_arr = [0, 0, 0, 1, 240]
        result = byte_arr_to_int(byte_arr)
        self.assertEqual(4096, result)


# int main()
if __name__ == '__main__':
    unittest.main()
