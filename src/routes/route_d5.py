from _route import DefenseRoute
from vex import wait


class D5Route(DefenseRoute):
    @staticmethod
    def name():
        return "Defense 5"


# Start on the far corner if the triangle, facing the wall/goal.


    @staticmethod
    def run(p, d):
        p.wing_piston.open()
        d.drive(800)
        d.turn(-45)
        p.wing_piston.close()
        d.turn(120)
        d.drive(1700)
        d.drive(-1100)
        d.turn(-120)
        p.wing_piston.open()
        d.drive(600)