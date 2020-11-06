###################################################################################################
# byte_manip_test.py - python test file for implementing unit tests for methods from byte_manip.py
###################################################################################################

# imports
import unittest
from byte_manip import *
import img_path.img_paths as p


class ByteManipTestsByteArrToInt(unittest.TestCase):
    def test_byte_arr_to_int_with_zero_byte_set(self):
        byte_arr = [1, 0, 0, 0, 240]
        result = byte_arr_to_int(byte_arr)
        self.assertEqual(1, result)

    def test_byte_arr_to_int_with_one_byte_set(self):
        byte_arr = [0, 1, 0, 0, 240]
        result = byte_arr_to_int(byte_arr)
        self.assertEqual(16, result)

    def test_byte_arr_to_int_with_two_byte_set(self):
        byte_arr = [0, 0, 1, 0, 240]
        result = byte_arr_to_int(byte_arr)
        self.assertEqual(256, result)

    def test_byte_arr_to_int_with_three_byte_set(self):
        byte_arr = [0, 0, 0, 1, 240]
        result = byte_arr_to_int(byte_arr)
        self.assertEqual(4096, result)


class ByteManipTestsIsInputValid(unittest.TestCase):
    def test_is_input_valid_with_valid_input_byte0(self):
        byte_arr = [1, 0, 0, 0, 240]
        is_valid = is_input_valid(byte_arr)
        self.assertTrue(is_valid)

    def test_is_input_valid_with_valid_input_byte1(self):
        byte_arr = [0, 1, 0, 0, 240]
        is_valid = is_input_valid(byte_arr)
        self.assertTrue(is_valid)

    def test_is_input_valid_with_valid_input_byte2(self):
        byte_arr = [0, 0, 1, 0, 240]
        is_valid = is_input_valid(byte_arr)
        self.assertTrue(is_valid)

    def test_is_input_valid_with_valid_input_byte3(self):
        byte_arr = [0, 0, 0, 1, 240]
        is_valid = is_input_valid(byte_arr)
        self.assertTrue(is_valid)

    def test_is_input_valid_with_valid_input_all_data_bits_set(self):
        byte_arr = [15, 15, 15, 15, 240]
        is_valid = is_input_valid(byte_arr)
        self.assertTrue(is_valid)

    def test_is_input_valid_with_invalid_input_byte0_header_byte_max(self):
        byte_arr = [240, 0, 0, 0, 240]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte0_header_byte_min(self):
        byte_arr = [16, 0, 0, 0, 240]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte1_header_byte_max(self):
        byte_arr = [0, 240, 0, 0, 240]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte1_header_byte_min(self):
        byte_arr = [0, 16, 0, 0, 240]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte2_header_byte_max(self):
        byte_arr = [0, 0, 240, 0, 240]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte2_header_byte_min(self):
        byte_arr = [0, 0, 16, 0, 240]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte3_header_byte_max(self):
        byte_arr = [0, 0, 0, 240, 240]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte3_header_byte_min(self):
        byte_arr = [0, 0, 0, 16, 240]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte4_header_byte_min(self):
        byte_arr = [0, 0, 0, 1, 0]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)

    def test_is_input_valid_with_invalid_input_byte4_header_byte_max(self):
        byte_arr = [0, 0, 0, 1, 15]
        is_valid = is_input_valid(byte_arr)
        self.assertFalse(is_valid)


class ByteManipTestsGetDisplayImagePath(unittest.TestCase):
    def test_get_display_image_path_byte_zero(self):
        result_img_path = get_display_image_path(1)
        self.assertEqual(p.LASER_FIRE_IMG, result_img_path)

        result_img_path = get_display_image_path(2)
        self.assertEqual(p.LASER_FIRE_IMG, result_img_path)

        result_img_path = get_display_image_path(4)
        self.assertEqual(p.LASER_FIRE_IMG, result_img_path)

        result_img_path = get_display_image_path(8)
        self.assertEqual(p.LASER_FIRE_IMG, result_img_path)

    def test_get_display_image_path_byte_one(self):
        result_img_path = get_display_image_path(16)
        self.assertEqual(p.ESTOP_IMG, result_img_path)

        result_img_path = get_display_image_path(32)
        self.assertEqual(p.SAFETY_CIRCUIT_IMG, result_img_path)

        result_img_path = get_display_image_path(64)
        self.assertEqual(p.DEFEAT_SAFETY_IMG, result_img_path)

        result_img_path = get_display_image_path(128)
        self.assertEqual(p.WARNING_IMG, result_img_path)

    def test_get_display_image_path_byte_two(self):
        result_img_path = get_display_image_path(256)
        self.assertEqual(p.FAULT_IMG, result_img_path)

        result_img_path = get_display_image_path(512)
        self.assertEqual(p.SLEEP_IMG, result_img_path)

        result_img_path = get_display_image_path(1024)
        self.assertEqual(p.FIBER_ERROR_IMG, result_img_path)


# int main()
if __name__ == '__main__':
    unittest.main()
