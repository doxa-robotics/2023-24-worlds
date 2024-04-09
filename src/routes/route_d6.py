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

        d.drive(740)
        d.turn_to(270)
        d.drive(530)
        d.drive(50)
        p.claw_piston.close()
        d.drive(-100)
        d.turn_to(180)
        p.wing_piston.open()
        d.drive(-280)
        d.turn_to(270)
        p.wing_piston.close()
        d.turn_to(0)
        d.drive(-300)
        p.claw_piston.open()
        d.drive(1150)
        d.drive(-1000)
