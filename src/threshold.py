class Threshold:
    _threshold: float
    _value: float | None
    rising: bool
    falling: bool

    def __init__(self, threshold: int | float, rising: bool, falling: bool) -> None:
        self._threshold = float(threshold)
        self._value = None
        self.rising = rising
        self.falling = falling

    def update(self, new_value: int | float) -> bool:
        new_float = float(new_value)
        old_float = self._value
        self._value = new_float
        if old_float is None:
            return False
        if self.rising and new_float > self._threshold and old_float <= self._threshold:
            return True
        elif self.falling and new_float < self._threshold and old_float >= self._threshold:
            return True
        else:
            return False
