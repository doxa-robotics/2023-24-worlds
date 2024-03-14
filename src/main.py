from vex import *

from autonomous_common import debug
from autonomous_test import autonomous_test
from constants import AUTONOMOUS_ROUTE, COMPETITION_MODE, USE_REAL_BOT
from driver_control import driver_control
from peripherals import RealBotPeripherals, TestBotPeripherals
from pid_drivetrain import PIDDrivetrain
from ui import UiHandler, ui_show_error
from routes import offense_1

# default to AUTONOMOUS_ROUTE but allow selection
selected_autonomous: str = AUTONOMOUS_ROUTE

if USE_REAL_BOT:
    peripherals = RealBotPeripherals()
else:
    peripherals = TestBotPeripherals()
drivetrain = PIDDrivetrain(peripherals)
ui_handler = UiHandler(peripherals.brain, peripherals,
                       "DOXA Robotics 99484", "99484")


def autonomous():
    # this function is called as a thread so we have to make sure
    ui_handler.cancel_resolve_route()
    # wait a negligible amount so the main thread can realize it should stop
    wait(50)
    ui_handler.route_ui(selected_autonomous)
    if selected_autonomous == "test":
        autonomous_test(peripherals, drivetrain)
    elif selected_autonomous == "o1":
        offense_1.offense_1()


def driver():
    # this function is called as a thread so we have to make sure
    ui_handler.cancel_resolve_route()
    # wait a negligible amount so the main thread can realize it should stop
    wait(50)
    ui_handler.opcontrol_ui()
    while True:
        try:
            driver_control(peripherals)
        except Exception as err:
            ui_show_error("driver control", err)


if COMPETITION_MODE:
    # initialize the competition first so it works if route resolution fails
    Competition(driver, autonomous)

    ui_handler.resolve_route()
    selected_autonomous = ui_handler.resolved_route
    debug("resolved autonomous route: {}".format(selected_autonomous))
    ui_handler.waiting_ui()
else:
    ui_handler.waiting_ui(do_loop=False)
    autonomous()
