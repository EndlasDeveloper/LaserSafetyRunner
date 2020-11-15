###################################################################################################
# serial_util_unit_tests.py - python test file for implementing unit tests for methods from byte_manip.py
###################################################################################################

# imports
import unittest
from serial_util import *


############################################################################
# Name: get_byte_from_int
# Description: helper method to simplify getting bytes with specific values
############################################################################
def get_byte_from_int(i):
    return int.to_bytes(i, length=8, byteorder='big', signed=False)


class SerialUtilTestsByteToInt(unittest.TestCase):
    def test_byte_to_int_b_zero(self):
        b = get_byte_from_int(0)
        result = byte_to_int(b)
        self.assertEqual(0, result)

    def test_byte_to_int_b_in_between(self):
        b = get_byte_from_int(99)
        result = byte_to_int(b)
        self.assertEqual(99, result)

    def test_byte_to_int_b_max(self):
        b = get_byte_from_int(127)
        result = byte_to_int(b)
        self.assertEqual(127, result)


class SerialUtilTestsByteArrToInt(unittest.TestCase):
    def test_byte_arr_to_int_with_zero_byte_set(self):
        byte_arr = [0, get_byte_from_int(1), 0, 0, 0, 128]
        result = byte_arr_to_int(byte_arr)
        self.assertEqual(1, result)

    def test_byte_arr_to_int_with_one_byte_set(self):
        byte_arr = [0, 0, get_byte_from_int(1), 0, 0, get_byte_from_int(128)]
        result = byte_arr_to_int(byte_arr)
        self.assertEqual(16, result)

    def test_byte_arr_to_int_with_two_byte_set(self):
        byte_arr = [0, 0, 0, get_byte_from_int(1), 0, get_byte_from_int(128)]
        result = byte_arr_to_int(byte_arr)
        self.assertEqual(256, result)

    def test_byte_arr_to_int_with_three_byte_set(self):
        byte_arr = [0, 0, 0, 0, get_byte_from_int(1), get_byte_from_int(128)]
        result = byte_arr_to_int(byte_arr)
        self.assertEqual(4096, result)


class SerialUtilTestsIsInputValid(unittest.TestCase):
    def test_is_input_valid_with_valid_input_byte0(self):
        byte_arr = [0, get_byte_from_int(1), 0, 0, 0, get_byte_from_int(128)]
        is_valid = is_input_valid(byte_arr)
        self.assertTrue(is_valid)

    def test_is_input_valid_with_valid_input_byte1(self):
        byte_arr = [0, 0, get_byte_from_int(1), 0, 0, get_byte_from_int(128)]
        is_valid = is_input_valid(byte_arr)
        self.assertTrue(is_valid)

    def test_is_input_valid_with_valid_input_byte2(self):
        byte_arr = [0, 0, 0, get_byte_from_int(1), 0, get_byte_from_int(128)]
        is_valid = is_input_valid(byte_arr)
        self.assertTrue(is_valid)

    def test_is_input_valid_with_valid_input_byte3(self):
        byte_arr = [0, 0, 0, 0, get_byte_from_int(1), get_byte_from_int(128)]
        is_valid = is_input_valid(byte_arr)
        self.assertTrue(is_valid)

    def test_is_input_valid_with_valid_input_all_data_bits_set(self):
        val = get_byte_from_int(15)
        byte_arr = [b'', val, val, val, val, get_byte_from_int(128)]
        is_valid = is_input_valid(byte_arr)
        self.assertTrue(is_valid)

    def test_is_input_valid_with_invalid_input_byte0_header_byte_max(self):
        byte_arr = [0, get_byte_from_int(128), 0, 0, 0, get_byte_from_int(128)]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte0_header_byte_min(self):
        byte_arr = [0, get_byte_from_int(16), 0, 0, 0, get_byte_from_int(128)]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte1_header_byte_max(self):
        byte_arr = [0, 0, get_byte_from_int(128), 0, 0, get_byte_from_int(128)]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte1_header_byte_min(self):
        byte_arr = [0, 0, get_byte_from_int(16), 0, 0, get_byte_from_int(128)]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte2_header_byte_max(self):
        byte_arr = [0, 0, 0, get_byte_from_int(128), 0, get_byte_from_int(128)]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte2_header_byte_min(self):
        byte_arr = [0, 0, 0, get_byte_from_int(16), 0, get_byte_from_int(128)]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte3_header_byte_max(self):
        byte_arr = [0, 0, 0, 0, get_byte_from_int(128), get_byte_from_int(128)]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte3_header_byte_min(self):
        byte_arr = [0, 0, 0, 0, get_byte_from_int(16), get_byte_from_int(128)]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte4_header_byte_min(self):
        byte_arr = [0, 0, 0, 0, get_byte_from_int(1), 0]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte4_header_byte_max(self):
        byte_arr = [0, 0, 0, 0, get_byte_from_int(1), get_byte_from_int(15)]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)


# int main()
if __name__ == '__main__':
    unittest.main()
