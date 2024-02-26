from autonomous_common import turn_for, debug
from peripherals import Peripherals
from vex import *
from random import random


def autonomous_test(p: Peripherals):
    turn_for(p, 178)
    while True:
        turn_for(p, random()*360 - 180)
        wait(500)
