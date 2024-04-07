import dataclasses
import enum


class Direction(enum.Enum):
    ABSOLUTE = enum.auto()
    DECREMENT = enum.auto()
    INCREMENT = enum.auto()


@dataclasses.dataclass
class Flags:
    brightness_direction: Direction
    brightness_number: str
    color_direction: Direction
    color_number: str
    host: str
    off: bool
    on: bool
    toggle: bool
    port: int
