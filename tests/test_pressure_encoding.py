"""Bit-pattern documentation tests for the PRESSURE byte.

The PRESSURE dict in parser.py is a flat lookup table of magic numbers.
These tests pin the bit-encoding the table actually implements so that
future contributors can read the rule rather than memorise 25 magic
numbers, and so that any accidental drift in the table is caught.
"""

from __future__ import annotations

import pytest

from oralb_ble.parser import PRESSURE


def decode_pressure_byte(byte: int) -> str:
    """Return the label PRESSURE *should* assign to ``byte`` per the rule.

    Rule
    ----
    Low nibble (``byte & 0x0F``) — button-event field:
        0 or 2  -> no button pressed (fall through to level)
        6       -> "button pressed"
        8 or 10 -> "power button pressed"

    Upper nibble (``byte >> 4``) — pressure-level field, only consulted
    when the low nibble is 0 or 2:
        < 9  -> "normal"
        >= 9 -> "high"
    """
    low = byte & 0x0F
    high = byte >> 4
    if low == 6:
        return "button pressed"
    if low in (8, 10):
        return "power button pressed"
    if low in (0, 2):
        return "high" if high >= 9 else "normal"
    raise AssertionError(f"unknown low-nibble code {low} in byte {byte}")


@pytest.mark.parametrize("byte,label", sorted(PRESSURE.items()))
def test_pressure_entry_matches_documented_encoding(byte: int, label: str) -> None:
    """Every PRESSURE entry must decode per the documented bit-pattern."""
    assert decode_pressure_byte(byte) == label


def test_pressure_button_low_nibbles_are_disjoint() -> None:
    """Button-event low nibbles never overlap pressure-level low nibbles."""
    level_nibbles = {0, 2}
    button_nibbles = {6, 8, 10}
    assert not (level_nibbles & button_nibbles)


def test_pressure_high_threshold_is_upper_nibble_nine() -> None:
    """High-pressure entries all have upper nibble >= 9, normals < 9."""
    for byte, label in PRESSURE.items():
        if (byte & 0x0F) not in (0, 2):
            continue
        upper = byte >> 4
        if label == "high":
            assert upper >= 9, f"expected upper>=9 for high pressure, got byte {byte}"
        elif label == "normal":
            assert upper < 9, f"expected upper<9 for normal pressure, got byte {byte}"
