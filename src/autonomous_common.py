from simple_pid import PID
from vex import *
from peripherals import Peripherals
from sys import stderr

PID_ACCEPTABLE_ERROR = 2.0
PID_ACCEPTABLE_ERROR_VELOCITY = 1.0


def time_seconds(p: Peripherals):
    return p.brain.timer.system() / 1000


def turn_for(p: Peripherals, angle_delta):
    debug("> start turn for %s" % angle_delta)
    starting_real_heading = p.inertial.heading()
    heading_difference = starting_real_heading - 180
    target = (((starting_real_heading + angle_delta) %
              360) - heading_difference) % 360
    heading = starting_real_heading - heading_difference
    pid = PID(1.5, 0, 0, setpoint=target, time_fn=lambda: time_seconds(p))
    real_velocity = PID_ACCEPTABLE_ERROR_VELOCITY
    while abs(heading - target) >= 2 or real_velocity >= 1.0:
        velocity = pid(heading)
        if velocity == None:
            raise Exception("PID failed: couldn't get new velocity")
        p.left_motors.spin(FORWARD, velocity)
        p.right_motors.spin(REVERSE, velocity)
        real_velocity = p.left_motors.velocity()
        heading = (p.inertial.heading() - heading_difference) % 360
    p.left_motors.stop(BRAKE)
    p.right_motors.stop(BRAKE)


def debug(content: str):
    print(content, file=stderr)
