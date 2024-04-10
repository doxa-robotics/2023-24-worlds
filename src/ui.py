from math import floor

from vex import *

from constants import AUTONOMOUS_ROUTE
from peripherals import Peripherals
from routes import Route
from utils import Logger, time_seconds

BRAIN_WIDTH_PX = 480
BRAIN_HEIGHT_PX = 240

ROUTE_TYPE_TITLE_TEXT = "select route type"
ROUTE_TITLE_TEXT = "select autonomous route"
CONFIRM_TEXT = "selecting route '{}'"
NO_ROUTE_TEXT = "No route"

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


def ui_show_error(context: str, err: Exception):
    # illegally get a screen reference
    screen = Brain().screen
    screen.set_fill_color(0x000000)
    screen.set_pen_color(0xffffff)
    screen.set_font(FontType.MONO20)
    err_text = repr(err)
    Logger.debug("error!:\n{}".format(err_text))
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
        def wrapper(*args, **kwargs):
            try:
                fn(*args, **kwargs)
            except Exception as err:
                try:
                    ui_show_error(context, err)
                except:
                    pass
        return wrapper
    return decorator


class UiTheme:
    background: Color
    text: Color

    tile: Color
    tile_text: Color
    tile_pressed: Color
    tile_selected: Color
    tile_selected_border: Color

    button: Color
    button_text: Color
    button_pressed: Color
    button_selected: Color
    button_selected_border: Color
    button_disabled: Color
    button_disabled_text: Color

    button_fatal: Color

    status: Color
    status_text: Color

    # python 3.7 dataclasses nashi...
    def __init__(
        self,
        background: Color,
        text: Color,

        tile: Color,
        tile_text: Color,
        tile_pressed: Color,
        tile_selected: Color,
        tile_selected_border: Color,

        button: Color,
        button_text: Color,
        button_pressed: Color,
        button_selected: Color,
        button_selected_border: Color,
        button_disabled: Color,
        button_disabled_text: Color,

        status: Color,
        status_text: Color,

        button_fatal: Color
    ) -> None:
        self.background = background
        self.text = text
        self.tile = tile
        self.tile_text = tile_text
        self.tile_pressed = tile_pressed
        self.tile_selected = tile_selected
        self.tile_selected_border = tile_selected_border
        self.button = button
        self.button_text = button_text
        self.button_pressed = button_pressed
        self.button_selected = button_selected
        self.button_selected_border = button_selected_border
        self.button_disabled = button_disabled
        self.button_disabled_text = button_disabled_text
        self.status = status
        self.status_text = status_text
        self.button_fatal = button_fatal

    @classmethod
    def theme_blue(cls):
        return cls(
            background=Color(0xaaaaff),
            text=Color(0x000000),

            tile=Color(0xffffff),
            tile_text=Color(0x000000),
            tile_pressed=Color(0xaaaaaa),
            tile_selected=Color(0x8888ff),
            tile_selected_border=Color(0x5555ff),

            button=Color(0x5555ff),
            button_text=Color(0x000000),
            button_pressed=Color(0x9999ff),
            button_selected=Color(0x5555ff),
            button_selected_border=Color(0x000000),
            button_disabled=Color(0xaaaaaa),
            button_disabled_text=Color(0x888888),

            status=Color(0x7777ff),
            status_text=Color(0x000000),
            button_fatal=Color(0xff0000)
        )

    @classmethod
    def theme_black(cls):
        return cls(
            background=Color(0x222222),
            text=Color(0x999999),

            tile=Color(0x000000),
            tile_text=Color(0xcccccc),
            tile_pressed=Color(0x333333),
            tile_selected=Color(0x555555),
            tile_selected_border=Color(0xffffff),

            button=Color(0x444444),
            button_text=Color(0xffffff),
            button_pressed=Color(0x333333),
            button_selected=Color(0x444444),
            button_selected_border=Color(0xffffff),
            button_disabled=Color(0x2a2a2a),
            button_disabled_text=Color(0x666666),

            status=Color(0x333333),
            status_text=Color(0x888888),
            button_fatal=Color(0xff0000)
        )


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

    def render(self, screen: Brain.Lcd, theme: UiTheme, incremental: bool = False):
        pass

    def update(self, touching: bool, clicked: bool, touch_x: int, touch_y: int) -> bool:
        in_box = (self.x <= touch_x <= self.x+self.width and
                  self.y <= touch_y <= self.y+self.height)
        self.pressed = touching and in_box
        if in_box and clicked:
            self.selected = not self.selected
            return True
        return in_box

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

    def render(self, screen: Brain.Lcd, theme: UiTheme, incremental: bool = False):
        if incremental and not self.needs_update():
            return
        if self.pressed:
            screen.set_fill_color(theme.tile_pressed)
        elif self.selected:
            screen.set_fill_color(theme.tile_selected)
        else:
            screen.set_fill_color(theme.tile)
        if self.selected:
            screen.set_pen_color(theme.tile_selected_border)
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
        screen.set_pen_color(theme.tile_text)
        screen.print_at(
            self.text,
            x=self.x + self.width/2 - screen.get_string_width(self.text)/2,
            y=self.y + self.height/2 + 5
        )


