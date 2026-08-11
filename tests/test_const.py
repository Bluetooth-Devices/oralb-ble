from __future__ import annotations

from oralb_ble import CHARACTERISTIC_LED_COLOR, LED_COLORS


def test_led_color_characteristic_uuid() -> None:
    assert CHARACTERISTIC_LED_COLOR == "a0f0ff2b-5047-4d53-8208-4f72616c2d42"


def test_led_colors_payloads() -> None:
    assert LED_COLORS == {
        "white": b"\x44\xcf\x63\x00",
        "blue": b"\x0f\x5b\xcc\x00",
        "turquoise": b"\x00\xff\x3d\x00",
        "pink": b"\xb2\x09\x1a\x00",
        "yellow": b"\x80\xff\x00\x00",
        "orange": b"\xfc\x70\x00\x00",
    }
    for payload in LED_COLORS.values():
        assert len(payload) == 4
        assert payload[3] == 0x00
