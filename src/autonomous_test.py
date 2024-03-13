from autonomous_common import debug
from peripherals import Peripherals
from vex import *

from pid_drivetrain import PIDDrivetrain


def autonomous_test(p: Peripherals, d: PIDDrivetrain):
    while True:
        d.drive(1000)
        d.turn(180)
