from vex import *
from threshold import Threshold
from utils import Logger


class UltrasonicClaw:
    pneumatic: Pneumatics
    ultrasonic: Sonar
    _can_close: bool
    _close_threshold: Threshold
    _can_close_threshold: Threshold

    def __init__(self, pneumatic: Pneumatics, ultrasonic: Sonar) -> None:
        self.pneumatic = pneumatic
        self.ultrasonic = ultrasonic
        self._can_close = True
        self._close_threshold = Threshold(100, False, True)
        self._can_close_threshold = Threshold(400, True, False)

    def update(self):
        distance = self.ultrasonic.distance(MM)
        if self._close_threshold.update(distance) and self._can_close:
            self._can_close = False
            self.pneumatic.close()
        if self._can_close_threshold.update(distance):
            self._can_close = True

    def close(self):
        self.pneumatic.close()
        self._can_close = True

    def open(self):
        self.pneumatic.open()
        self._can_close = False