class RouteButtonGroup:
    buttons: list[RouteButton]

    def __init__(self, *buttons: RouteButton) -> None:
        self.buttons = list(buttons)

    def render(self, screen: Brain.Lcd, theme: UiTheme, incremental: bool = False):
        for button in self.buttons:
            button.render(screen, theme, incremental)

    def update(self, touching: bool, clicked: bool, touch_x: int, touch_y: int) -> bool:
        for button in self.buttons:
            consumed = button.update(
                touching, clicked, touch_x, touch_y)
            if button.selected:
                for clearing_button in self.buttons:
                    if clearing_button is not button:
                        clearing_button.set_selected(False)
            if consumed:
                return True
        return False

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

    def render(self, screen: Brain.Lcd, theme: UiTheme, incremental: bool = False):
        if incremental and not self.needs_update():
            return
        if self.disabled:
            screen.set_fill_color(theme.button_disabled)
        elif self.pressed:
            screen.set_fill_color(theme.button_pressed)
        elif self.selected:
            screen.set_fill_color(theme.button_selected)
        else:
            screen.set_fill_color(theme.button)
        if self.selected:
            screen.set_pen_color(theme.button_selected_border)
            screen.set_pen_width(3)
        else:
            screen.set_pen_width(0)
        screen.draw_rectangle(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height
        )
        if self.disabled:
            screen.set_pen_color(theme.button_disabled_text)
        else:
            screen.set_pen_color(theme.button_text)
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
        return clicked

    def set_disabled(self, value: bool):
        self.disabled = value


