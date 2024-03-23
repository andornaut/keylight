import dataclasses
import enum


class Direction(enum.Enum):
    ADD = enum.auto()
    SUBTRACT = enum.auto()
    ABSOLUTE = enum.auto()


@dataclasses.dataclass
class Flags:
    brightness_direction: int
    brightness_number: int
    color_direction: Direction
    color_number: str
    host: str
    off: bool
    on: bool
    toggle: bool
    port: int
