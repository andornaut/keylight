import enum


class Operation(enum.Enum):
    DECREMENT = enum.auto()
    INCREMENT = enum.auto()
    SET = enum.auto()


class Power(str, enum.Enum):
    on = "on"
    off = "off"
    toggle = "toggle"
