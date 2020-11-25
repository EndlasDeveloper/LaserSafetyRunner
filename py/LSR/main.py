import app_vars as av
from laser_safety_runner import LaserSafetyRunner
from asyncio import run

av.laser_safety_runner = LaserSafetyRunner()
av.laser_safety_runner.init_serial_to_arduino()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #######################################################################
    # Name: main
    # Description: asynchronous main function to start the application.
    #######################################################################
    async def main():
        # initialize the runner with global reference
        # run the runner
        await av.laser_safety_runner.run()
    # asyncio run
    run(main())



