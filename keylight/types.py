import dataclasses


@dataclasses.dataclass
class Flags:
    brightness: int
    color: int
    host: str
    off: bool
    on: bool
    port: int
