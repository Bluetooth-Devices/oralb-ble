# Oral-B GATT characteristics

This page is the companion to
[`oralb_ble.const`](https://github.com/Bluetooth-Devices/oralb-ble/blob/main/src/oralb_ble/const.py)
— it catalogs every GATT characteristic Oral-B brushes expose on their
custom service, what we know about each one, and which are still
awaiting reverse-engineering.

All characteristics live under the vendor service
`a0f0ff00-5047-4d53-8208-4f72616c2d42` (Procter & Gamble). Only the
trailing UUID octets vary, so the table below uses the short
`a0f0ffXX` form. Where a characteristic has a `CHARACTERISTIC_*`
constant in `const.py`, the name is shown verbatim.

Status legend:

- **Wired up** — read or written by `oralb_ble` today (covered by the
  test suite).
- **Documented** — name and payload semantics are known, but no code
  path uses them yet.
- **Unknown** — UUID is reachable, semantics are not yet decoded.

## Wired up

| UUID short | Constant                  | Direction | Payload                                                                                                                                   |
| ---------- | ------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `a0f0ff05` | `CHARACTERISTIC_BATTERY`  | Read      | Single byte, battery percentage (`0`–`100`). Surfaced as the `battery_percent` sensor.                                                    |
| `a0f0ff0b` | `CHARACTERISTIC_PRESSURE` | Read      | Single byte decoded via `ACTIVE_CONNECTION_PRESSURE` (`0`=low, `1`=normal, `2`=high). Surfaced as the `pressure` sensor when GATT-polled. |
| `a0f0ff02` | `CHARACTERISTIC_MODEL`    | Read      | Model identifier. The advertisement payload already exposes the same value in byte 1, so the parser keeps relying on the advertisement.   |

The "wired up" set is intentionally minimal: the BLE advertisement
already carries state, sector, brushing time, mode, and pressure-band
information without a GATT connection (see
[wire format](wire-format.md)). GATT is only opened for values that
cannot ride along on the advertisement.

## Documented but unused

These characteristics are named in `const.py` because their purpose has
been confirmed by upstream reverse-engineering (see references at the
bottom of this page). The parser does not read or write them yet — a
future feature could.

| UUID short | Constant                         | Direction     | Notes                                                                                                                               |
| ---------- | -------------------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `a0f0ff01` | `CHARACTERISTIC_TOOTHBRUSH_ID`   | Read          | Hardware identifier. Useful for distinguishing two brushes of the same model that share a BLE address surfaced via `short_address`. |
| `a0f0ff03` | `CHARACTERISTIC_USER_ID`         | Read / Write  | Active user slot (`1`–`4` on multi-user brushes).                                                                                   |
| `a0f0ff04` | `CHARACTERISTIC_STATUS`          | Read / Notify | Mirrors the toothbrush state byte from the advertisement. Notifications would let a client react without polling.                   |
| `a0f0ff06` | `CHARACTERISTIC_BUTTON`          | Read / Notify | Live button-press telemetry. Maps to the "button pressed" / "power button pressed" labels in `PRESSURE`.                            |
| `a0f0ff07` | `CHARACTERISTIC_MODE`            | Read          | Current cleaning mode. Decoded via `SMART_SERIES_MODES` or `IO_SERIES_MODES` depending on the model line.                           |
| `a0f0ff08` | `CHARACTERISTIC_BRUSHING_TIME`   | Read          | Seconds elapsed in the current session. The advertisement already carries this as `data[5] * 60 + data[6]`.                         |
| `a0f0ff09` | `CHARACTERISTIC_SECTOR`          | Read          | Current sector code, decoded via `SECTOR_MAP`. The advertisement already exposes this as `data[8]`.                                 |
| `a0f0ff21` | `CHARACTERISTIC_CONTROL`         | Write         | Generic control surface (start/stop session, reset). Exact opcodes are not yet pinned down here.                                    |
| `a0f0ff22` | `CHARACTERISTIC_CURRENT_TIME`    | Read / Write  | Wall-clock time on the brush, used to time-stamp session history.                                                                   |
| `a0f0ff25` | `CHARACTERISTIC_AVAILABLE_MODES` | Read          | Bitmask / list of modes the brush actually supports — narrower than the model-wide `SMART_SERIES_MODES` table.                      |
| `a0f0ff26` | `CHARACTERISTIC_SECTOR_TIMER`    | Read          | Per-sector elapsed seconds. The advertisement exposes this as `data[9]`.                                                            |
| `a0f0ff29` | `CHARACTERISTIC_SESSION_INFO`    | Read          | Per-session metadata (start time, duration, mode used). Candidate source for the "well-brushed" sensor proposed in issue #46.       |
| `a0f0ff0d` | `CHARACTERISTIC_POSITION`        | Read / Notify | Suspected to carry positional / orientation data from the IMU. Exact encoding is still unconfirmed — see the comment in `const.py`. |
| `a0f0ff2b` | `CHARACTERISTIC_UNKNOWN_9` ※     | Write         | LED ring colour on IO-Series brushes. Issue #36 captured six 4-byte payloads (white/blue/turquoise/pink/yellow/orange).             |

※ Issue [#36](https://github.com/Bluetooth-Devices/oralb-ble/issues/36)
proposes renaming `CHARACTERISTIC_UNKNOWN_9` to
`CHARACTERISTIC_LED_COLOR` and exporting the payload table.

## Unknown

These characteristics are reachable on at least one Oral-B model but
their payload semantics have not been decoded. They are named
`CHARACTERISTIC_UNKNOWN_*` in `const.py` precisely as placeholders. If
you reverse-engineer one, the workflow is:

1. Capture a `read_gatt_char()` payload from a running brush in a known
   state (idle / brushing / charging / paired with the official app).
2. Diff payloads across states or across the app's user actions.
3. Rename the constant in `const.py` and add a regression test against
   the captured bytes (see `tests/test_const.py` for the shape).

| UUID short | Constant                    | Notes                                                                   |
| ---------- | --------------------------- | ----------------------------------------------------------------------- |
| `a0f0ff81` | `CHARACTERISTIC_UNKNOWN_4`  |                                                                         |
| `a0f0ff82` | `CHARACTERISTIC_UNKNOWN_5`  |                                                                         |
| `a0f0ff83` | `CHARACTERISTIC_UNKNOWN_3`  |                                                                         |
| `a0f0ff84` | `CHARACTERISTIC_UNKNOWN_1`  |                                                                         |
| `a0f0ff85` | `CHARACTERISTIC_UNKNOWN_2`  |                                                                         |
| `a0f0ff0a` | `CHARACTERISTIC_UNKNOWN_7`  | Adjacent to `0x0b` (pressure) — possibly a related telemetry char.      |
| `a0f0ff0c` | _commented out_             | Reads fail on the brushes tested so far — not exposed by all firmwares. |
| `a0f0ff23` | `CHARACTERISTIC_UNKNOWN_10` | Adjacent to `0x22` (current time) — likely related.                     |
| `a0f0ff2a` | `CHARACTERISTIC_UNKNOWN_12` |                                                                         |
| `a0f0ff2c` | `CHARACTERISTIC_UNKNOWN_8`  |                                                                         |
| `a0f0ff2d` | `CHARACTERISTIC_UNKNOWN_11` |                                                                         |

The grouping of UUIDs is not random: the `0x01–0x09` block carries
session-state values (identifier, user, state, battery, button, mode,
brush-time, sector, plus the unknown `0x0a`); the `0x20–0x2D` block
carries control and configuration surfaces (control, current time,
user-id 2, available modes, sector timer, plus the unknown `0x2A`–`0x2D`
and the LED-colour char at `0x2B`); the `0x81–0x85` block is its own
cluster of unknowns. Knowing where a UUID sits in this layout is often
a useful first hint when guessing its purpose.

## References

- Upstream Oral-B protocol notes: <https://github.com/wise86-android/OralBlue_python/blob/15e1a03bcb3350574d438e4593bcff59608a77a7/Protocol.md>
- MatrixEditor model-ID reverse engineering: <https://github.com/MatrixEditor/oralb-io/blob/master/oralb/blesdk/brush.py>
- Issue [#36](https://github.com/Bluetooth-Devices/oralb-ble/issues/36) — LED ring colour control.
- Issue [#46](https://github.com/Bluetooth-Devices/oralb-ble/issues/46) — Brushing-quality sensors (likely sourced from `CHARACTERISTIC_SESSION_INFO`).
