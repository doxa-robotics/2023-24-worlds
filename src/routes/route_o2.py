from _route import OffenseRoute


class O2Route(OffenseRoute):
    """ An offensive auton route, based off of cachedVideo.mp4

    slightly modified
    """
    @staticmethod
    def name():
        return "Offense 2"

    @staticmethod
    def run(p, d):
        p.claw_piston.open()
        p.wing_piston.open()
        d.drive(400)
        p.wing_piston.close()
        d.drive(700)
        d.turn(-30)
        d.drive(840)

        p.claw_piston.close()
        p.wing_piston.close()
        d.drive(-1000)
        d.turn(90)
        p.claw_piston.open()
        d.turn(170)
        d.drive(600)
        d.turn(48)
        d.drive(800)
        p.claw_piston.close()
        d.drive(-1100)
        d.turn(50)
        p.wing_piston.open()
        d.drive(500)
        d.turn(45)
        d.drive(660)
        p.wing_piston.close()
        d.drive(660)
        d.turn(180)
        d.drive(100)
        d.drive(-100)

        d.turn(90)
        p.claw_piston.open()

        d.drive(1680)

        p.claw_piston.close()
        d.turn(1000)
        d.drive(1000)
        d.turn(38)
        d.drive(1000)

        d.turn(148)
        p.wing_piston.open()
        p.claw_piston.open()
        d.drive(1000)
