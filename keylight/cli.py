import argparse
import sys

from keylight import constants, types


def _normalize(name: str, value: int, min: int, max: int):
    if value is None:
        return None
    if value > max:
        print(f"{name} {value} is above the maximum. Setting to {max}.", file=sys.stderr)
        return max
    if value < min:
        print(f"{name} {value} is below the minimum. Setting to {min}.", file=sys.stderr)
        return min

    return value


def parse() -> types.Flags:
    parser = argparse.ArgumentParser(description="A CLI to control an Elgato Key Light")
    parser.add_argument(
        "-b",
        "--brightness",
        type=int,
        help=f"{constants.MIN_BRIGHTNESS} <= brightness <= {constants.MAX_BRIGHTNESS}",
    )
    parser.add_argument("-c", "--color", type=int, help="2900 <= color temperature <= 6987")
    parser.add_argument("--host", help="hostname of the Key Light (omit to use auto-discovery)")
    power_group = parser.add_mutually_exclusive_group()
    power_group.add_argument("--on", action="store_true", help="turn the Key Light on")
    power_group.add_argument("--off", action="store_true", help="turn the Key Light off")
    power_group.add_argument("--toggle", action="store_true", help="toggle the Key Light on/off")
    args = parser.parse_args()
    return types.Flags(
        brightness=_normalize(
            "Brightness",
            args.brightness,
            constants.MIN_BRIGHTNESS,
            constants.MAX_BRIGHTNESS,
        ),
        color=_normalize("Color", args.color, constants.MIN_COLOR, constants.MAX_COLOR),
        host=args.host,
        on=args.on,
        off=args.off,
        toggle=args.toggle,
        port=constants.DEFAULT_PORT,
    )
