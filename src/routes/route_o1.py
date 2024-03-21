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
        d.drive(-930)
        d.turn(-30)
        p.wing_piston.open()
        d.drive(-500)
        d.turn(-40)
        d.drive(-530)
        p.wing_piston.close()
        d.drive(200)
        d.turn(190)
        p.claw_piston.open()
        d.drive(460)
        d.drive(-530)
        p.claw_piston.close()
        d.turn(-75)
        p.claw_piston.open()
        d.drive(1200)
        p.claw_piston.close()
        d.turn(135)
        p.claw_piston.open()
        d.drive(950)
        d.drive(-400)
        d.turn(-150)
        d.drive(400)
        p.claw_piston.close()
        d.turn(150)
