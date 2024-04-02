from _route import OffenseRoute
from vex import wait


class TestRoute(OffenseRoute):
    @staticmethod
    def name():
        return ""


# Start facing goal, middle of the mat between the corner and the elevation bar

    @staticmethod
    def run(p, d):
        p.claw_piston.open()
        d.drive (400)
        d.turn(25)
        d.drive (500)
        p.claw_piston.close()
        d.drive (-100)
        p.wing_piston.open()
        d.turn(-200)
        d.drive(700)
        d.turn(120)
        d.drive(500)
       
