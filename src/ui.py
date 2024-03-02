from math import floor

from vex import *

from autonomous_common import debug
from constants import AUTONOMOUS_ROUTE

BACKGROUND_COLOR = 0xaaaaff

BRAIN_WIDTH_PX = 480
BRAIN_HEIGHT_PX = 240

ROUTE_TYPE_TITLE_TEXT = "select route type"
ROUTE_TITLE_TEXT = "select autonomous route"
CONFIRM_TEXT = "selecting route '{}'"

PADDING = 20
TOP_PADDING = 32
BOTTOM_BAR_HEIGHT = 32
BOTTOM_PADDING = 5

ROUTE_PADDING = 5
ROUTE_WIDTH = int((BRAIN_WIDTH_PX - PADDING*2 +
                  ROUTE_PADDING)/3 - ROUTE_PADDING)
ROUTE_TYPE_HEIGHT = 70
ROUTE_HEIGHT = 50

BUTTON_HEIGHT = 40
BUTTON_WIDTH = 80

# the first letters of the ID are important - they decide which subcategory
# the route is
AUTONOMOUS_ROUTE_NAMES = {
    "o1": "Offense 1",
    "o2": "Offense 2",
    "o3": "Offense 3",
    "o4": "Offense 4",
    "o5": "Offense 5",
    "o6": "Offense 6",

    "d1": "Defense 1",
    "d2": "Defense 2",
    "d3": "Defense 3",
    "d4": "Defense 4",
    "d5": "Defense 5",
    "d6": "Defense 6",

    "test": "Test",

    "x": "No route"
}


def ui_show_error(context: str, err: Exception):
    # illegally get a screen reference
    screen = Brain().screen
    screen.set_fill_color(0x000000)
    screen.set_pen_color(0xffffff)
    screen.set_font(FontType.MONO20)
    err_text = repr(err)
    debug("error:\n{}".format(err_text))
    text = "error during {}\n  (using route {} if not set):\n\n{}".format(
        context,
        AUTONOMOUS_ROUTE,
        err_text)
    y = 30
    for line in text.split("\n"):
        screen.print_at(
            line,
            x=10,
            y=y
        )
        y += 20
    screen.render()


def ui_crashpad(context: str):
    def decorator(fn: Callable):
        def wrapper(*args):
            try:
                fn(*args)
            except Exception as err:
                try:
                    ui_show_error(context, err)
                except:
                    pass
        return wrapper
    return decorator


class GenericButton:
    pressed: bool
    selected: bool

    last_pressed: bool
    last_selected: bool

    x: int
    y: int
    width: int
    height: int
    text: str
    value: str | None

    def __init__(self, x: int, y: int, width: int, height: int, text: str, value: str | None = None) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.value = value

        self.last_pressed = True
        self.pressed = False
        self.last_selected = True
        self.selected = False

    def render(self, screen: Brain.Lcd, incremental: bool = False):
        pass

    def update(self, touching: bool, clicked: bool, touch_x: int, touch_y: int) -> bool:
        in_box = (self.x <= touch_x <= self.x+self.width and
                  self.y <= touch_y <= self.y+self.height)
        self.pressed = touching and in_box
        if in_box and clicked:
            self.selected = not self.selected
            return self.selected
        return False

    def needs_update(self):
        needs_update = (self.last_pressed != self.pressed or
                        self.last_selected != self.selected)
        self.last_pressed = self.pressed
        self.last_selected = self.selected
        return needs_update

    def set_selected(self, value: bool):
        self.selected = value


