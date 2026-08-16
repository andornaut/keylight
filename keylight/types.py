import enum


class Operation(enum.Enum):
    DECREMENT = enum.auto()
    INCREMENT = enum.auto()
    SET = enum.auto()


class Power(enum.StrEnum):
    on = "on"
    off = "off"
    toggle = "toggle"
