import sys
import textwrap

# Ignore warning:
# /opt/homebrew/lib/python3.9/site-packages/zeroconf/_services/browser.py:169:
# FutureWarning: <leglight.discovery.discover.<locals>.thelistener object at 0x101e15a00>
# has no update_service method. Provide one (it can be empty if you don't care about the updates),
# it'll become mandatory.
# https://stackoverflow.com/a/14463362
import warnings

import leglight

# https://gitlab.com/obviate.io/pyleglight/
from keylight import cli, types

warnings.filterwarnings("ignore")


def _connect(host, port):
    return leglight.LegLight(host, port)


def _discover():
    lights = leglight.discover(1)
    if not lights:
        print("Could not find a Key Light", file=sys.stderr)
        exit(1)
    if len(lights) > 1:
        print(f"Found {len(lights)} Key Lights. Using the first.")
    return lights[0]


def _main(flags: types.Flags):
    light = _connect(flags.host, flags.port) if flags.host else _discover()
    print(f'Connected to "{light.productName}" at {light.address}:{light.port}')

    if flags.brightness_number is not None:
        if flags.brightness_direction is types.Direction.INCREMENT:
            light.incBrightness(flags.brightness_number)
        elif flags.brightness_direction is types.Direction.DECREMENT:
            light.decBrightness(flags.brightness_number)
        else:
            light.brightness(flags.brightness_number)
    if flags.color_number is not None:
        if flags.color_direction is types.Direction.INCREMENT:
            light.incColor(flags.color_number)
        elif flags.color_direction is types.Direction.DECREMENT:
            light.decColor(flags.color_number)
        else:
            light.color(flags.color_number)
    if flags.on:
        light.on()
    if flags.off:
        light.off()
    if flags.toggle:
        if light.isOn:
            light.off()
        else:
            light.on()
    print(
        textwrap.dedent(
            f"""\
        Brightness: {light.isBrightness}%
        Color temperature: {light.isTemperature:.0f}k
        On/Off: {"On" if light.isOn else "Off"}"""
        )
    )


def main():
    _main(cli.parse())


if __name__ == "__main__":
    main()