class RouteButton(GenericButton):
    @classmethod
    def from_grid_position(cls, ix: int, iy: int, text: str, value: str | None = None, height: int = ROUTE_HEIGHT):
        return cls(
            x=PADDING + ix*(ROUTE_WIDTH + ROUTE_PADDING),
            y=TOP_PADDING + 15 + iy*(height + ROUTE_PADDING),
            width=ROUTE_WIDTH,
            height=height,
            text=text,
            value=value
        )

    def render(self, screen: Brain.Lcd, incremental: bool = False):
        if incremental and not self.needs_update():
            return
        if self.pressed:
            screen.set_fill_color(0xaaaaaa)
        else:
            screen.set_fill_color(0xffffff)
        if self.selected:
            screen.set_pen_color(0x5555ff)
            screen.set_fill_color(0xaaaaff)
            screen.set_pen_width(3)
        else:
            screen.set_pen_width(0)
        screen.draw_rectangle(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height
        )
        screen.set_font(FontType.PROP20)
        screen.set_pen_color(0x000000)
        screen.print_at(
            self.text,
            x=self.x + self.width/2 - screen.get_string_width(self.text)/2,
            y=self.y + self.height/2 + 5
        )


class RouteButtonGroup:
    buttons: list[RouteButton]

    def __init__(self, *buttons: RouteButton) -> None:
        self.buttons = list(buttons)

    def render(self, screen: Brain.Lcd, incremental: bool = False):
        for button in self.buttons:
            button.render(screen, incremental)

    def update(self, touching: bool, clicked: bool, touch_x: int, touch_y: int):
        for button in self.buttons:
            clear_selected_state = button.update(
                touching, clicked, touch_x, touch_y)
            if clear_selected_state:
                for clearing_button in self.buttons:
                    if clearing_button is not button:
                        clearing_button.set_selected(False)

    def has_selected(self) -> bool:
        for button in self.buttons:
            if button.selected:
                return True
        return False

    def selected(self) -> str | None:
        for button in self.buttons:
            if button.selected:
                return button.value
        return None


class NormalButton(GenericButton):
    disabled: bool

    def __init__(self, initial_disabled: bool, *args, **kwargs) -> None:
        self.disabled = initial_disabled
        super().__init__(*args, **kwargs)

    def render(self, screen: Brain.Lcd, incremental: bool = False):
        if incremental and not self.needs_update():
            return
        if self.disabled:
            screen.set_fill_color(0xaaaaaa)
            screen.set_pen_color(0x888888)
        elif self.pressed:
            screen.set_fill_color(0x9999ff)
            screen.set_pen_color(0x000000)
        else:
            screen.set_fill_color(0x5555ff)
            screen.set_pen_color(0x000000)
        if self.selected:
            screen.set_pen_color(0x000000)
            screen.set_pen_width(3)
        else:
            screen.set_pen_width(0)
        screen.draw_rectangle(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height
        )
        screen.set_font(FontType.PROP20)
        screen.print_at(
            self.text,
            x=self.x + self.width/2 - screen.get_string_width(self.text)/2,
            y=self.y + self.height/2 + 5
        )

    def update(self, touching: bool, clicked: bool, touch_x: int, touch_y: int) -> bool:
        clicked = super().update(touching, clicked, touch_x, touch_y)
        if self.disabled:
            self.selected = False
            self.pressed = False
        return not self.disabled and clicked

    def set_disabled(self, value: bool):
        self.disabled = value


