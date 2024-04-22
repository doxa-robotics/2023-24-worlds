from _route import DefenseRoute


class DisruptDRoute(DefenseRoute):
    @staticmethod
    def name():
        return "Disrupt (D)"

    @staticmethod
    def run(p, d):
        p.inertial.set_heading(90.0 + 8.2)

        p.wing_piston.open()
        p.wait(500)
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
        d.turn_to(125)
        d.drive(-1180)

        # do corner
        p.wing_piston.open()
        d.turn_to(180 + 25)
        d.drive(-450)
        d.turn_to(230)
        d.drive(-220)
        p.wing_piston.close()
        d.turn_to(270)
        d.drive(-40)
        d.turn_to(270)

        # go descore
        d.drive(230)
        d.drive(60)
        d.turn_to(45)
        p.wing_piston.open()
        d.drive(-360)

        # touch bar
        d.turn_to(10)
        d.drive(-880)
        p.wing_piston.close()
        d.turn_to(0)
        d.drive(-100)
