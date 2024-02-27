from simple_pid import PID
from vex import *
from peripherals import Peripherals
from sys import stderr
from constants import WHEEL_TRAVEL_MM, WHEEL_TRACK_WIDTH_MM

PID_ACCEPTABLE_ERROR = 2.0  # degrees
PID_ACCEPTABLE_ERROR_VELOCITY = 0.01  # m/s
PID_P_CONSTANT = 0.00304
PID_I_CONSTANT = 0.0
PID_D_CONSTANT = 0.0
PID_TIMEOUT = 10
PID_VELOCITY_UNTIMEOUT = 1.0


def time_seconds(p: Peripherals):
    return p.brain.timer.system() / 1000


def _turn_for(p: Peripherals, angle_delta: int | float) -> float | None:
    starting_real_heading = p.inertial.heading()
    heading_difference = starting_real_heading + angle_delta
    heading = starting_real_heading - heading_difference
    pid = PID(PID_P_CONSTANT * (WHEEL_TRACK_WIDTH_MM / 100), PID_I_CONSTANT, PID_D_CONSTANT,
              setpoint=0, time_fn=lambda: time_seconds(p))
    real_velocity = PID_ACCEPTABLE_ERROR_VELOCITY
    while abs(heading) >= 2 or real_velocity >= 1.0:
        velocity_mps = pid(heading)
        if velocity_mps == None:
            raise Exception("PID failed: couldn't get new velocity")
        velocity_rpm = (velocity_mps * 60.0) / (WHEEL_TRAVEL_MM / 1000)
        p.left_motors.spin(FORWARD, velocity_rpm, units=RPM)
        p.right_motors.spin(REVERSE, velocity_rpm, units=RPM)
        real_velocity = p.left_motors.velocity()
        real_heading = p.inertial.heading()
        heading = real_heading - heading_difference
        if real_heading > 340:
            p.inertial.set_heading(20)
            heading_difference -= 340 - 20
        elif real_heading < 20:
            p.inertial.set_heading(340)
            heading_difference += 340 - 20
    p.left_motors.stop(BRAKE)
    p.right_motors.stop(BRAKE)
    return abs(heading)


def turn_for(p: Peripherals, angle_delta: int | float):
    debug("> start turn for %s" % angle_delta)
    debug("        heading is %s deg" % p.inertial.heading())
    start = time_seconds(p)
    result = _turn_for(p, angle_delta)
    debug("  done, accurate to %s deg" % result)
    debug("        took %s secs" % (time_seconds(p) - start))


def debug(content: str):
    print(content, file=stderr)
