"""Unit tests for keylight.cli.normalize (no hardware needed)."""

import pytest
import typer

from keylight import cli, constants, types


def test_set_below_minimum_clamps_to_minimum(capsys):
    direction, number = cli.normalize(
        "Color", "100", constants.MIN_COLOR, constants.MAX_COLOR
    )

    assert direction is types.Operation.SET
    assert number == constants.MIN_COLOR
    _, err = capsys.readouterr()
    assert "is below the minimum" in err


def test_decrement_past_minimum_names_the_decrement(capsys):
    # A decrement larger than the whole range (e.g. -150 with max 100)
    # bottoms out at the minimum. The message must describe the decrement,
    # not misreport the input as "below the minimum" (that text belongs to
    # the clamp-a-small-SET-value case above).
    direction, number = cli.normalize(
        "Brightness", "-150", constants.MIN_BRIGHTNESS, constants.MAX_BRIGHTNESS
    )

    assert direction is types.Operation.SET
    assert number == constants.MIN_BRIGHTNESS
    _, err = capsys.readouterr()
    assert "decrements past the minimum" in err
    assert "is below the minimum" not in err


def test_increment_above_maximum_clamps_to_maximum(capsys):
    direction, number = cli.normalize(
        "Brightness", "+150", constants.MIN_BRIGHTNESS, constants.MAX_BRIGHTNESS
    )

    assert direction is types.Operation.SET
    assert number == constants.MAX_BRIGHTNESS
    _, err = capsys.readouterr()
    assert "is above the maximum" in err


@pytest.mark.parametrize("value", ["abc", "1.5", "", "+"])
def test_malformed_value_is_a_clean_error(value, capsys):
    with pytest.raises(typer.Exit) as exc_info:
        cli.normalize(
            "Brightness", value, constants.MIN_BRIGHTNESS, constants.MAX_BRIGHTNESS
        )

    assert exc_info.value.exit_code == 1

    _, err = capsys.readouterr()
    assert "must be in the form" in err
