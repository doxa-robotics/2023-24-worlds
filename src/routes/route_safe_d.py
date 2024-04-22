from _route import DefenseRoute


class SafeDRoute(DefenseRoute):
    """ A defensive route
    """
    @staticmethod
    def name():
        return "Safe (D)"

    @staticmethod
    def run(p, d):
        # p.inertial.set_heading(180 + 45)
        p.inertial.set_heading(360 - 45)
        p.wing_piston.open()
        p.claw_piston.close()

        d.turn_to(180 + 20)  # descore
        p.wing_piston.close()

        # prepare to score preload
        d.turn_to(180 + 65)
        p.claw_piston.open()
        d.drive(120)
        p.wait(500)
        for _ in range(8):
            d.drive(45)

        # back against the wall to reorient
        p.wait(500)
        d.turn_to(270)
        d.drive(45)
        d.drive(45)
        d.drive(-200)
        d.turn_to(0)
        d.drive(-100)

        # turn from the back and push the ball in
        d.turn_to(90)
        d.drive(-210)
        d.drive(-55)

        # go to the goal
        d.drive(100)
        p.wait(500)
        d.turn_to(180 + 45)
        d.drive(-800)
        d.turn_to(180)
        d.drive(-560)
        d.drive(-70)
