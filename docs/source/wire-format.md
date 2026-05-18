# Oral-B BLE wire format

This page documents the on-the-wire layout that
[`oralb_ble.parser`](https://github.com/Bluetooth-Devices/oralb-ble/blob/main/src/oralb_ble/parser.py)
decodes. It is a developer reference for contributors adding new model
IDs, new fixtures, or new sensors — not a stable public API.

The Oral-B brush is passively discoverable: most data arrives in the BLE
_advertisement payload_ (manufacturer-specific data). A handful of values
(battery percentage, active-connection pressure) are only available by
opening a GATT connection and reading the relevant characteristic.

## Manufacturer-specific advertisement

- **Company identifier**: `0x00DC` (220 decimal) — assigned to "Procter &
  Gamble Company" by the Bluetooth SIG. The parser exposes this as
  `ORALB_MANUFACTURER` in `parser.py`.
- **Payload length**: either **9 or 11 bytes**. Any other length is
  ignored and logged at DEBUG.
  - Length-9 payloads come from older (v1) brushes and omit the
    `sector_timer` and `number_of_sectors` fields.
  - Length-11 payloads are emitted by every protocol version from v2
    onwards (D21/D36/D601/D700/D701/D706 and the IO Series).

The parser indexes the payload as raw bytes. The table below uses
zero-based byte offsets.

| Byte | Field              | Notes                                                                                                             |
| ---: | ------------------ | ----------------------------------------------------------------------------------------------------------------- |
|    0 | Protocol version   | `1` (D36 / Pro 6000), `2` (Triumph v2 / early D36), `3` (D601 / D701), `4` (D700), `6` (IO Series), `7` (IO 4).   |
|    1 | Model identifier   | Looked up in `MODEL_ID_TO_MODEL`. Unknown IDs fall back to `Models.Unknown` (uses `SMART_SERIES_MODES`).          |
|    2 | Reserved           | Not interpreted by this parser. Believed to be firmware/hardware revision.                                        |
|    3 | Toothbrush state   | Decoded via `STATES`. `3` is the only value that means "actively brushing" — drives the `brushing` binary sensor. |
|    4 | Pressure           | Decoded via `PRESSURE`. See [pressure bit-encoding](#pressure-byte-bit-encoding) below.                           |
|    5 | Brush-time minutes | High byte of the elapsed brushing time. Combined with byte 6 as `data[5] * 60 + data[6]` seconds.                 |
|    6 | Brush-time seconds | Low component of the elapsed brushing time, in seconds within the current minute.                                 |
|    7 | Mode               | Decoded via the per-model `modes` dict (`SMART_SERIES_MODES` or `IO_SERIES_MODES`).                               |
|    8 | Sector code        | Decoded via `SECTOR_MAP`. Reported as `"no sector"` whenever the state is not `running`.                          |
|    9 | Sector timer       | Seconds elapsed in the current sector. Present only on length-11 payloads.                                        |
|   10 | Number of sectors  | How many sectors the brush is configured for (commonly `4` or `6`). Present only on length-11 payloads.           |

### Pressure byte bit-encoding

The `PRESSURE` lookup table is not a flat list of magic numbers — it is a
2-D table over two independent fields packed into a single byte:

- **Low nibble** (`pressure & 0x0F`) encodes the button event:
  - `0` or `2` — no button event
  - `6` — brushing-button pressed
  - `8` or `10` — power-button pressed
- **High nibble** (`pressure >> 4`) encodes the pressure level:
  - `< 9` — normal pressure
  - `>= 9` — high pressure

When both a pressure level and a button event are set, the button-event
label wins in the flattened string the parser emits (this is by design —
the active-button label is the more actionable signal for the user).

### Reading an example

A real-world IO Series advertisement looks like this in the test suite
(`ORALB_IO_SERIES_6`):

```python
manufacturer_data = {220: b"\x062k\x02r\x00\x00\x01\x01\x00\x04"}
```

Byte-by-byte:

| Offset | Hex  | Decimal | Decoded                                             |
| -----: | ---- | ------: | --------------------------------------------------- |
|      0 | `06` |       6 | Protocol v6                                         |
|      1 | `32` |      50 | Model `IOSeries` ("SONOS IO BIG_TI")                |
|      2 | `6b` |     107 | Reserved                                            |
|      3 | `02` |       2 | State `idle`                                        |
|      4 | `72` |     114 | Pressure `normal` (high nibble `7`, low nibble `2`) |
|      5 | `00` |       0 | Brush-time minutes                                  |
|      6 | `00` |       0 | Brush-time seconds → 0s elapsed                     |
|      7 | `01` |       1 | Mode `sensitive` (IO Series modes)                  |
|      8 | `01` |       1 | Sector `1` — overridden to `no sector` because idle |
|      9 | `00` |       0 | Sector timer 0s                                     |
|     10 | `04` |       4 | Number of sectors: 4                                |

## GATT characteristics

The advertisement-only path misses battery state and a finer pressure
reading. `OralBBluetoothDeviceData.async_poll()` opens a GATT connection
and reads two characteristics from `const.py`:

| Constant                  | UUID                                   | Payload                                                                   |
| ------------------------- | -------------------------------------- | ------------------------------------------------------------------------- |
| `CHARACTERISTIC_BATTERY`  | `a0f0ff05-5047-4d53-8208-4f72616c2d42` | Single byte: battery percentage (`0`–`100`).                              |
| `CHARACTERISTIC_PRESSURE` | `a0f0ff0b-5047-4d53-8208-4f72616c2d42` | Single byte decoded via `ACTIVE_CONNECTION_PRESSURE` → `low/normal/high`. |

> **Note**: the connected-mode pressure vocabulary
> (`low` / `normal` / `high`) differs from the advertisement-mode
> vocabulary (`normal` / `high` / `button pressed` / `power button
pressed`). Both write to the same `pressure` sensor — the last
> successful read wins.

The remaining UUIDs in `const.py` are catalogued for future
reverse-engineering work; only the two above are wired up today.

## Adding a new model

When a user reports an unknown brush, the workflow is:

1. Capture the advertisement payload (a `manufacturer_data[220]` byte
   string) and add it as a `BluetoothServiceInfo` fixture at the top of
   `tests/test_parser.py`.
2. Decode byte 1 by hand using this document.
3. Add the new identifier to `MODEL_ID_TO_MODEL` in `parser.py`.
4. Pick an existing `Models` entry that matches (line, mode set) — only
   add a brand new `Models` value when the brush ships a mode dict that
   neither `SMART_SERIES_MODES` nor `IO_SERIES_MODES` cover.
5. Write a regression test that asserts `result.devices[None].model`
   matches the expected `device_type`.

## References

- Original parser: <https://github.com/Ernst79/bleparser/blob/c42ae922e1abed2720c7fac993777e1bd59c0c93/package/bleparser/oral_b.py>
- Protocol reverse-engineering notes: <https://github.com/wise86-android/OralBlue_python/blob/15e1a03bcb3350574d438e4593bcff59608a77a7/Protocol.md>
- Model-ID source: <https://github.com/MatrixEditor/oralb-io/blob/master/oralb/blesdk/brush.py>