class StatusBar:
    team: str
    short_team: str
    status_text: str
    brain: Brain
    battery: float  # between 0 and 1
    has_sdcard: bool

    def __init__(self, brain: Brain, team: str, short_team: str) -> None:
        self.team = team
        self.short_team = short_team
        self.status_text = ""
        self.brain = brain
        self.battery = 0.0
        self.has_sdcard = False

    def update(self, touching: bool, clicked: bool, touch_x: int, touch_y: int):
        self.battery = self.brain.battery.capacity() / 100

    def update_to_route_select(self):
        self.status_text = ""

    def update_to_route(self, route_id: str):
        self.status_text = "running route {}".format(
            AUTONOMOUS_ROUTE_NAMES[route_id])

    def update_to_opcontrol(self):
        self.status_text = "opcontrol period"

    def update_to_waiting_no_route(self):
        self.status_text = "waiting for match start..."

    def update_to_waiting(self, selected: str):
        self.status_text = "waiting to start route '{}'...".format(selected)

    def render(self, screen: Brain.Lcd):
        screen.set_pen_width(0)
        screen.set_fill_color(0x7777ff)
        screen.draw_rectangle(
            x=0,
            y=BRAIN_HEIGHT_PX - BOTTOM_BAR_HEIGHT,
            width=BRAIN_WIDTH_PX,
            height=BOTTOM_BAR_HEIGHT
        )

        screen.set_font(FontType.MONO15)
        screen.set_pen_color(0x000000)
        if len(self.status_text) > 0:
            text = "{} - {}".format(self.short_team, self.status_text)
        else:
            text = self.team
        screen.print_at(
            text,
            x=PADDING,
            y=BRAIN_HEIGHT_PX - 12,
            opaque=False
        )

        item_padding = 15

        battery_width = 50
        battery_height = BOTTOM_BAR_HEIGHT - 5*2

        screen.set_pen_width(2)
        screen.set_pen_color(0x000000)
        screen.set_fill_color(0xaaaaaa)
        screen.draw_rectangle(
            x=BRAIN_WIDTH_PX - PADDING - battery_width,
            y=BRAIN_HEIGHT_PX - BOTTOM_BAR_HEIGHT/2 - battery_height/2,
            width=battery_width,
            height=battery_height
        )
        screen.set_pen_width(0)
        screen.set_fill_color(0x000000)
        screen.draw_rectangle(
            x=BRAIN_WIDTH_PX - PADDING,
            y=BRAIN_HEIGHT_PX - BOTTOM_BAR_HEIGHT/2 - 5,
            width=6,
            height=10
        )
        if self.battery > 0.8:
            screen.set_fill_color(0x3ea629)
        elif self.battery > 0.3:
            screen.set_fill_color(0xff8800)
        else:
            screen.set_fill_color(0xff0000)
        screen.draw_rectangle(
            x=BRAIN_WIDTH_PX - PADDING - battery_width + 1,
            y=BRAIN_HEIGHT_PX - BOTTOM_BAR_HEIGHT/2 - battery_height/2 + 1,
            width=battery_width*self.battery - 1,
            height=battery_height - 1
        )

        screen.set_font(FontType.MONO20)
        screen.set_pen_color(0x000000)
        text = str(int(self.battery * 100))
        screen.print_at(
            text,
            x=BRAIN_WIDTH_PX - PADDING - battery_width /
            2 - screen.get_string_width(text)/2,
            y=BRAIN_HEIGHT_PX - BOTTOM_BAR_HEIGHT/2 + 6,
            opaque=False
        )

        sdcard_width = 15
        sdcard_height = battery_height
        screen.set_fill_color(0x666666)
        screen.draw_rectangle(
            x=BRAIN_WIDTH_PX - PADDING - battery_width - sdcard_width - item_padding,
            y=BRAIN_HEIGHT_PX - BOTTOM_BAR_HEIGHT/2 - sdcard_height/2,
            width=sdcard_width,
            height=sdcard_height
        )
        screen.set_pen_color(0x7777ff)
        screen.set_pen_width(5)
        screen.draw_line(
            x1=BRAIN_WIDTH_PX - PADDING - battery_width - 4 - item_padding,
            y1=BRAIN_HEIGHT_PX - BOTTOM_BAR_HEIGHT/2 - sdcard_height/2 - 3,
            x2=BRAIN_WIDTH_PX - PADDING - battery_width - item_padding + 3,
            y2=BRAIN_HEIGHT_PX - BOTTOM_BAR_HEIGHT/2 - sdcard_height/2 + 4,
        )
        screen.set_font(FontType.MONO12)
        screen.set_pen_color(0x333333)
        text = "SD"
        screen.print_at(
            text,
            x=BRAIN_WIDTH_PX - PADDING - battery_width - sdcard_width /
            2 - item_padding - screen.get_string_width(text)/2,
            y=BRAIN_HEIGHT_PX - BOTTOM_BAR_HEIGHT/2 + 5,
            opaque=False
        )
        if not self.has_sdcard:
            screen.set_pen_color(0xff0000)
            screen.set_pen_width(3)
            screen.draw_line(
                x1=BRAIN_WIDTH_PX - PADDING - battery_width - sdcard_width - item_padding - 1,
                y1=BRAIN_HEIGHT_PX - BOTTOM_BAR_HEIGHT/2 - sdcard_height/2 - 1,
                x2=BRAIN_WIDTH_PX - PADDING - battery_width - item_padding + 1,
                y2=BRAIN_HEIGHT_PX - BOTTOM_BAR_HEIGHT/2 + sdcard_height/2 + 1
            )


