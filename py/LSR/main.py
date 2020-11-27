import app_vars as av
from laser_safety_runner import LaserSafetyRunner
from asyncio import run


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    av.laser_safety_runner = LaserSafetyRunner()
    av.laser_safety_runner.run()




