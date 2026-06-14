import sys
import textwrap
from typing import Annotated, Optional

import leglight
import typer

from keylight import cli, constants, types

app = typer.Typer(help="A CLI to control an Elgato Key Light", add_completion=False)


def _connect(host, port):
    return leglight.LegLight(host, port)


def _discover():
    lights = leglight.discover(constants.DISCOVERY_TIMEOUT)
    if not lights:
        cli.fail("Could not find a Key Light")
    if len(lights) > 1:
        print(f"Found {len(lights)} Key Lights. Using the first.", file=sys.stderr)
    return lights[0]


@app.command()
def run(
    brightness: Annotated[
        Optional[str],
        typer.Option(
            "--brightness",
            "-b",
            help=f"{constants.MIN_BRIGHTNESS} <= BRIGHTNESS <= {constants.MAX_BRIGHTNESS}; Prefix with +/- to increment/decrement",
        ),
    ] = None,
    color: Annotated[
        Optional[str],
        typer.Option(
            "--color",
            "-c",
            help=f"{constants.MIN_COLOR} <= COLOR <= {constants.MAX_COLOR}; Prefix with +/- to increment/decrement",
        ),
    ] = None,
    host: Annotated[Optional[str], typer.Option(help="hostname of the Key Light (omit to use auto-discovery)")] = None,
    power: Annotated[
        Optional[types.Power],
        typer.Option("--power", "-p", help="turn the Key Light on, off, or toggle it"),
    ] = None,
):
    (brightness_direction, brightness_number) = cli.normalize(
        "Brightness",
        brightness,
        constants.MIN_BRIGHTNESS,
        constants.MAX_BRIGHTNESS,
    )
    (color_direction, color_number) = cli.normalize(
        "Color",
        color,
        constants.MIN_COLOR,
        constants.MAX_COLOR,
    )

    light = _connect(host, constants.DEFAULT_PORT) if host else _discover()
    print(f'Connected to "{light.productName}" at {light.address}:{light.port}')

    if brightness_number is not None:
        if brightness_direction is types.Operation.INCREMENT:
            light.incBrightness(brightness_number)
        elif brightness_direction is types.Operation.DECREMENT:
            light.decBrightness(brightness_number)
        else:
            light.brightness(brightness_number)

    if color_number is not None:
        if color_direction is types.Operation.INCREMENT:
            light.incColor(color_number)
        elif color_direction is types.Operation.DECREMENT:
            light.decColor(color_number)
        else:
            light.color(color_number)

    if power is types.Power.on:
        light.on()
    elif power is types.Power.off:
        light.off()
    elif power is types.Power.toggle:
        light.off() if light.isOn else light.on()

    print(
        textwrap.dedent(
            f"""\
        Brightness: {light.isBrightness}%
        Color temperature: {light.isTemperature:.0f}k
        On/Off: {"On" if light.isOn else "Off"}"""
        )
    )


def main():
    app()


if __name__ == "__main__":
    main()
