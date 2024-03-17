from simple_pid import PID
from vex import *

from peripherals import Peripherals, PIDDrivetrainConfig
from utils import time_seconds


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
        old_heading = self.p.inertial.heading()
        self.p.inertial.set_heading(180)
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
        self.p.inertial.set_heading(
            old_heading + delta + heading - heading_difference)
        return abs(heading)

    def turn_v2(self, target_heading_delta: int | float) -> float:
        """Turns the bot a specific amount of degrees (relative), version 2

        `delta` is in degrees. May change the value of the inertial's heading.
        """
        real_heading = self.p.inertial.heading()
        target_heading = real_heading + float(target_heading_delta)
        heading = real_heading
        heading_difference = 0

        pid = PID(self.config.turning_p, 0, 0,
                  setpoint=target_heading, time_fn=lambda: time_seconds(self.p))
        real_velocity = self.config.max_stop_velocity
        while (abs(heading - target_heading) >= self.config.turning_max_error or
               abs(real_velocity) >= self.config.max_stop_velocity):
            # calculate using PID the new set velocity
            set_velocity = pid(heading)
            if set_velocity == None:
                raise Exception("PID failed: couldn't get new velocity")
            self.p.left_motors.spin(FORWARD, set_velocity, units=RPM)
            self.p.right_motors.spin(REVERSE, set_velocity, units=RPM)

            # get the average current velocity between the left and right motor
            # groups
            real_velocity = (self.p.left_motors.velocity(
                units=RPM) - self.p.right_motors.velocity(units=RPM))/2

            # add or subtract from the heading to make sure it's within 60-300
            # and never overflows from 359 => 0 and vice versa
            real_heading = self.p.inertial.heading()
            heading = real_heading + heading_difference
            if real_heading > 300:
                self.p.inertial.set_heading(real_heading - 200)
                heading_difference += 200
            elif real_heading < 60:
                self.p.inertial.set_heading(real_heading + 200)
                heading_difference -= 200

        self.p.left_motors.stop(BRAKE)
        self.p.right_motors.stop(BRAKE)
        self.p.inertial.set_heading(
            (self.p.inertial.heading() + heading_difference) % 360)
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

    def drive_v2(self, target_distance_delta: int | float) -> float:
        """ Drives the bot a specified distance, version 2

        `distance` is in mm. resets the motor encoders.

        Returns the final error (measured by the encoders) in mm.
        """
        def revolutions_to_mm(revolutions: int | float):
            return revolutions * self.p.WHEEL_TRAVEL_MM

        self.p.left_motors.reset_position()
        self.p.right_motors.reset_position()

        # set the current distance traveled to be 0, since we just reset the
        # motor groups' encoders.
        distance = 0

        pid = PID(self.config.drive_p, 0, 0,
                  setpoint=target_distance_delta, time_fn=lambda: time_seconds(self.p))
        real_velocity = self.config.max_stop_velocity
        while (abs(distance - target_distance_delta) >= self.config.drive_max_error or
               abs(real_velocity) >= self.config.max_stop_velocity):
            # calculate using PID the new set velocity
            set_velocity = pid(distance)
            if set_velocity == None:
                raise Exception("PID failed: couldn't get new velocity")
            self.p.left_motors.spin(FORWARD, set_velocity, units=RPM)
            self.p.right_motors.spin(FORWARD, set_velocity, units=RPM)

            # get the average current velocity between the left and right motor
            # groups
            real_velocity = (self.p.left_motors.velocity(
                units=RPM) + self.p.right_motors.velocity(units=RPM))/2

            # get the new distance traveled
            distance = revolutions_to_mm((self.p.left_motors.position(
                units=TURNS) + self.p.right_motors.position(units=TURNS))/2)

        # stop all motors
        self.p.left_motors.stop(BRAKE)
        self.p.right_motors.stop(BRAKE)

        # return the final error in mm
        return abs(distance - target_distance_delta)
