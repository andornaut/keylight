import argparse
import sys

import typer

from keylight import constants, types


def _normalize(name: str, value: str, min_number: int, max_number: int):
    if value is None:
        return types.Direction.ABSOLUTE, None

    direction, number = _parse_int(name, value)

    if number < 0:
        # This can't currently happen, b/c eg. "--10" will be parsed as a long-arg "--" instead of "decrement by negative 10"
        # Nevertheless, this function should guard against it, b/c the caller could change.
        print(f"{name} must be >=0", file=sys.stderr)
        raise typer.Exit(code=1)
    elif number < min_number:
        if direction is types.Direction.ABSOLUTE:
            print(f"{name}={value} is below the minimum. Setting {name}={min_number}.", file=sys.stderr)
            number = min_number
    elif number > max_number:
        if direction is types.Direction.DECREMENT:
            print(f"{name}={value} is below the minimum. Setting {name}={min_number}.", file=sys.stderr)
            number = min_number
            direction = types.Direction.ABSOLUTE
        else:
            print(f"{name}={value} is above the maximum. Setting {name}={max_number}.", file=sys.stderr)
            number = max_number
            direction = types.Direction.ABSOLUTE

    return (direction, number)


def _parse_int(name: str, value: str) -> tuple[types.Direction, int]:
    try:
        if value.startswith("+"):
            direction = types.Direction.INCREMENT
            number = value[1:]
        elif value.startswith("-"):
            direction = types.Direction.DECREMENT
            number = value[1:]
        else:
            direction = types.Direction.ABSOLUTE
            number = value
        return direction, int(number)
    except ValueError:
        print(f"{name} must be in the form '[+-]integer' or 'integer'", file=sys.stderr)
        raise typer.Exit(code=1)


def parse() -> types.Flags:
    parser = argparse.ArgumentParser(description="A CLI to control an Elgato Key Light")
    parser.add_argument(
        "-b",
        "--brightness",
        type=str,
        help=f"{constants.MIN_BRIGHTNESS} <= brightness <= {constants.MAX_BRIGHTNESS}",
    )
    parser.add_argument("-c", "--color", type=str, help="2900 <= color temperature <= 7000")
    parser.add_argument("--host", help="hostname of the Key Light (omit to use auto-discovery)")
    power_group = parser.add_mutually_exclusive_group()
    power_group.add_argument("--on", action="store_true", help="turn the Key Light on")
    power_group.add_argument("--off", action="store_true", help="turn the Key Light off")
    power_group.add_argument("--toggle", action="store_true", help="toggle the Key Light on/off")
    args = parser.parse_args()

    (brightness_direction, brightness_number) = _normalize(
        "Brightness",
        args.brightness,
        constants.MIN_BRIGHTNESS,
        constants.MAX_BRIGHTNESS,
    )
    (color_direction, color_number) = _normalize("Color", args.color, constants.MIN_COLOR, constants.MAX_COLOR)
    return types.Flags(
        brightness_direction,
        brightness_number,
        color_direction,
        color_number,
        host=args.host,
        on=args.on,
        off=args.off,
        toggle=args.toggle,
        port=constants.DEFAULT_PORT,
    )
