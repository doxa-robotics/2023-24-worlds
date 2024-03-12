from simple_pid import PID
from autonomous_common import time_seconds
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

        `delta` is in degrees. This method may override the inertial's heading
        to an unexpected value.
        """
        starting_real_heading = self.p.inertial.heading()
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
            real_heading = self.p.inertial.heading()
            heading = real_heading - heading_difference
            if real_heading > 340:
                self.p.inertial.set_heading(20)
                heading_difference -= 340 - 20
            elif real_heading < 20:
                self.p.inertial.set_heading(340)
                heading_difference += 340 - 20
        self.p.left_motors.stop(BRAKE)
        self.p.right_motors.stop(BRAKE)
        return abs(heading)

    def drive(self, distance: int | float) -> float:
        value = (self.p.left_motors.position() +
                 self.p.right_motors.position()) / 2
        target_value = value + distance
        pid = PID(self.config.drive_p, 0, 0, setpoint=target_value,
                  time_fn=lambda: time_seconds(self.p))
        delta = target_value - value
        real_velocity = self.config.max_stop_velocity
        while abs(delta) >= self.config.drive_max_error or real_velocity >= self.config.max_stop_velocity:
            value = (self.p.left_motors.position() +
                     self.p.right_motors.position()) / 2
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
