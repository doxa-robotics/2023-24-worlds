from _route import DefenseRoute


class D5Route(DefenseRoute):
    @staticmethod
    def name():
        return "Defense 5"

    @staticmethod
    def run(p, d):
        p.inertial.set_heading(90.0 + 8.2)

        p.wing_piston.open()
        d.drive(1090)

        # intake the middle ball
        d.drive(50)
        p.claw_piston.close()
        d.drive(-100)

        # disrupt the middle
        d.turn_to(0)
        p.wing_piston.open()
        d.drive(-500)
        p.wing_piston.close()

        # get remaining three triballs
        d.turn_to(120)
        d.drive(-1200)

        # do corner
        p.wing_piston.open()
        d.turn_to(180 + 45)
        d.drive(-600)
        p.wing_piston.open()
        d.turn_to(270)
        p.wing_piston.close()
        d.drive(-100)
        d.drive(-50)
        d.turn_to(270)

        # go descore
        d.drive(300)
        d.turn_to(45)
        p.wing_piston.open()
        d.drive(-200)
        d.turn_to(0)
        d.drive(-1000)
        d.drive(-100)
        p.wing_piston.close()
