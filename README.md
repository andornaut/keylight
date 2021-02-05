# Keylight

A CLI to control an [Elgato Key Light](https://www.elgato.com/en/gaming/key-light) for Linux and macOS.

Leverages the [pyleglight](https://gitlab.com/obviate.io/pyleglight) library.

## Requirements

* Python >= 3.6

## Installation

Keylight can be downloaded from [pypi.org](https://pypi.org/project/keylight/).

```bash
pip install keylight
```

## Usage

```
$ keylight
usage: keylight [-h] [-b BRIGHTNESS] [-c COLOR] [--host HOST] [--on] [--off]

A CLI to control an Elgato Key Light

optional arguments:
  -h, --help            show this help message and exit
  -b BRIGHTNESS, --brightness BRIGHTNESS
                        0 <= brightness <= 100
  -c COLOR, --color COLOR
                        2900 <= color temperature <= 6987
  --host HOST           Hostname (without the scheme or port) of the Key
                        Light
  --on                  Turn the Key Light on
  --off                 Turn the Key Light off
```

### Examples

```
$ keylight --host=keylight --brightness 25 --color 3500 --on
Connected to: Elgato Light @ keylight:9123
Brightness: 25
Color: 3500
Turning On

$ keylight --off
Connected to: Elgato Light @ 192.168.1.100:9123
Turning Off
```

## Developing

```bash
# Build
pip install --upgrade build
python3 -m build
pip install --upgrade dist/*.whl 

# Publish
pip install twine
twine upload dist/
```
