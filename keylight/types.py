import dataclasses
import enum


class Operation(enum.Enum):
    DECREMENT = enum.auto()
    INCREMENT = enum.auto()
    SET = enum.auto()


@dataclasses.dataclass
class Flags:
    brightness_direction: Operation
    brightness_number: str
    color_direction: Operation
    color_number: str
    host: str
    off: bool
    on: bool
    toggle: bool
    port: int
