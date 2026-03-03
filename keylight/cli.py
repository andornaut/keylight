import sys
from typing import Optional, Tuple

import typer

from keylight import types


def normalize(name: str, value: Optional[str], min_number: int, max_number: int) -> Tuple[types.Operation, Optional[int]]:
    if value is None:
        return types.Operation.SET, None

    direction, number = _parse_int(name, value)

    if number < 0:
        # This can't currently happen, b/c eg. "--10" will be parsed as a long-arg "--" instead of "decrement by negative 10"
        # Nevertheless, this function should guard against it, b/c the caller could change.
        print(f"{name} must be >=0", file=sys.stderr)
        raise typer.Exit(code=1)
    elif number < min_number:
        if direction is types.Operation.SET:
            print(f"{name}={value} is below the minimum. Setting {name}={min_number}.", file=sys.stderr)
            number = min_number
    elif number > max_number:
        if direction is types.Operation.DECREMENT:
            print(f"{name}={value} is below the minimum. Setting {name}={min_number}.", file=sys.stderr)
            number = min_number
            direction = types.Operation.SET
        else:
            print(f"{name}={value} is above the maximum. Setting {name}={max_number}.", file=sys.stderr)
            number = max_number
            direction = types.Operation.SET

    return (direction, number)


def _parse_int(name: str, value: str) -> Tuple[types.Operation, int]:
    try:
        if value.startswith("+"):
            direction = types.Operation.INCREMENT
            number = value[1:]
        elif value.startswith("-"):
            direction = types.Operation.DECREMENT
            number = value[1:]
        else:
            direction = types.Operation.SET
            number = value
        return direction, int(number)
    except ValueError:
        print(f"{name} must be in the form '[+-]integer' or 'integer'", file=sys.stderr)
        raise typer.Exit(code=1)
