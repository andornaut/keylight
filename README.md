# keylight

A modern CLI to control [Elgato Key Lights](https://www.elgato.com/en/gaming/key-light) across Linux, macOS, and Windows.

Built with [Typer](https://typer.tiangolo.com/) and powered by the [pyleglight](https://gitlab.com/obviate.io/pyleglight) library.

## Requirements

* Python ~3.12

## Installation

Install `keylight` via `pip` or [pipx](https://github.com/pypa/pipx) (recommended for CLIs):

```bash
pipx install keylight
```

## Usage

```text
Usage: keylight [OPTIONS]

Options:
  -b, --brightness TEXT  0 <= BRIGHTNESS <= 100; Prefix with +/- to increment/decrement
  -c, --color TEXT       2900 <= COLOR <= 7000; Prefix with +/- to increment/decrement
  --host TEXT            hostname of the Key Light (omit to use auto-discovery)
  --on                   turn the Key Light on
  --off                  turn the Key Light off
  --toggle               toggle the Key Light on/off
  --help                 Show this message and exit.
```

### Examples

**Auto-discovery and basic control:**

```bash
$ keylight --brightness 45 --color 5500 --on
Connected to "Elgato Key Light" at 192.168.1.100:9123
Brightness: 45%
Color temperature: 5500k
On/Off: On
```

**Direct host connection and relative adjustments:**

```bash
$ keylight --host 192.168.1.105 --brightness +10
Connected to "Elgato Key Light Air" at 192.168.1.105:9123
Brightness: 55%
Color temperature: 5500k
On/Off: On
```

**Toggling power:**

```bash
$ keylight --toggle
Connected to "Elgato Key Light" at 192.168.1.100:9123
Brightness: 55%
Color temperature: 5500k
On/Off: Off
```

#### Shell Aliases

For quicker access, you can define shell aliases in your `.bashrc` or `.zshrc`:

```bash
alias kon='keylight --on'
alias koff='keylight --off'
alias ktoggle='keylight --toggle'
```

## Development

`keylight` uses [Poetry](https://python-poetry.org/) for dependency management and packaging.

```bash
# Enter the virtual environment
poetry shell

# Run the CLI during development
poetry run keylight --help

# Lint and format
poetry run ruff check .

# Build and publish
poetry build
poetry publish
```
