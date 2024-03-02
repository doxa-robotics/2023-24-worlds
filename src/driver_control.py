from vex import *

from autonomous_common import debug
from constants import TURNING_SPEED_FACTOR
from peripherals import Peripherals
from ultrasonic_claw import UltrasonicClaw


def _damp_controller(val):
    value = math.pow(0.1*val, 2)
    if val < 0:
        return -value
    else:
        return value


def driver_control(p: Peripherals):
    last_a_pressing = False
    last_b_pressing = False
    ultrasonic_claw = UltrasonicClaw(p.claw_piston, p.front_sonar)
    while True:
        # Spin the left and right groups based on the controller
        axis3 = p.controller.axis3.position()
        if -5 < axis3 < 5:
            axis3 = 0
        axis3 = _damp_controller(axis3)

        axis1 = p.controller.axis1.position()
        if -5 < axis1 < 5:
            axis1 = 0
        axis1 = _damp_controller(axis1)

        p.left_motors.spin(
            DirectionType.FORWARD,
            axis3 + axis1*TURNING_SPEED_FACTOR,
            VelocityUnits.PERCENT)
        p.right_motors.spin(
            DirectionType.FORWARD,
            axis3 - axis1*TURNING_SPEED_FACTOR,
            VelocityUnits.PERCENT)

        a_pressing = p.controller.buttonA.pressing()
        if a_pressing and not last_a_pressing:
            if p.wing_piston.value():
                p.wing_piston.close()
            else:
                p.wing_piston.open()
        last_a_pressing = a_pressing

        ultrasonic_claw.update()
        b_pressing = p.controller.buttonB.pressing()
        if b_pressing and not last_b_pressing:
            if p.claw_piston.value():
                ultrasonic_claw.close()
            else:
                ultrasonic_claw.open()
        last_b_pressing = b_pressing

        wait(20)