class AutonSelectorScreen:
    route_type: str | None = None

    resolved: str | None = None

    button_group: RouteButtonGroup
    next_button: NormalButton
    back_button: NormalButton | None

    brain: Brain

    def __init__(self, brain: Brain) -> None:
        self.brain = brain
        self.update_to_route_type_select()

    def update_to_route_type_select(self):
        self.button_group = RouteButtonGroup(
            RouteButton.from_grid_position(
                0, 0, "Defense", "d", ROUTE_TYPE_HEIGHT),
            RouteButton.from_grid_position(
                1, 0, "Offense", "o", ROUTE_TYPE_HEIGHT),
            RouteButton.from_grid_position(
                2, 0, "No route!", "x", ROUTE_TYPE_HEIGHT),
            RouteButton.from_grid_position(
                0, 1, "Test route", "t", ROUTE_TYPE_HEIGHT)
        )
        self.back_button = None
        self.next_button = NormalButton(
            initial_disabled=True,
            x=BRAIN_WIDTH_PX - BUTTON_WIDTH - PADDING,
            y=BRAIN_HEIGHT_PX - BUTTON_HEIGHT - BOTTOM_PADDING - BOTTOM_BAR_HEIGHT,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            text="Next"
        )

    def update_to_route_select(self):
        if self.route_type is None:
            raise Exception("invalid state")
        routes = [route for route in AUTONOMOUS_ROUTE_NAMES.keys()
                  if route.startswith(self.route_type)]

        buttons = []
        # I would use enumerate but apparently the VEX V5 brain doesn't support
        # it, even though the MicroPython version info claims it supports up to
        # Python 3.5
        i = 0
        for id in routes:
            buttons.append(RouteButton.from_grid_position(
                ix=i % 3,
                iy=floor(i/3),
                text=AUTONOMOUS_ROUTE_NAMES[id],
                value=id
            ))
            i += 1
        self.button_group = RouteButtonGroup(
            *buttons
        )
        self.back_button = NormalButton(
            initial_disabled=False,
            x=PADDING,
            y=BRAIN_HEIGHT_PX - BUTTON_HEIGHT - BOTTOM_PADDING - BOTTOM_BAR_HEIGHT,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            text="Back"
        )
        self.next_button = NormalButton(
            initial_disabled=True,
            x=BRAIN_WIDTH_PX - BUTTON_WIDTH - PADDING,
            y=BRAIN_HEIGHT_PX - BUTTON_HEIGHT - BOTTOM_PADDING - BOTTOM_BAR_HEIGHT,
            width=BUTTON_WIDTH,
            height=BUTTON_HEIGHT,
            text="Select"
        )

    def render(self, screen: Brain.Lcd):
        screen.set_fill_color(BACKGROUND_COLOR)
        screen.set_pen_width(0)
        screen.draw_rectangle(
            x=0,
            y=0,
            width=BRAIN_WIDTH_PX,
            height=BRAIN_HEIGHT_PX
        )

        screen.set_font(FontType.PROP30)
        screen.set_fill_color(BACKGROUND_COLOR)
        screen.set_pen_color(0x000000)
        if self.route_type is None:
            text = ROUTE_TYPE_TITLE_TEXT
        else:
            text = ROUTE_TITLE_TEXT
        screen.print_at(
            text,
            x=BRAIN_WIDTH_PX/2 - screen.get_string_width(text)/2,
            y=TOP_PADDING
        )

        button_group_selected = self.button_group.selected()

        if self.route_type is not None and button_group_selected is not None:
            screen.set_font(FontType.PROP20)
            screen.set_fill_color(BACKGROUND_COLOR)
            screen.set_pen_color(0x000000)
            text = CONFIRM_TEXT.format(button_group_selected)
            screen.print_at(
                text,
                x=BRAIN_WIDTH_PX/2 - screen.get_string_width(text)/2,
                y=BRAIN_HEIGHT_PX - BOTTOM_BAR_HEIGHT - BOTTOM_PADDING - 15
            )

        self.button_group.render(screen)

        if self.back_button is not None:
            self.back_button.render(screen)
        self.next_button.render(screen)

    def update(self, touching: bool, clicked: bool, touch_x: int, touch_y: int):
        self.button_group.update(touching, clicked, touch_x, touch_y)

        back_clicked = False
        if self.back_button is not None:
            back_clicked = self.back_button.update(
                touching, clicked, touch_x, touch_y)
        next_clicked = self.next_button.update(
            touching, clicked, touch_x, touch_y)
        self.next_button.set_disabled(not self.button_group.has_selected())

        if back_clicked:
            self.route_type = None
            self.update_to_route_type_select()

        if next_clicked:
            if self.route_type is None:
                self.route_type = self.button_group.selected()
                self.update_to_route_select()
            else:
                self.resolved = self.button_group.selected()


