import globals as g
from laser_safety_runner import LaserSafetyRunner

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # initialize the runner
    g.laser_safety_runner = LaserSafetyRunner()
    # run the runner
    if not g.laser_safety_runner.run():
        print("LaserSafetyRunner: run() failed!")
        exit()



