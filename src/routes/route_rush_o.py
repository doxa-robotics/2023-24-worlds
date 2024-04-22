from _route import OffenseRoute


class RushORoute(OffenseRoute):
    """ An offensive route, rushing
    """
    @staticmethod
    def name():
        return "Rush (O)"

    @staticmethod
    def run(p, d):
        p.inertial.set_heading(270.0 - 8.2)
        p.wing_piston.open()
        d.drive(1090)
        p.wing_piston.close()

        # intake the middle ball
        d.drive(50)
        p.claw_piston.close()
        d.turn_to(0)
        p.claw_piston.open()
        d.drive(620)  # drop the middle ball off in the goal

        # intake the middle top ball
        d.turn_to(189)
        d.drive(890)
        d.drive(50)
        p.claw_piston.close()
        d.drive(50)

        # back into the goal
        d.turn_to(10)
        d.drive(800)
        p.claw_piston.open()

        # out of the goal and back to start
        d.drive(-400)
        d.turn_to(90)
        d.drive(1200)

        # drive towards the corner
        d.turn_to(180)
        p.wing_piston.open()
        d.drive(-160)

        # descore corner and score preload
        d.turn_to(160)
        p.wing_piston.open()
        d.drive(-260)
        d.turn_to(110)
        d.drive(-100)
        d.turn_to(110)
        d.drive(-700)
        p.wing_piston.close()
        d.turn_to(100)
        d.drive(-400)  # the triball slips out here
