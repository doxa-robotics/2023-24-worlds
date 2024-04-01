from _route import OffenseRoute


class O3Route(OffenseRoute):
    """ An offensive route
    """
    @staticmethod
    def name():
        return "Offense 3"

    @staticmethod
    def run(p, d):
        p.inertial.set_heading(135)
        d.drive(1600)
        p.claw_piston.close()
        d.turn_to(180)
        p.wing_piston.open()
        d.drive(-800)
        p.wing_piston.close()
        d.drive(400)
        d.turn_to(0)
        d.drive(400)
        p.claw_piston.open()
        d.drive(-400)
        d.turn_to(90)
        d.drive(1600)
        d.turn_to(0)
        d.drive(-600)