class UiHandler:
    brain: Brain
    resolved_route: str

    was_touching: bool

    touching: bool
    clicked: bool
    touch_x: int
    touch_y: int

    status_bar: StatusBar

    def __init__(self, brain: Brain, team: str, short_team: str) -> None:
        self.brain = brain
        self.resolved_route = AUTONOMOUS_ROUTE
        self.was_touching = False
        self.status_bar = StatusBar(brain, team, short_team)

        self.touching = False
        self.clicked = False
        self.touch_x = -1
        self.touch_y = -1

    def update(self):
        self.touching = self.brain.screen.pressing()
        self.clicked = not self.touching and self.was_touching
        self.was_touching = self.touching
        self.touch_x = self.brain.screen.x_position()
        self.touch_y = self.brain.screen.y_position()

        self.status_bar.update(*self.touch_info())

    def render(self):
        self.status_bar.render(self.brain.screen)

    def touch_info(self) -> tuple[bool, bool, int, int]:
        return (self.touching, self.clicked, self.touch_x, self.touch_y)

    @ui_crashpad("ui rendering")
    def resolve_route(self) -> None:
        self.status_bar.update_to_route_select()
        selector = AutonSelectorScreen(self.brain)
        while selector.resolved is None:
            selector.update(*self.touch_info())
            self.update()
            selector.render(self.brain.screen)
            self.render()
            self.brain.screen.render()
        self.brain.screen.clear_screen()
        self.brain.screen.render()
        self.resolved_route = selector.resolved

    @ui_crashpad("ui rendering")
    def route_ui(self, route: str) -> None:
        self.status_bar.update_to_route(route)
        self.update()
        self.render()
        self.brain.screen.render()

    @ui_crashpad("ui rendering")
    def opcontrol_ui(self) -> None:
        self.status_bar.update_to_opcontrol()
        self.update()
        self.render()
        self.brain.screen.render()

    @ui_crashpad("ui rendering")
    def waiting_ui(self) -> None:
        if self.resolved_route is None:
            self.status_bar.update_to_waiting_no_route()
        else:
            self.status_bar.update_to_waiting(self.resolved_route)
        self.update()
        self.render()
        self.brain.screen.render()
