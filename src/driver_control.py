from vex import *
from peripherals import Peripherals
from ultrasonic_claw import UltrasonicClaw
from autonomous_common import debug


def driver_control(p: Peripherals):
    last_a_pressing = False
    last_b_pressing = False
    last_y_pressing = False
    ultrasonic_claw = UltrasonicClaw(p.claw_piston, p.front_sonar)
    while True:
        # Spin the left and right groups based on the controller
        axis3 = p.controller.axis3.position()
        if axis3 < 3 and axis3 > -3:
            axis3 = 0

        axis1 = p.controller.axis1.position()
        if axis1 < 3 and axis1 > -3:
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

        ultrasonic_claw.update()
        b_pressing = p.controller.buttonB.pressing()
        if b_pressing and not last_b_pressing:
            if p.claw_piston.value():
                ultrasonic_claw.close()
            else:
                ultrasonic_claw.open()
        last_b_pressing = b_pressing

        wait(20)
