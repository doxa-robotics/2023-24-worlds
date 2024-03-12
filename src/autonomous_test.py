from autonomous_common import debug
from peripherals import Peripherals
from vex import *
from random import random

from pid_drivetrain import PIDDrivetrain


def autonomous_test(p: Peripherals):
    while True:
        p.drivetrain.drive(1500)
        p.drivetrain.turn(180)
