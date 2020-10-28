####################################################################
# main.py - implements the main entry point into the program
####################################################################

# imports
import byte_manip as b_manip
import serial
import constants as c
import pygame
from pygame.locals import *

# default image path
DEFAULT_IMG = c.NO_LOAD_IMG

# flag so we don't try and open a port twice
is_com_port_open = False

# int main()
if __name__ == '__main__':
    ser = ""
    img = DEFAULT_IMG
    pygame.init()

    display_width = 640
    display_height = 480
    game_display = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
    pygame.display.set_caption('LASER SAFETY RUNNER')
    clock = pygame.time.Clock()
    py_img = pygame.image.load(img)
    py_img_last = py_img

    # void loop()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            else:
                continue
        # try and open the serial port if we haven't done so already
        if is_com_port_open is False:
            try:
                ser = serial.Serial(port=c.COM_PORT, baudrate=c.BAUD_RATE, bytesize=c.BYTE_SIZE, timeout=c.SERIAL_TIMEOUT)
                ser.write(b'\x80')
                ser.flushInput()
                reply = ser.read()
                ser.flushInput()
                response = int.from_bytes(reply, c.ENDIAN, signed=False)
                # print(reply) should be 255
                if response == 255:
                    is_com_port_open = True
            except serial.SerialException:
                print("Unable to open COM port: " + c.COM_PORT)
                pygame.quit()
                exit()
        elif is_com_port_open is True:
            index = 0
            ser.flushInput()
            byte_arr = ser.read(5)
            ser.flushInput()
            if b_manip.is_input_valid(byte_arr):
                img = b_manip.get_display_image_path(b_manip.byte_arr_to_int(byte_arr))
                for b in byte_arr:
                    print("byte{0}: {1}".format(str(index), (int(b))))
                    index += 1
                print("\n")
            else:
                print("invalid input\n")
        py_img = pygame.image.load(img)
        if py_img != py_img_last:
            game_display.fill((0, 0, 0))
            game_display.blit(py_img, (0, 0))
            pygame.display.update()





