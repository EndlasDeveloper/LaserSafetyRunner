import RPi.GPIO as GPIO
 
# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
# set up the GPIO channels IN or OUT
GPIO.setup(12, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)

GPIO.setup(32, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
 
# input from pin
#input_value = GPIO.input(pin)
 
# output to pin
#GPIO.output(12, GPIO.LOW)
