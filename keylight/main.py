import sys

# https://gitlab.com/obviate.io/pyleglight/
import leglight

from keylight import cli, types


def _connect(host, port):
    return leglight.LegLight(host, port)


def _discover():
    lights = leglight.discover(1)
    if not lights:
        print('Could not find a Key Light', file=sys.stderr)
        exit(1)
    if len(lights) > 1:
        print(f'Found {len(lights)} Key Lights. Using the first.')
    return lights[0]


def _main(flags: types.Flags):
    light = _connect(flags.host, flags.port) if flags.host else _discover()
    print(f'Connected to: {light}')

    if flags.brightness is not None:
        print(f'Brightness: {flags.brightness}')
        light.brightness(flags.brightness)
    if flags.color is not None:
        print(f'Color: {flags.color}')
        light.color(flags.color)
    if flags.on:
        print('Turning On')
        light.on()
    if flags.off:
        print('Turning Off')
        light.off()


def main():
    _main(cli.parse())


if __name__ == '__main__':
    main()
