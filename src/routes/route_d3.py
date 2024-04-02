from _route import DefenseRoute


class D3Route(DefenseRoute):
    """ A defensive route
    """
    @staticmethod
    def name():
        return "Defense 3"

    @staticmethod
    def run(p, d):
        p.inertial.set_heading(45)
        p.wing_piston.open()
        p.claw_piston.close()
        d.turn_to(0)
        p.wing_piston.close()
        d.turn_to(240)
        d.drive(700)
        p.claw_piston.open()
        d.drive(-700)
        d.turn_to(20)
        d.drive(1000)
