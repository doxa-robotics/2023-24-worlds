from simple_pid import PID
from utils import debug, time_seconds
from peripherals import PIDDrivetrainConfig, Peripherals
from vex import *


class PIDDrivetrain:
    p: Peripherals
    config: PIDDrivetrainConfig

    def __init__(self, p: Peripherals) -> None:
        self.p = p
        self.config = p.pid_drivetrain_config

    def turn(self, delta: int | float) -> float:
        """Turns the bot a specific amount of degrees (Relative)

        `delta` is in degrees.
        """
        def get_heading():
            if self.config.gyro_reversed:
                return 360 - self.p.inertial.heading()
            else:
                return self.p.inertial.heading()

        old_heading = get_heading()
        self.p.inertial.set_heading(180)
        starting_real_heading = get_heading()
        heading_difference = starting_real_heading + float(delta)
        heading = starting_real_heading - heading_difference
        pid = PID(self.config.turning_p, 0, 0,
                  setpoint=0, time_fn=lambda: time_seconds(self.p))
        real_velocity = self.config.max_stop_velocity
        while abs(heading) >= self.config.turning_max_error or real_velocity >= self.config.max_stop_velocity:
            velocity_mps = pid(heading)
            if velocity_mps == None:
                raise Exception("PID failed: couldn't get new velocity")
            velocity_rpm = (velocity_mps * 60.0) / \
                (self.p.WHEEL_TRAVEL_MM / 1000)
            self.p.left_motors.spin(FORWARD, velocity_rpm, units=RPM)
            self.p.right_motors.spin(REVERSE, velocity_rpm, units=RPM)
            real_velocity = (self.p.left_motors.velocity() *
                             60) / (self.p.WHEEL_TRAVEL_MM / 1000)
            real_heading = get_heading()
            heading = real_heading - heading_difference
            margin = 80
            if real_heading > 360 - margin:
                self.p.inertial.set_heading(margin)
                heading_difference -= 360 - margin
            elif real_heading < margin:
                self.p.inertial.set_heading(360 - margin)
                heading_difference += 360 - margin
        self.p.left_motors.stop(BRAKE)
        self.p.right_motors.stop(BRAKE)
        self.p.inertial.set_heading(
            old_heading + delta + heading - heading_difference)
        return abs(heading)

    def drive(self, distance: int | float) -> float:
        self.p.left_motors.reset_position()
        self.p.right_motors.reset_position()
        value = ((self.p.left_motors.position() +
                 self.p.right_motors.position()) / 2) / 360 * self.p.WHEEL_TRAVEL_MM
        target_value = value + distance
        pid = PID(self.config.drive_p, 0, 0, setpoint=target_value,
                  time_fn=lambda: time_seconds(self.p))
        delta = target_value - value
        real_velocity = self.config.max_stop_velocity
        while abs(delta) >= self.config.drive_max_error or real_velocity >= self.config.max_stop_velocity:
            value = ((self.p.left_motors.position() +
                     self.p.right_motors.position()) / 2) / 360 * self.p.WHEEL_TRAVEL_MM
            delta = target_value - value
            velocity_mps = pid(value)
            if velocity_mps == None:
                raise Exception("PID failed: couldn't get new velocity")
            velocity_rpm = (velocity_mps * 60.0) / \
                (self.p.WHEEL_TRAVEL_MM / 1000)
            self.p.left_motors.spin(FORWARD, velocity_rpm, units=RPM)
            self.p.right_motors.spin(FORWARD, velocity_rpm, units=RPM)
            real_velocity = (((self.p.left_motors.velocity(
            ) + self.p.right_motors.velocity()) / 2) * 60) / (self.p.WHEEL_TRAVEL_MM / 1000)
        self.p.left_motors.stop(BRAKE)
        self.p.right_motors.stop(BRAKE)
        return abs(delta)
