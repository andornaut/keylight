# Keylight

A CLI to control an [Elgato Key Light](https://www.elgato.com/en/gaming/key-light) for Linux, macOS, and Windows.

Leverages the [pyleglight](https://gitlab.com/obviate.io/pyleglight) library.

## Requirements

* Python >= 3.6

## Installation

Keylight can be downloaded from [pypi.org](https://pypi.org/project/keylight/).

```bash
pip3 install keylight
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
  --host HOST           hostname of the Key Light (omit to use auto-discovery)
  --on                  turn the Key Light on
  --off                 turn the Key Light off
```

### Examples

```
$ keylight --brightness 45 --color 5500 --on
Auto-discovering Key Light ...
Connected to: Elgato Light @ 192.168.1.100:9123
Brightness: 45%
Color: 5500k
Turning On

$ keylight --host=keylight --off
Connected to: Elgato Light @ keylight:9123
Turning Off
```

#### Aliases

You may find it convenient to use shell aliases:

```
alias koff='keylight --host keylight --off'
alias kon='keylight --host keylight --on'
```

Example usage:

```
# Turn on and set brightness to 20%
$ kon -b20
Connected to: Elgato Light BW42J1A06055 @ keylight:9123
Brightness: 20%
Turning On
```

## Developing

```bash
poetry shell

poetry build

poetry run keylight --on

poetry version patch
poetry publish
```
