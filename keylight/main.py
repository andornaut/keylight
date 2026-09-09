import functools
import sys
import textwrap
from typing import Annotated

import leglight
import requests
import typer

from keylight import cli, constants, types

app = typer.Typer(help="A CLI to control an Elgato Key Light", add_completion=False)


def _set_request_timeout():
    # leglight calls requests.get and requests.put without a timeout and offers
    # no way to pass one. requests in turn hands urllib3 an explicit None, which
    # puts the socket in blocking mode and so ignores socket.setdefaulttimeout,
    # leaving these defaults as the only place a timeout can be set. Without one
    # a light that accepts packets but never answers hangs the command.
    requests.get = functools.partial(requests.get, timeout=constants.REQUEST_TIMEOUT)
    requests.put = functools.partial(requests.put, timeout=constants.REQUEST_TIMEOUT)


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
        str | None,
        typer.Option(
            "--brightness",
            "-b",
            help=f"{constants.MIN_BRIGHTNESS} <= BRIGHTNESS <= {constants.MAX_BRIGHTNESS}; "
            "Prefix with +/- to increment/decrement",
        ),
    ] = None,
    color: Annotated[
        str | None,
        typer.Option(
            "--color",
            "-c",
            help=f"{constants.MIN_COLOR} <= COLOR <= {constants.MAX_COLOR}; Prefix with +/- to increment/decrement",
        ),
    ] = None,
    host: Annotated[str | None, typer.Option(help="hostname of the Key Light (omit to use auto-discovery)")] = None,
    power: Annotated[
        types.Power | None,
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

    # Set after the arguments are parsed, so that a usage error does not depend
    # on the network, and before the first request rather than at import.
    _set_request_timeout()

    try:
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
    except requests.exceptions.RequestException as error:
        cli.fail(f"Could not reach the Key Light: {error}")


def main():
    app()


if __name__ == "__main__":
    main()
