from _route import DefenseRoute


class D1Route(DefenseRoute):
    """ An defensive auton route, descoring triball for AWP
    """
    @staticmethod
    def name():
        return "Defense 1"

    @staticmethod
    def run(p, d):
        p.inertial.set_heading(45)
        p.claw_piston.close()
        p.wing_piston.open()
        d.drive(-250)
        d.turn_to(90)
        d.drive(-200)
        p.wing_piston.close()
        d.turn_to(125)
        d.drive(-780)
        p.wing_piston.open()
        d.drive(-360)
        d.turn_to(185)
        d.drive(-460)
        p.wing_piston.close()
        p.claw_piston.open()
        d.drive(980)
        d.drive(-280)
        p.claw_piston.close()
        d.turn_to(270)
        d.drive(-1280)
        d.turn_to(180)
        d.drive(-750)
