import unittest
from display import *

d = Display()


class DisplayGetDisplayImagePath(unittest.TestCase):
    def test_get_display_image_path_byte_zero(self):
        d.state = 1
        result_img_path = d.get_display_image_path()
        self.assertEqual(LASER_FIRE_IMG, result_img_path)

        d.state = 2
        result_img_path = d.get_display_image_path()
        self.assertEqual(LASER_FIRE_IMG, result_img_path)

        d.state = 4
        result_img_path = d.get_display_image_path()
        self.assertEqual(LASER_FIRE_IMG, result_img_path)

        d.state = 8
        result_img_path = d.get_display_image_path()
        self.assertEqual(LASER_FIRE_IMG, result_img_path)

    def test_get_display_image_path_byte_one(self):
        d.state = 16
        result_img_path = d.get_display_image_path()
        self.assertEqual(ESTOP_IMG, result_img_path)

        d.state = 32
        result_img_path = d.get_display_image_path()
        self.assertEqual(SAFETY_CIRCUIT_IMG, result_img_path)

        d.state = 64
        result_img_path = d.get_display_image_path()
        self.assertEqual(DEFEAT_SAFETY_IMG, result_img_path)

        d.state = 128
        result_img_path = d.get_display_image_path()
        self.assertEqual(WARNING_IMG, result_img_path)

    def test_get_display_image_path_byte_two(self):
        d.state = 256
        result_img_path = d.get_display_image_path()
        self.assertEqual(FAULT_IMG, result_img_path)

        d.state = 512
        result_img_path = d.get_display_image_path()
        self.assertEqual(SLEEP_IMG, result_img_path)

        d.state = 1024
        result_img_path = d.get_display_image_path()
        self.assertEqual(FIBER_ERROR_IMG, result_img_path)