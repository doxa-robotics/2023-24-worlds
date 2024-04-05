from _route import DefenseRoute


class D2Route(DefenseRoute):
    """ An defensive auton route, descoring triball for AWP
    """
    @staticmethod
    def name():
        return "Defense 2"

    @staticmethod
    def run(p, d):
        # set_heading sets the reference heading.
        # turn_to turns to an ABSOLUTE angle. it does NOT just turn the robot
        # it turns to an angle

        p.inertial.set_heading(45)  # TODO: change this to be pointing up
        p.claw_piston.close()
        d.turn_to(90)
        p.wing_piston.open()
        p.claw_piston.open()
        # Going toward corner triball
        d.drive(900)
        d.turn_to(180)
        d.drive(1140)
        p.wing_piston.close()
        d.drive(1350)
        d.turn_to(45)
        p.wing_piston.open()
        d.drive(800)
        d.turn_to(40)
        p.wing_piston.close()
        p.claw_piston.close()
        # Going Back to goal
        d.turn_to(140)
        d.drive(800)
        d.turn_to(-42)
        d.drive(1140)
