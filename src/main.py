from vex import *

from autonomous_common import debug
from autonomous_test import autonomous_test
from constants import AUTONOMOUS_ROUTE, COMPETITION_MODE, USE_REAL_BOT
from driver_control import driver_control
from peripherals import RealBotPeripherals, TestBotPeripherals
from ui import UiHandler, ui_show_error

# default to AUTONOMOUS_ROUTE but allow selection
selected_autonomous: str = AUTONOMOUS_ROUTE

if USE_REAL_BOT:
    peripherals = RealBotPeripherals()
else:
    peripherals = TestBotPeripherals()
ui_handler = UiHandler(peripherals.brain, "DOXA Robotics 99484", "99484")


def autonomous():
    ui_handler.route_ui(selected_autonomous)
    if selected_autonomous == "test":
        autonomous_test(peripherals)


def driver():
    ui_handler.opcontrol_ui()
    while True:
        try:
            driver_control(peripherals)
        except Exception as err:
            ui_show_error("driver control", err)


if COMPETITION_MODE:
    ui_handler.resolve_route()
    selected_autonomous = ui_handler.resolved_route
    debug("resolved autonomous route: {}".format(selected_autonomous))
    ui_handler.waiting_ui()
    Competition(driver, autonomous)
else:
    ui_handler.waiting_ui()
    autonomous()
