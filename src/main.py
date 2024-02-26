from vex import *
from peripherals import Peripherals
from driver_control import driver_control
from autonomous_test import autonomous_test
from constants import COMPETITION_MODE

peripherals = Peripherals()


def autonomous():
    autonomous_test(peripherals)


def driver():
    while True:
        try:
            driver_control(peripherals)
        except:
            pass


if COMPETITION_MODE:
    Competition(driver, autonomous)
else:
    autonomous()
