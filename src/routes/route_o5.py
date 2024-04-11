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

        d.drive(-80)
        d.turn_to(110)
        d.drive(-100)
        d.turn_to(110)
        d.drive(-700)
        p.wing_piston.close()
        d.turn_to(100)
        d.drive(-350)  # the triball slips out here
        p.claw_piston.open()
        d.drive_until_photomicro_state(False, -40)

        d.turn_to(180 - 17)  # prepare to back out

        # forwards out of the goal and get the center and bar-center triballs
        d.drive(1180)
        d.drive(50)  # on purpose to slow down
        p.claw_piston.close()
        d.drive(50)
        d.turn_to(360 - 30)
        p.claw_piston.open()
        d.drive(250)
        d.turn_to(220)
        d.drive(340)
        d.drive(50)
        p.claw_piston.close()

        # back into the goal
        d.turn_to(180)
        p.wing_piston.open()
        d.drive(-900)

        # deposit the captured triball
        p.wing_piston.close()
        d.turn_to(0)
        p.claw_piston.open()
        d.drive(-250)

        # touch the bar
        d.drive(-800)
        d.turn_to(270)
        d.drive(-1100)
