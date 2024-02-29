from vex import *
from peripherals import RealBotPeripherals, TestBotPeripherals
from driver_control import driver_control
from autonomous_test import autonomous_test
from constants import COMPETITION_MODE, USE_REAL_BOT

if USE_REAL_BOT:
    peripherals = RealBotPeripherals()
else:
    peripherals = TestBotPeripherals()


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
