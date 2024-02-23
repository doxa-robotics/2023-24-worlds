from vex import *
from peripherals import Peripherals


def driver_control(p: Peripherals):
    last_a_pressing = False
    last_b_pressing = False
    while True:
        # Spin the left and right groups based on the controller
        axis3 = p.controller.axis3.position()
        if axis3 < 3 or axis3 > -3:
            axis3 = 0

        axis1 = p.controller.axis1.position()
        if axis1 < 3 or axis1 > -3:
            axis1 = 0

        p.left_motors.spin(
            DirectionType.FORWARD,
            axis3 + axis1,
            VelocityUnits.PERCENT)
        p.right_motors.spin(
            DirectionType.FORWARD,
            axis3 - axis1,
            VelocityUnits.PERCENT)

        a_pressing = p.controller.buttonA.pressing()
        if a_pressing and not last_a_pressing:
            if p.wing_piston.value():
                p.wing_piston.close()
            else:
                p.wing_piston.open()
        last_a_pressing = a_pressing

        b_pressing = p.controller.buttonB.pressing()
        if b_pressing and not last_b_pressing:
            if p.claw_piston.value():
                p.claw_piston.close()
            else:
                p.claw_piston.open()
        last_b_pressing = b_pressing

        wait(20)
