from _route import OffenseRoute


class O4Route(OffenseRoute):
    """ An offensive route
    """
    @staticmethod
    def name():
        return "Offense 4"

    @staticmethod
    def run(p, d):
        p.inertial.set_heading(135)
        p.claw_piston.close()
        p.wing_piston.close()
        d.turn_to(270)
        p.claw_piston.open()
        d.drive(1160)
        p.claw_piston.close()

        # Going back
        d.turn_to(180)
        d.drive(1160)
        d.turn_to(40)
        d.drive(700)
        d.turn_to(49)

        # Going to goal 1st
        d.drive(580)
        p.claw_piston.open()
        d.turn_to(270)
        d.drive(1600)
        p.wing_piston.open()
        d.drive(1600)
        d.turn_to(90)
        d.drive(660)
        d.turn_to(90)

        # Going to final goal
        d.drive(920)
        p.claw_piston.close()
        p.wing_piston.close()
