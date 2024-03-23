import argparse
import sys

import typer

from keylight import constants, types


def _normalize(name: str, value: str, min: int, max: int):
    """
    TODO Split normalization from validation and add the following validations:
    * color can only be incremented or decremented >=100
    * both brightness and color cannot be incremented or decremented negative values
    * both brightness and color cannot be incremented more than their max values
    """
    if value is None:
        return types.Direction.ABSOLUTE, None

    try:
        if value.startswith("+"):
            direction = types.Direction.ADD
            number = value[1:]
        elif value.startswith("-"):
            direction = types.Direction.SUBTRACT
            number = value[1:]
        else:
            direction = types.Direction.ABSOLUTE
            number = value
        number = int(number)
    except ValueError:
        print(f"{name} must be in the form '[+-]integer' or 'integer'", file=sys.stderr)
        raise typer.Exit(code=1)

    if direction is types.Direction.ABSOLUTE:
        if number > max:
            print(f"{name} {value} is above the maximum. Setting to {max}.", file=sys.stderr)
            number = max
        if number < min:
            print(f"{name} {value} is below the minimum. Setting to {min}.", file=sys.stderr)
            number = min

    return (direction, number)


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
