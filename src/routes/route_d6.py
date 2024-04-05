from _route import DefenseRoute


class D6Route(DefenseRoute):
    """ An defensive auton route, descoring triball for AWP
    """
    @staticmethod
    def name():
        return "Defense 6"

    @staticmethod
    def run(p, d):
        p.inertial.set_heading(360 - 45)

        p.claw_piston.close()
        p.wing_piston.open()

        d.turn(-360)
        d.turn_to(-60)
        p.wing_piston.close()

        # Going toward triball
        d.drive(950)
        d.drive(50)
        p.claw_piston.close()

        # Go to the middle bar
        d.turn_to(-90)
        p.claw_piston.open()
        p.wing_piston.open()
        d.drive(250)

        # Go back to first place
        d.turn_to(-45)

        return
        d.drive(1980)

        # Going to the goal
        d.turn_to(-90)
        d.drive(1100)

        # Go back to the goal backward
        d.drive(-100)
        d.turn(180)
        p.wing_piston.open()
        d.drive(100)

        # Go to the bar
        d.drive(700)
        d.turn(-50)
        d.drive(600)
        d.turn_to(0)
        p.wing_piston.open()
        d.drive(1100)
