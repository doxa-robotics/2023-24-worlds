from _route import OffenseRoute


class O4Route(OffenseRoute):
    """ An offensive route
    """
    @staticmethod
    def name():
        return "Offense 4"

    @staticmethod
    def run(p, d):
        # initialize the drivetrain with a downward heading
        p.inertial.set_heading(180)

        # start
        p.claw_piston.close()

        # Going back
        # TODO: can the bot turn around?
        d.turn_to(0)  # point back up
        d.drive(1160)
        d.turn_to(320)
        d.drive(700)
        p.wing_piston.open()
        d.turn_to(270)

        # Going to goal 1st
        d.drive(580)
        p.claw_piston.open()
        d.turn_to(180)
        d.drive(1600)
        p.wing_piston.open()
        d.drive(1600)
        d.turn_to(270)
        d.drive(660)
        d.turn_to(270)

        # Going to final goal
        d.drive(920)
        p.claw_piston.open()

        # back out and touch bar
        d.drive(-200)
        d.turn_to(90)
        d.drive(1200)
        d.turn_to(180)
        d.drive(-800)
