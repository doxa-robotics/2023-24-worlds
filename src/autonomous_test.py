from autonomous_common import turn_for
from peripherals import Peripherals
from vex import *


def autonomous_test(p: Peripherals):
    for _ in range(5 * 2):
        turn_for(p, 180)
