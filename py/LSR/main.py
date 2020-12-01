###########################################################
# File: main.py
# Description: main entry point into the application script
###########################################################

import app_vars as av
from laser_safety_runner import LaserSafetyRunner


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    av.laser_safety_runner = LaserSafetyRunner()
    av.laser_safety_runner.run()




