from vex import *
from peripherals import Peripherals
from sys import stderr


def time_seconds(p: Peripherals):
    return p.brain.timer.system() / 1000


def debug(content: str):
    print(content, file=stderr)
