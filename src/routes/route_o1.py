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
        d.drive(-850)
        d.turn(-45)
        d.drive(-500)
        d.turn(-77)
        d.drive(-400)
        d.drive(100)
        d.turn(180)
        d.drive(100)
        d.drive(-40)
        d.turn(-50)
        d.drive(1200)
        d.turn(125)
        d.drive(900)
