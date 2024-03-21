from simple_pid import PID
from utils import Logger, time_seconds
from vex import *
from peripherals import Peripherals, PIDDrivetrainConfig

DRIFT_CORRECTION_FACTOR = 4.2


class PIDDrivetrain:
    p: Peripherals
    config: PIDDrivetrainConfig

    def __init__(self, p: Peripherals) -> None:
        self.p = p
        self.config = p.pid_drivetrain_config

    @Logger.logger_context("PIDDrivetrain.turn")
    def turn(self, target_heading_delta: int | float) -> float:
        """Turns the bot a specific amount of degrees (relative), version 2

        `delta` is in degrees. May change the value of the inertial's heading.
        """
        start_time = time_seconds(self.p)
        Logger.debug("turning {}deg".format(target_heading_delta))

        def get_heading():
            if self.config.gyro_reversed:
                return 360 - self.p.inertial.heading()
            else:
                return self.p.inertial.heading()

        real_heading = get_heading()
        target_heading = real_heading + float(target_heading_delta)
        heading = real_heading
        heading_difference = 0

        pid = PID(self.config.turning_p, 0, 0,
                  setpoint=target_heading, time_fn=lambda: time_seconds(self.p))
        real_velocity = self.config.max_stop_velocity
        last_moving_time = time_seconds(self.p)
        while (abs(heading - target_heading) >= self.config.turning_max_error or
               abs(real_velocity) >= self.config.max_stop_velocity):
            # calculate using PID the new set velocity
            set_velocity = pid(heading)
            if set_velocity == None:
                raise Exception("PID failed: couldn't get new velocity")
            if abs(real_velocity) >= self.config.timeout_velocity:
                last_moving_time = time_seconds(self.p)
            if time_seconds(self.p) - last_moving_time > self.config.timeout:
                Logger.debug("PID timeout")
                break
            self.p.left_motors.spin(FORWARD, set_velocity, units=RPM)
            self.p.right_motors.spin(REVERSE, set_velocity, units=RPM)

            # get the average current velocity between the left and right motor
            # groups
            real_velocity = (self.p.left_motors.velocity(
                units=RPM) - self.p.right_motors.velocity(units=RPM))/2

            # add or subtract from the heading to make sure it's within 60-300
            # and never overflows from 359 => 0 and vice versa
            real_heading = get_heading()
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
        Logger.debug("took {}secs".format(time_seconds(self.p) - start_time))
        return abs(heading)

    @Logger.logger_context("PIDDrivetrain.drive")
    def drive(self, target_distance_delta: int | float, drift_correction: bool = False) -> float:
        error = 0
        start_time = time_seconds(self.p)
        Logger.debug("driving {}mm".format(target_distance_delta))
        if drift_correction:
            error = self.drive_pid_no_drift(target_distance_delta)
        else:
            error = self.drive_pid(target_distance_delta)
        # if abs(target_distance_delta) > 500:
        #     error = self.drive_pid(target_distance_delta)
        # else:
        #     self.p.left_motors.reset_position()
        #     self.p.right_motors.reset_position()
        #     distance_rev = target_distance_delta / self.p.WHEEL_TRAVEL_MM
        #     self.p.left_motors.spin_for(
        #         FORWARD, distance_rev, units=TURNS, wait=False, velocity=5, units_v=PERCENT)
        #     self.p.right_motors.spin_for(
        #         FORWARD, distance_rev, units=TURNS, wait=False, velocity=5, units_v=PERCENT)
        #     while self.p.left_motors.is_spinning() or self.p.right_motors.is_spinning():
        #         pass
        Logger.debug("took {}secs".format(time_seconds(self.p) - start_time))
        return error

    def drive_pid(self, target_distance_delta: int | float) -> float:
        """ Drives the bot a specified distance, version 2

        `distance` is in mm. resets the motor encoders.

        Returns the final error (measured by the encoders) in mm.
        """
        def revolutions_to_mm(revolutions: int | float):
            return revolutions * self.p.WHEEL_TRAVEL_MM
        minmax = max if target_distance_delta > 0 else min

        self.p.left_motors.reset_position()
        self.p.right_motors.reset_position()

        # set the current distance traveled to be 0, since we just reset the
        # motor groups' encoders.
        distance = 0

        pid = PID(self.config.drive_p, 0, 0,
                  setpoint=target_distance_delta, time_fn=lambda: time_seconds(self.p))
        real_velocity = self.config.max_stop_velocity
        last_moving_time = time_seconds(self.p)
        while (abs(distance - target_distance_delta) >= self.config.drive_max_error or
               abs(real_velocity) >= self.config.max_stop_velocity):
            # calculate using PID the new set velocity
            set_velocity = pid(distance)
            if set_velocity == None:
                raise Exception("PID failed: couldn't get new velocity")
            if abs(real_velocity) >= self.config.timeout_velocity:
                last_moving_time = time_seconds(self.p)
            if time_seconds(self.p) - last_moving_time > self.config.timeout:
                Logger.debug("PID timeout")
                break
            self.p.left_motors.spin(FORWARD, set_velocity, units=RPM)
            self.p.right_motors.spin(FORWARD, set_velocity, units=RPM)

            # get the average current velocity between the left and right motor
            # groups
            real_velocity = (self.p.left_motors.velocity(
                units=RPM) + self.p.right_motors.velocity(units=RPM))/2

            # get the new distance traveled
            distance = revolutions_to_mm(minmax(self.p.left_motors.position(
                units=TURNS), self.p.right_motors.position(units=TURNS)))

        # stop all motors
        self.p.left_motors.stop(BRAKE)
        self.p.right_motors.stop(BRAKE)

        # return the final error in mm
        return abs(distance - target_distance_delta)

    def drive_pid_no_drift(self, target_distance_delta: int | float) -> float:
        """ Drives the bot a specified distance without drifting

        `distance` is in mm. resets the motor encoders.

        Returns the final error (measured by the encoders) in mm.
        """
        def revolutions_to_mm(revolutions: int | float):
            return revolutions * self.p.WHEEL_TRAVEL_MM
        minmax = min if target_distance_delta > 0 else max

        self.p.left_motors.reset_position()
        self.p.right_motors.reset_position()

        # set the current distance traveled to be 0, since we just reset the
        # motor groups' encoders.
        distance = 0

        pid = PID(self.config.drive_p, 0, 0,
                  setpoint=target_distance_delta, time_fn=lambda: time_seconds(self.p))
        real_velocity = self.config.max_stop_velocity
        last_moving_time = time_seconds(self.p)

        while (abs(distance - target_distance_delta) >= self.config.drive_max_error or
               abs(real_velocity) >= self.config.max_stop_velocity):
            # calculate using PID the new set velocity
            set_velocity = pid(distance)
            if set_velocity == None:
                raise Exception("PID failed: couldn't get new velocity")
            if abs(real_velocity) >= self.config.timeout_velocity:
                last_moving_time = time_seconds(self.p)
            if time_seconds(self.p) - last_moving_time > self.config.timeout:
                Logger.debug("PID timeout")
                break

            # get the new distance traveled
            left_distance = revolutions_to_mm(self.p.left_motors.position(
                units=TURNS))
            right_distance = revolutions_to_mm(
                self.p.right_motors.position(units=TURNS))
            distance = minmax(left_distance, right_distance)

            if left_distance < right_distance:
                self.p.left_motors.spin(
                    FORWARD, set_velocity + (right_distance - left_distance) * DRIFT_CORRECTION_FACTOR, units=RPM)
                self.p.right_motors.spin(
                    FORWARD, set_velocity, units=RPM)
            elif right_distance < left_distance:
                self.p.left_motors.spin(
                    FORWARD, set_velocity, units=RPM)
                self.p.right_motors.spin(
                    FORWARD, set_velocity + (left_distance - right_distance) * DRIFT_CORRECTION_FACTOR, units=RPM)
            else:
                self.p.left_motors.spin(
                    FORWARD, set_velocity, units=RPM)
                self.p.right_motors.spin(
                    FORWARD, set_velocity, units=RPM)

            # get the average current velocity between the left and right motor
            # groups
            real_velocity = (self.p.left_motors.velocity(
                units=RPM) + self.p.right_motors.velocity(units=RPM))/2

        # stop all motors
        self.p.left_motors.stop(BRAKE)
        self.p.right_motors.stop(BRAKE)

        # return the final error in mm
        return abs(distance - target_distance_delta)
