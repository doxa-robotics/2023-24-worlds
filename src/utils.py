from vex import *
from peripherals import Peripherals
from sys import stderr


def has_interaction(p: Peripherals):
    c = p.controller
    return (
        abs(c.axis1.position()) > 5 or
        abs(c.axis2.position()) > 5 or
        abs(c.axis3.position()) > 5 or
        abs(c.axis4.position()) > 5 or
        c.buttonA.pressing() or
        c.buttonX.pressing() or
        c.buttonY.pressing() or
        c.buttonB.pressing() or
        c.buttonUp.pressing() or
        c.buttonDown.pressing() or
        c.buttonLeft.pressing() or
        c.buttonRight.pressing() or
        c.buttonR1.pressing() or
        c.buttonR2.pressing() or
        c.buttonL1.pressing() or
        c.buttonL2.pressing()
    )


def time_seconds(p: Peripherals):
    return p.brain.timer.system() / 1000


class BaseLogger:
    indentation: int

    def __init__(self) -> None:
        self.indentation = 0

    def debug(self, content: str):
        self.print("{}{}".format("  " * self.indentation, content))

    def print(self, content: str):
        print(content, file=stderr)

    def logger_context(self, context: str):
        def decorator(fn: Callable):
            def wrapper(*args, **kwargs):
                self.debug("[{}]".format(context))
                self.indentation += 1
                fn(*args, **kwargs)
                self.indentation -= 1
            return wrapper
        return decorator


Logger = BaseLogger()
