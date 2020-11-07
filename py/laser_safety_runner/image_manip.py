###########################################################################
# image_manip.py - utility methods for image display and manipulation
###########################################################################

# imports
from PIL import Image


############################################################################################
# Name: display_image
# Description: method takes a string with the relative path to an image to open
#              and uses Image library functions to open the image file and show it
############################################################################################
def display_image(image_path_str):
    image = Image.open(image_path_str)
    image.show()
