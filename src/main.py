from vex import *

from constants import (AUTONOMOUS_ROUTE, COMPETITION_MODE, FULL_SPEED_PID,
                       USE_REAL_BOT)
from driver_control import driver_control
from peripherals import Peripherals, RealBotPeripherals, TestBotPeripherals
from pid_drivetrain import PIDDrivetrain
from routes import routes
from ui import UiHandler, ui_show_error
from utils import Logger, has_interaction

wait(200)  # let gyro and stuff warm up

# default to AUTONOMOUS_ROUTE but allow selection
selected_autonomous: str = AUTONOMOUS_ROUTE

peripherals: Peripherals
if USE_REAL_BOT:
    peripherals = RealBotPeripherals(FULL_SPEED_PID)
else:
    peripherals = TestBotPeripherals()
Logger.set_peripherals(peripherals)
drivetrain = PIDDrivetrain(peripherals)
ui_handler = UiHandler(peripherals.brain, peripherals,
                       "DOXA Robotics 99484", "99484",
                       routes)


@Logger.logger_context("autonomous")
def autonomous():
    # this function is called as a thread so we have to make sure
    ui_handler.cancel_resolve_route()
    # wait a negligible amount so the main thread can realize it should stop
    wait(150)
    while peripherals.inertial.is_calibrating():
        pass
    ui_handler.route_ui(selected_autonomous)
    route = None
    for possible_route in routes:
        if possible_route.name() == selected_autonomous:
            route = possible_route
    if route is None:
        raise Exception("undefined route! {}".format(route))
    ui_handler.start_timer()
    route.run(peripherals, drivetrain)
    Logger.dump_to_sdcard()
    ui_handler.show_timer()


@Logger.logger_context("opcontrol")
def driver():
    while not has_interaction(peripherals):
        pass
    # this function is called as a thread so we have to make sure
    ui_handler.cancel_resolve_route()
    # wait a negligible amount so the main thread can realize it should stop
    wait(50)
    ui_handler.opcontrol_ui()
    while True:
        try:
            driver_control(peripherals)
            Logger.dump_to_sdcard()
        except Exception as err:
            Logger.debug(repr(err))
            Logger.dump_to_sdcard()
            ui_show_error("driver control", err)


if COMPETITION_MODE:
    # initialize the competition first so it works if route resolution fails
    Competition(driver, autonomous)
    # calibrate the inertial for use in auton
    peripherals.inertial.calibrate()

    ui_handler.resolve_route()
    selected_autonomous = ui_handler.resolved_route
    Logger.debug("resolved autonomous route: {}".format(selected_autonomous))
    Logger.dump_to_sdcard()
    ui_handler.waiting_ui()
else:
    ui_handler.waiting_ui(do_loop=False)
    Logger.dump_to_sdcard()
    autonomous()
