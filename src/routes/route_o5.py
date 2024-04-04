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
        d.turn_to(100)
        p.wing_piston.close()
        d.drive(-1000)  # back into the goal
        p.wing_piston.close()
        p.claw_piston.open()  # open the claw
        d.turn_to(360 - 20)  # prepare to back out

        # back out of the goal and get the center and bar-center triballs
        d.drive(-900)
        d.turn_to(223)  # turn around and approach at an angle
        d.drive(270)
        d.drive(50)  # on purpose to slow down
        p.claw_piston.close()
        d.turn_to(170)
        p.wing_piston.open()
        d.drive(-800)  # back into the goal

        # deposit the captured triball
        p.wing_piston.close()
        d.turn_to(0)
        p.claw_piston.open()
        d.drive(100)

        d.turn_to(180 - 24)  # spin around to intake
        d.drive(960)
        d.drive(30)
        p.claw_piston.close()
        # p.wait(400)
        d.turn_to(360 - 24)
        d.drive(900)
        p.claw_piston.open()

        # back out of the goal and touch the bar
        # change of plans: just touch the bar by ramming the barrier
        d.drive(-1100)
        d.turn_to(270)
        d.drive(-500)
        p.wing_piston.open()
