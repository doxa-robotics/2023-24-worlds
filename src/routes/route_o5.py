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

        d.drive(-70)
        d.turn_to(110)
        d.drive(-100)
        d.turn_to(110)
        p.wing_piston.close()
        d.drive(-700)
        d.turn_to(100)
        d.drive(-350)
        d.drive_until_photomicro_state(False, -40)

        p.claw_piston.open()  # open the claw
        d.turn_to(360 - 20)  # prepare to back out

        # back out of the goal and get the center and bar-center triballs
        d.drive(-970)
        d.turn_to(227)  # turn around and approach at an angle
        d.drive(180)
        d.drive(50)  # on purpose to slow down
        p.claw_piston.close()
        d.drive(50)
        d.turn_to(170)
        p.wing_piston.open()
        d.drive(-900)  # back into the goal

        # deposit the captured triball
        p.wing_piston.close()

        d.turn_to(360 - 27)
        p.claw_piston.open()
        d.drive(-500)
        d.turn_to(180 - 27)  # spin around to intake
        d.drive(440)
        d.drive(40)
        p.claw_piston.close()
        d.turn_to(360 - 20)
        d.drive(900)
        p.claw_piston.open()

        # back out of the goal and touch the bar
        # change of plans: just touch the bar by ramming the barrier
        d.drive(-1100)
        d.turn_to(270)
        d.drive(-500)
        p.wing_piston.open()
