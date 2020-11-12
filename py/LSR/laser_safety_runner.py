# imports
from threading import Thread
from multiprocessing import Process
from arduino_serial_manager import ArduinoSerialManager
import app_vars as av
import asyncio
from constant_serial import *
from serial_util import is_port_set
from constant_display import BASE_UI_REFRESH_RATE
from time import perf_counter
from display import Display


############################################################################
# Class: LaserSafetyRunner
# Description: manages the multi-threading capability of the app.
############################################################################
class LaserSafetyRunner:

    def init_serial_to_arduino(self):
        # get mutex so other threads wait their turn
        if self.ard_listener.determine_platform_and_connect():
            print("Connected successfully to com port: " + av.com_port)
        # always release mutex before returning

    def __init__(self):
        self.display = Display()
        self.ard_listener = ArduinoSerialManager()

        # initialize the ui and arduino threads
        # initialize the base time reference
        self.t0 = perf_counter()
        # init arduino listener and UI objects

        self.init_serial_to_arduino()

    async def run(self):
        t0 = perf_counter()
        while True:
            serial_event = asyncio.Event()
            buffer_read_event = asyncio.Event()
            display_event = asyncio.Event()
            # Spawn a Task to wait until 'serial_event' is set.
            serial_event_waiter = asyncio.create_task(self.ard_listener.start_reading_from_serial(serial_event))
            buffer_read_event_waiter = asyncio.create_task(self.display.copy_data_buffer(buffer_read_event))
            display_event_waiter = asyncio.create_task(self.display.update_display(display_event))
            # Sleep for 1 second and set the serial_event.
            serial_event.set()
            await serial_event_waiter
            display_event.set()
            # Wait until the waiter task is finished.
            await buffer_read_event_waiter
            if perf_counter() - t0 > 2:
                print("update disp")
                t0 = perf_counter()
                await display_event_waiter



