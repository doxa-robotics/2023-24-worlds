from vex import *

from utils import debug, has_interaction
from constants import AUTONOMOUS_ROUTE, COMPETITION_MODE, USE_REAL_BOT
from driver_control import driver_control
from peripherals import Peripherals, RealBotPeripherals, TestBotPeripherals
from pid_drivetrain import PIDDrivetrain
from ui import UiHandler, ui_show_error
from routes import routes

# default to AUTONOMOUS_ROUTE but allow selection
selected_autonomous: str = AUTONOMOUS_ROUTE

peripherals: Peripherals
if USE_REAL_BOT:
    peripherals = RealBotPeripherals()
else:
    peripherals = TestBotPeripherals()
drivetrain = PIDDrivetrain(peripherals)
ui_handler = UiHandler(peripherals.brain, peripherals,
                       "DOXA Robotics 99484", "99484",
                       routes)


def autonomous():
    # this function is called as a thread so we have to make sure
    ui_handler.cancel_resolve_route()
    # wait a negligible amount so the main thread can realize it should stop
    wait(50)
    ui_handler.route_ui(selected_autonomous)
    route = None
    for possible_route in routes:
        if possible_route.name() == selected_autonomous:
            route = possible_route
    if route is None:
        raise Exception("undefined route! {}".format(route))
    route.run(peripherals, drivetrain)


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
