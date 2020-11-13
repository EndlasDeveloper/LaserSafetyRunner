import app_vars as g
from laser_safety_runner import LaserSafetyRunner
from asyncio import run
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # initialize the runner with global reference
    g.laser_safety_runner = LaserSafetyRunner()
    # run the runner
    g.laser_safety_runner.run()




