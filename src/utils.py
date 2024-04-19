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


CURRENT_INDEX_FILENAME = ".log-index"


class BaseLogger:
    indentation: int
    content: str
    last_dump_time: float
    p: Peripherals | None
    sdcard: Brain.Sdcard | None
    dump_file_index: int

    def __init__(self, p: Peripherals | None = None) -> None:
        self.indentation = 0
        self.last_dump_time = 0
        self.content = ""
        self.sdcard = None
        self.p = None
        self.dump_file_index = -1
        if p is not None:
            self.set_peripherals(p)

    def set_peripherals(self, p: Peripherals):
        self.sdcard = p.brain.sdcard if p.brain.sdcard.is_inserted() else None
        self.p = p
        if self.sdcard is not None:
            dump_file_index = 0
            try:
                dump_file_index = int(self.sdcard.loadfile(
                    CURRENT_INDEX_FILENAME).decode("utf-8", "ignore")) + 1
            except:
                pass
            self.dump_file_index = dump_file_index
            self.sdcard.savefile(CURRENT_INDEX_FILENAME,
                                 bytearray(str(dump_file_index), "utf-8"))

    def format_dump_filename(self):
        return "run-{}.log".format(self.dump_file_index)

    def debug(self, content: str):
        line = "{}{}".format("  " * self.indentation, content)
        if self.p is not None:
            ms = str(time_seconds(self.p) * 1000.0)
            self.content += ms
            self.content += " " * (6 - len(ms))
        self.content += line
        self.content += "\n"
        self.print(line)
        if self.p is not None and time_seconds(self.p) - self.last_dump_time > 1.0:
            self.dump_to_sdcard()

    def dump_to_sdcard(self):
        if self.p is not None and self.sdcard is not None:
            bytes_written = self.sdcard.savefile(self.format_dump_filename(),
                                                 bytearray(self.content, "utf-8"))
            self.last_dump_time = time_seconds(self.p)
            self.debug("dumped {} bytes to {}".format(
                bytes_written, self.format_dump_filename()))

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
