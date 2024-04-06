from _route import OffenseRoute


class O4Route(OffenseRoute):
    """ An offensive route, getting the corner, bar, preload, and right-center triballs """

    @staticmethod
    def name():
        return "Offense 4"

    @staticmethod
    def run(p, d):
        # initialize the drivetrain with a downward heading
        p.inertial.set_heading(180)

        # start
        p.claw_piston.close()

        # Going back
        d.drive(-600)
        d.turn_to(160)
        p.wing_piston.open()
        d.drive(-700)
        d.turn_to(0)  # descore, overturning to fling away from the edge
        d.turn_to(270)  # turn back to back into the goal
        p.wing_piston.close()

        # Backing into the goal the first time
        d.drive(-580)
        d.drive(200)
        d.turn_to(-90)
        d.drive(200)
        p.claw_piston.open()

        # get the rightmost center triball
        d.drive(-200)
        d.turn_to(180)
        d.drive(800)
        d.turn_to(210)
        d.drive(200)
        d.drive(50)
        p.claw_piston.close()

        # go back to the goal
        d.turn_to(-35)
        d.drive(900)
        p.claw_piston.open()
        d.drive(-200)
        d.turn_to(-90)
        d.drive(-1000)
        d.turn_to(0)
        d.drive(-900)
        d.drive(-50)
