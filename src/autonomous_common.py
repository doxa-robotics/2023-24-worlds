from simple_pid import PID
from vex import *
from peripherals import Peripherals
from sys import stderr
from constants import WHEEL_TRAVEL_MM, WHEEL_TRACK_WIDTH_MM

PID_ACCEPTABLE_ERROR = 2.0  # degrees
PID_ACCEPTABLE_ERROR_VELOCITY = 0.01  # m/s


def time_seconds(p: Peripherals):
    return p.brain.timer.system() / 1000


def turn_for(p: Peripherals, angle_delta):
    debug("> start turn for %s" % angle_delta)
    starting_real_heading = p.inertial.heading()
    heading_difference = starting_real_heading - 180
    target = (((starting_real_heading + angle_delta) %
              360) - heading_difference) % 360
    heading = starting_real_heading - heading_difference
    pid = PID(0.0035 * (WHEEL_TRACK_WIDTH_MM / 100), 0, 0,
              setpoint=target, time_fn=lambda: time_seconds(p))
    real_velocity = PID_ACCEPTABLE_ERROR_VELOCITY
    debug("diff=%s" % heading_difference)
    while abs(heading - target) % 360 >= 2 or real_velocity >= 1.0:
        velocity_mps = pid(heading)
        if velocity_mps == None:
            raise Exception("PID failed: couldn't get new velocity")
        velocity_rpm = (velocity_mps * 60.0) / (WHEEL_TRAVEL_MM / 1000)
        p.left_motors.spin(FORWARD, velocity_rpm, units=RPM)
        p.right_motors.spin(REVERSE, velocity_rpm, units=RPM)
        real_velocity = p.left_motors.velocity()
        heading = (p.inertial.heading() - heading_difference) % 360
    p.left_motors.stop(BRAKE)
    p.right_motors.stop(BRAKE)


def debug(content: str):
    print(content, file=stderr)
