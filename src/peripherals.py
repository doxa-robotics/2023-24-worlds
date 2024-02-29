from vex import *
from constants import WHEEL_TRAVEL_MM, WHEEL_TRACK_WIDTH_MM


class Peripherals:
    brain: Brain
    inertial: Inertial
    drivetrain: SmartDrive
    left_motors: MotorGroup
    right_motors: MotorGroup
    controller: Controller
    claw_piston: Pneumatics
    wing_piston: Pneumatics
    front_sonar: Sonar


class RealBotPeripherals(Peripherals):
    def __init__(self) -> None:
        self.brain = Brain()
        self.controller = Controller()

        self.wing_piston = Pneumatics(self.brain.three_wire_port.f)
        self.claw_piston = Pneumatics(self.brain.three_wire_port.a)

        self.front_sonar = Sonar(self.brain.three_wire_port.c)

        self.inertial = Inertial(Ports.PORT5)

        self.left_motors = MotorGroup(
            Motor(Ports.PORT18, False),
            Motor(Ports.PORT10, True),

            Motor(Ports.PORT19, True),
            Motor(Ports.PORT9, False),
        )
        self.right_motors = MotorGroup(
            Motor(Ports.PORT11, True),
            Motor(Ports.PORT1, False),

            Motor(Ports.PORT17, False),
            Motor(Ports.PORT2, True),
        )
        self.drivetrain = SmartDrive(
            self.left_motors,
            self.right_motors,
            self.inertial,
            WHEEL_TRAVEL_MM,
            WHEEL_TRACK_WIDTH_MM
        )


class TestBotPeripherals(Peripherals):
    def __init__(self) -> None:
        self.brain = Brain()
        self.controller = Controller()

        self.wing_piston = Pneumatics(self.brain.three_wire_port.f)
        self.claw_piston = Pneumatics(self.brain.three_wire_port.a)

        self.front_sonar = Sonar(self.brain.three_wire_port.c)

        fleft = Motor(Ports.PORT20)
        fright = Motor(Ports.PORT11, True)
        bleft = Motor(Ports.PORT19)
        bright = Motor(Ports.PORT1, True)
        self.inertial = Inertial(Ports.PORT5)

        self.left_motors = MotorGroup(fleft, bleft)
        self.right_motors = MotorGroup(fright, bright)
        self.drivetrain = SmartDrive(
            self.left_motors,
            self.right_motors,
            self.inertial,
            WHEEL_TRAVEL_MM,
            WHEEL_TRACK_WIDTH_MM
        )
