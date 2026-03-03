import dataclasses
import enum
from typing import Optional


class Operation(enum.Enum):
    DECREMENT = enum.auto()
    INCREMENT = enum.auto()
    SET = enum.auto()


@dataclasses.dataclass
class Flags:
    brightness_direction: Operation
    brightness_number: Optional[int]
    color_direction: Operation
    color_number: Optional[int]
    host: Optional[str]
    off: bool
    on: bool
    toggle: bool
    port: int
