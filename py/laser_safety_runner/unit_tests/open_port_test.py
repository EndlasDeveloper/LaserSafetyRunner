#########################################
# Unit tests for opening the serial port
#########################################

# imports
import unittest
from image_manip import *


# test class for open port tests
class OpenPortTests(unittest.TestCase):
    def test_display_image(self):
        display_image(IMAGE_DIR + IMAGE_TO_SHOW)
        self.assertEqual(True, True)


# entry point into test main
if __name__ == '__main__':
    unittest.main()
