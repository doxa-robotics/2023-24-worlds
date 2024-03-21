from _route import OffenseRoute


class O1Route(OffenseRoute):
    """ An offensive auton route, based off of cachedVideo.mp4

    slightly modified
    """
    @staticmethod
    def name():
        return "Offense 1"

    @staticmethod
    def run(p, d):
        p.claw_piston.close()
        d.drive(-950)
        d.turn(-45)
        p.wing_piston.open()
        d.drive(-600)
        d.turn(-32)
        d.drive(-400)
        p.wing_piston.close()
        d.drive(150)
        d.turn(150)
        p.claw_piston.open()
        d.drive(150)
        d.drive(-200)
        p.claw_piston.close()
        d.turn(-50)
        d.drive(1200)
        d.turn(125)
        d.drive(900)
