import unittest
from main import *


class OpenPortTests(unittest.TestCase):
    def test_display_image(self):
        display_image(IMAGE_DIR + IMAGE_TO_SHOW)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
