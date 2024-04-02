from _route import OffenseRoute


class O5Route(OffenseRoute):
    """ An offensive route, going under the goal
    """
    @staticmethod
    def name():
        return "Offense 5"

    @staticmethod
    def run(p, d):
        # 0 degrees is the claw facing straight north
        # initialize the drivetrain with a southeast heading
        p.inertial.set_heading(135)

        # close the claw for preload and open the wings
        p.claw_piston.close()
        p.wing_piston.open()

        # drive backwards to descore match load zone
        d.drive(-400)
        d.turn_to(90)
        d.drive(-800)  # back into the goal
        p.claw_piston.open()  # open the claw
        d.turn_to(0)  # prepare to back out

        # back out of the goal and get the center and bar-center triballs
        d.drive(-1200)
        d.turn_to(190)  # turn around and approach at an angle
        d.drive(500)
        p.claw_piston.close()
        d.drive(-800)  # back into the goal

        return

        # deposit the captured triball
        d.turn_to(360 - 15)
        p.claw_piston.open()
        d.drive(-600)
        d.turn_to(180 - 15)  # spin around to intake
        d.drive(500)
        p.claw_piston.close()
        d.turn_to(360 - 15)
        d.drive(1000)
        p.claw_piston.open()
        d.drive(-200)
