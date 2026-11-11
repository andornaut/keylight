# keylight

[![PyPI](https://img.shields.io/pypi/v/keylight)](https://pypi.org/project/keylight/)
[![Release](https://github.com/andornaut/keylight/actions/workflows/release.yml/badge.svg)](https://github.com/andornaut/keylight/actions/workflows/release.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/license/MIT)

A modern CLI to control [Elgato Key Lights](https://www.elgato.com/p/key-light) across Linux, macOS, and Windows.

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
$ keylight --help
 Usage: keylight [OPTIONS]

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --brightness  -b      <str>            0 <= BRIGHTNESS <= 100; Prefix with   │
│                                        +/- to increment/decrement            │
│ --color       -c      <str>            2900 <= COLOR <= 7000; Prefix with    │
│                                        +/- to increment/decrement            │
│ --host                <str>            hostname of the Key Light (omit to    │
│                                        use auto-discovery)                   │
│ --power       -p      <on|off|toggle>  turn the Key Light on, off, or toggle │
│                                        it                                    │
│ --help                                 Show this message and exit.           │
╰──────────────────────────────────────────────────────────────────────────────╯
```

### Examples

**Auto-discovery and basic control:**

```bash
$ keylight --brightness 45 --color 5500 --power on
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
$ keylight --power toggle
Connected to "Elgato Key Light" at 192.168.1.100:9123
Brightness: 55%
Color temperature: 5500k
On/Off: Off
```

#### Shell Aliases

For quicker access, you can define shell aliases in your `.bashrc` or `.zshrc`:

```bash
alias kon='keylight --power on'
alias koff='keylight --power off'
alias ktoggle='keylight --power toggle'
```

## Developing

Checks require Make and Docker. Project-owned stock image phases live in
`tests/container/`. Native checks use the declared runtime; Markdown and
ShellCheck use separate pinned images. Each phase receives a sanitized source
snapshot and disposable scratch storage.

```bash
make check
poetry run ruff check .
poetry run ruff format --check .
poetry build
```

The full gate runs Ruff, Markdown lint and distribution packaging. No test suite
is declared. Native Poetry commands run on the host; `poetry build` writes distributions under `dist/`.

## Publishing

1. Bump `version` in `pyproject.toml`
2. Commit the change
3. Tag the commit `vX.Y.Z` and push the tag

Pushing the tag is the whole release. The Release workflow runs the checks,
builds the distribution, cuts the GitHub release, and uploads that same sdist
and wheel to PyPI. `poetry publish` is not run by hand.

Nothing here holds a PyPI API token. The workflow authenticates with a
short-lived credential minted from its own OIDC claim, against a trusted
publisher registered on PyPI that names this repository and
`.github/workflows/release.yml`. Renaming that file stops publishing until the
trusted publisher is updated to match.
