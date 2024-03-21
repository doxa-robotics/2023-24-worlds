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
        d.drive(168)
        p.claw_piston.close()
        p.wing_piston.close()
        d.drive(-100)
        d.turn(90)
        p.claw_piston.open()
        d.turn(170)
        d.drive(60)
        d.turn(48)
        d.drive(80)
        p.claw_piston.close()
        d.drive(-110)
        d.turn(50)
        p.wing_piston.open()
        d.drive(50)
        d.turn(45)
        d.drive(66)
        p.wing_piston.close()
        d.drive(66)
        d.turn(180)
        d.drive(10)
        d.drive(-10)

        while d.turn(90):
            p.claw_piston.open()

        d.drive(168)

        p.claw_piston.close()
        d.turn(100)
        d.drive(100)
        d.turn(38)
        d.drive(100)

        d.turn(148)
        while d.drive(100):
            p.wing_piston.open()
            p.claw_piston.open()
