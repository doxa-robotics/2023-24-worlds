from _route import OffenseRoute


class O3Route(OffenseRoute):
    """ An offensive route, rushing
    """
    @staticmethod
    def name():
        return "Offense 3"

    @staticmethod
    def run(p, d):
        p.inertial.set_heading(135)
        d.drive(1600)
        # rush
        p.claw_piston.close()
        d.turn_to(180)
        p.wing_piston.open()
        # back into goal
        d.drive(-800)
        p.wing_piston.close()
        d.drive(400)
        # spin to de-intake
        d.turn_to(0)
        d.drive(400)
        p.claw_piston.open()
        # back out of goal
        d.drive(-400)
        # not getting 3rd triball due to time
        d.turn_to(90)
        d.drive(1600)
        d.turn_to(0)
        d.drive(-600)