class StatusBar:
    team: str
    short_team: str
    status_text: str
    brain: Brain

    last_text: str
    text: str
    last_battery: float
    battery: float  # between 0 and 1
    last_has_sdcard: bool
    has_sdcard: bool

    is_calibrating: bool = False

    def __init__(self, brain: Brain, team: str, short_team: str) -> None:
        self.team = team
        self.short_team = short_team
        self.status_text = ""
        self.brain = brain

        self.update()

        self.last_battery = -self.battery
        self.last_has_sdcard = not self.has_sdcard
        self.last_text = "_{}".format(self.text)

    def update(self):
        self.battery = self.brain.battery.capacity() / 100
        self.has_sdcard = self.brain.sdcard.is_inserted()
        if len(self.status_text) > 0:
            self.text = "{} - {}".format(self.short_team, self.status_text)
        elif self.is_calibrating:
            self.text = "calibrating, please don't move"
        else:
            self.text = self.team

    def update_to_route_select(self):
        self.status_text = ""
        self.update()

    def update_to_route(self, route_id: str):
        self.status_text = "running route {}".format(route_id)
        self.update()

    def update_to_opcontrol(self):
        self.status_text = "opcontrol period"
        self.update()

    def update_to_waiting_no_route(self):
        self.status_text = "skipping autonomous, waiting..."
        self.update()

    def update_to_waiting(self, selected: str):
        self.status_text = "waiting to start route '{}'...".format(selected)
        self.update()

    def needs_update(self):
        return (self.last_battery != self.battery or
                self.last_has_sdcard != self.has_sdcard or
                self.last_text != self.text)

    def render(self, screen: Brain.Lcd, theme: UiTheme, incremental: bool = False):
        if incremental and not self.needs_update():
            return
        self.last_battery = self.battery
        self.last_has_sdcard = self.has_sdcard
        self.last_text = self.text

        screen.set_pen_width(0)
        screen.set_fill_color(theme.status)
        screen.draw_rectangle(
            x=0,
            y=BRAIN_HEIGHT_PX - BOTTOM_BAR_HEIGHT,
            width=BRAIN_WIDTH_PX,
            height=BOTTOM_BAR_HEIGHT
        )

        screen.set_font(FontType.MONO15)
        screen.set_pen_color(theme.status_text)
        screen.print_at(
            self.text,
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
        screen.set_pen_color(theme.status)
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


class MotorTempWidget(GenericButton):
    peripherals: Peripherals
    worst_left_motor_temp: float
    worst_right_motor_temp: float

    popup_width = 120
    popup_height = 80

    hidden = False

    def __init__(self, peripherals: Peripherals, *args, **kwargs) -> None:
        self.peripherals = peripherals
        super().__init__(*args, **kwargs, text="Temperatures")

    def update(self, touching: bool, clicked: bool, touch_x: int, touch_y: int) -> bool:
        self.worst_left_motor_temp = 0
        for motor in self.peripherals.left_motors_list:
            temp = motor.temperature()
            if temp > self.worst_left_motor_temp:
                self.worst_left_motor_temp = temp
        self.worst_right_motor_temp = 0
        for motor in self.peripherals.right_motors_list:
            temp = motor.temperature()
            if temp > self.worst_right_motor_temp:
                self.worst_right_motor_temp = temp
        consumed = super().update(touching, clicked, touch_x, touch_y)
        consumed = consumed or (
            self.selected and
            self.x <= touch_x <= self.x + self.popup_width and
            self.y + self.height <= touch_y <= self.y + self.height + self.popup_height
        )
        return consumed

    def render(self, screen: Brain.Lcd, theme: UiTheme, incremental: bool = False):
        if incremental and not self.needs_update():
            raise Exception("MotorTempWidget can't be incrementally rendered")
        if self.hidden:
            return
        if self.pressed:
            screen.set_fill_color(theme.button_pressed)
        elif self.selected:
            screen.set_fill_color(theme.button_selected)
        else:
            screen.set_fill_color(theme.button)
        if self.selected:
            screen.set_pen_color(theme.button_selected_border)
            screen.set_pen_width(3)
        else:
            screen.set_pen_width(0)
        screen.draw_rectangle(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height
        )
        screen.set_font(FontType.MONO12)
        screen.set_pen_color(theme.button_text)
        screen.print_at(
            self.text,
            x=self.x + self.width/2 - screen.get_string_width(self.text)/2,
            y=self.y + self.height/2 + 3
        )
        if self.selected:
            screen.set_fill_color(theme.button_selected)
            screen.set_pen_width(0)
            screen.draw_rectangle(
                x=self.x,
                y=self.y + self.height,
                width=self.popup_width,
                height=self.popup_height
            )
            screen.set_pen_color(theme.button_text)
            screen.set_font(FontType.MONO12)
            text = "Left motors (max)"
            screen.print_at(
                text,
                x=self.x+5,
                y=self.y + self.height + 15
            )
            screen.set_font(FontType.MONO20)
            screen.print_at(
                "{}C".format(self.worst_left_motor_temp),
                x=self.x+5,
                y=self.y + self.height + 34
            )
            screen.set_font(FontType.MONO12)
            text = "Right motors (max)"
            screen.print_at(
                text,
                x=self.x+5,
                y=self.y + self.height + 52
            )
            screen.set_font(FontType.MONO20)
            screen.print_at(
                "{}C".format(self.worst_right_motor_temp),
                x=self.x+5,
                y=self.y + self.height + 71
            )


class AutonSelectorScreen:
    route_type: str | None = None

    resolved: str | None = None
    route_mapping: dict[str, list[type[Route]]]

    button_group: RouteButtonGroup
    next_button: NormalButton
    back_button: NormalButton | None

    brain: Brain

    def __init__(self, brain: Brain, routes: list[type[Route]]) -> None:
        self.brain = brain
        self.route_mapping = {}
        for route in routes:
            category = route.category_name()
            if self.route_mapping.get(category) is None:
                self.route_mapping[category] = []
            self.route_mapping[category].append(route)
        self.update_to_route_type_select()

    def update_to_route_type_select(self):
        categories = []
        i = 0
        for category in self.route_mapping.keys():
            categories.append(RouteButton.from_grid_position(
                i % 3, floor(i / 3), category, category, ROUTE_TYPE_HEIGHT))
            i += 1
        self.button_group = RouteButtonGroup(
            *categories
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
        routes = self.route_mapping[self.route_type]
        routes.sort(key=lambda route: route.name())

        buttons = []
        # I would use enumerate but apparently the VEX V5 brain doesn't support
        # it, even though the MicroPython version info claims it supports up to
        # Python 3.5
        i = 0
        for route in routes:
            buttons.append(RouteButton.from_grid_position(
                ix=i % 3,
                iy=floor(i/3),
                text=route.name(),
                value=route.name()
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

    def render(self, screen: Brain.Lcd, theme: UiTheme):
        screen.set_fill_color(theme.background)
        screen.set_pen_width(0)
        screen.draw_rectangle(
            x=0,
            y=0,
            width=BRAIN_WIDTH_PX,
            height=BRAIN_HEIGHT_PX
        )

        screen.set_font(FontType.PROP30)
        screen.set_pen_color(theme.text)
        if self.route_type is None:
            text = ROUTE_TYPE_TITLE_TEXT
        else:
            text = ROUTE_TITLE_TEXT
        screen.print_at(
            text,
            x=BRAIN_WIDTH_PX/2 - screen.get_string_width(text)/2,
            y=TOP_PADDING,
            opaque=False
        )

        button_group_selected = self.button_group.selected()

        if self.route_type is not None and button_group_selected is not None:
            screen.set_font(FontType.PROP20)
            screen.set_pen_color(theme.text)
            text = CONFIRM_TEXT.format(button_group_selected)
            screen.print_at(
                text,
                x=BRAIN_WIDTH_PX/2 - screen.get_string_width(text)/2,
                y=BRAIN_HEIGHT_PX - BOTTOM_BAR_HEIGHT - BOTTOM_PADDING - 15,
                opaque=False
            )

        self.button_group.render(screen, theme)

        if self.back_button is not None:
            self.back_button.render(screen, theme)
        self.next_button.render(screen, theme)

    def update(self, touching: bool, clicked: bool, touch_x: int, touch_y: int):
        consumed = self.button_group.update(
            touching, clicked, touch_x, touch_y)
        self.next_button.set_disabled(not self.button_group.has_selected())
        if consumed:
            return True

        if self.back_button is not None:
            consumed = self.back_button.update(
                touching, clicked, touch_x, touch_y)
            if self.back_button.selected:
                self.route_type = None
                self.update_to_route_type_select()
            if consumed:
                return True

        consumed = self.next_button.update(
            touching, clicked, touch_x, touch_y)
        if self.next_button.selected:
            if self.route_type is None:
                self.route_type = self.button_group.selected()
                self.update_to_route_select()
            else:
                self.resolved = self.button_group.selected()
        if consumed:
            return True

        return False


class UiHandler:
    brain: Brain
    peripherals: Peripherals

    resolved_route: str
    routes: list[type[Route]]

    was_touching: bool

    touching: bool
    clicked: bool
    touch_x: int
    touch_y: int

    motor_temp_widget: MotorTempWidget
    status_bar: StatusBar

    theme: UiTheme

    resolve_route_canceled: bool

    def __init__(self, brain: Brain, peripherals: Peripherals, team: str, short_team: str, routes: list[type[Route]]) -> None:
        self.brain = brain
        self.peripherals = peripherals

        self.resolved_route = AUTONOMOUS_ROUTE
        self.was_touching = False
        self.resolve_route_canceled = False

        self.motor_temp_widget = MotorTempWidget(
            peripherals, x=0, y=0, width=80, height=30)
        self.status_bar = StatusBar(brain, team, short_team)

        self.touching = False
        self.clicked = False
        self.touch_x = -1
        self.touch_y = -1

        self.routes = routes

        self.theme = UiTheme.theme_black()

    def update(self):
        self.touching = self.brain.screen.pressing()
        self.clicked = not self.touching and self.was_touching
        self.was_touching = self.touching
        self.touch_x = self.brain.screen.x_position()
        self.touch_y = self.brain.screen.y_position()

        self.status_bar.update()
        return self.motor_temp_widget.update(*self.touch_info())

    def render(self, skip_image: bool = False):
        if not skip_image:
            self.brain.screen.draw_image_from_file("logo.bmp", 0, 0)
        self.motor_temp_widget.render(self.brain.screen, self.theme)
        self.status_bar.render(self.brain.screen, self.theme)

    def touch_info(self) -> tuple[bool, bool, int, int]:
        return (self.touching, self.clicked, self.touch_x, self.touch_y)

    @Logger.logger_context("UiHandler.resolve_route")
    @ui_crashpad("ui rendering")
    def resolve_route(self) -> None:
        self.status_bar.update_to_route_select()
        selector = AutonSelectorScreen(self.brain, self.routes)
        while selector.resolved is None and not self.resolve_route_canceled:
            if not self.update():
                # skip updating selector if we consumed the touch
                selector.update(*self.touch_info())
            self.status_bar.is_calibrating = self.peripherals.inertial.is_calibrating()
            selector.render(self.brain.screen, self.theme)
            self.render(skip_image=True)
            self.brain.screen.render()
        Logger.debug("finished resolution, clearing screen")
        self.brain.screen.clear_screen()
        self.brain.screen.render()
        if selector.resolved is not None:
            self.resolved_route = selector.resolved

    def cancel_resolve_route(self) -> None:
        self.resolve_route_canceled = True

    @Logger.logger_context("UiHandler.route_ui")
    @ui_crashpad("ui rendering")
    def route_ui(self, route: str) -> None:
        self.motor_temp_widget.set_selected(False)
        self.motor_temp_widget.hidden = True
        self.status_bar.update_to_route(route)
        self.update()
        self.render()
        self.brain.screen.render()
        Logger.debug("rendered route UI")

    @ui_crashpad("ui rendering")
    def opcontrol_ui(self) -> None:
        self.motor_temp_widget.hidden = True
        self.motor_temp_widget.set_selected(False)
        self.status_bar.update_to_opcontrol()
        self.update()
        self.render()
        self.brain.screen.render()

    @Logger.logger_context("UiHandler.waiting_ui")
    @ui_crashpad("ui rendering")
    def waiting_ui(self, do_loop=True) -> None:
        if self.resolved_route is None or self.resolved_route == NO_ROUTE_TEXT:
            self.status_bar.update_to_waiting_no_route()
        else:
            self.status_bar.update_to_waiting(self.resolved_route)
        while True:
            self.update()
            self.render()
            self.brain.screen.render()
            if not do_loop or self.resolve_route_canceled:
                break
        Logger.debug("waiting done")

    timer_start: float = 0

    @Logger.logger_context("UiHandler.start_timer")
    @ui_crashpad("ui rendering")
    def start_timer(self):
        self.timer_start = time_seconds(self.peripherals)

    @Logger.logger_context("UiHandler.show_timer")
    @ui_crashpad("ui rendering")
    def show_timer(self):
        elapsed = time_seconds(self.peripherals) - self.timer_start
        screen = self.brain.screen
        screen.set_fill_color(0x000000 if elapsed <= 15.0 else 0xaa4444)
        screen.set_pen_color(0xffffff)
        screen.set_font(FontType.PROP60)
        text = "{} secs".format(
            elapsed)
        screen.print_at(
            text,
            x=BRAIN_WIDTH_PX/2 - screen.get_string_width(text)/2,
            y=80
        )
        screen.render()
