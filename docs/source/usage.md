# Usage

`oralb-ble` is a **passive parser** for Oral-B toothbrush BLE
advertisements, with an optional active path that opens a GATT
connection to pull battery percentage and a finer pressure reading.
This page documents both modes, the sensors the library exposes, and
the brushing-session lifecycle the parser tracks.

For the byte-level layout of every advertisement field, see
[Wire format](wire-format.md).

## Installation

```bash
pip install oralb-ble
```

The package targets Python 3.11+ and depends on `bleak`,
`bleak-retry-connector`, `bluetooth-data-tools`,
`bluetooth-sensor-state-data`, and `home-assistant-bluetooth`.

## Passive mode (advertisement parsing)

The brush broadcasts manufacturer-specific data while idle, while
brushing, and for a short window afterwards. No connection is required
to read sensor state — feed each captured advertisement into
[`OralBBluetoothDeviceData.update()`][parser] and read the resulting
`SensorUpdate`.

```python
from home_assistant_bluetooth import BluetoothServiceInfo
from oralb_ble import OralBBluetoothDeviceData

service_info = BluetoothServiceInfo(
    name="Oral-B Toothbrush",
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    manufacturer_data={220: b"\x062k\x02r\x00\x00\x01\x01\x00\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)

parser = OralBBluetoothDeviceData()
update = parser.update(service_info)

print(update.title)
# IO Series 48BE

for key, value in update.entity_values.items():
    print(f"{key.key}: {value.native_value}")
# time: 0
# sector: no sector
# number_of_sectors: 4
# sector_timer: 0
# toothbrush_state: idle
# pressure: normal
# mode: sensitive
# signal_strength: -63

for key, value in update.binary_entity_values.items():
    print(f"{key.key}: {value.native_value}")
# brushing: False
```

The parser is **stateful per device** — keep the same
`OralBBluetoothDeviceData` instance across advertisements from a given
toothbrush. State the parser tracks internally:

- `_brushing` — whether the last advertisement reported state `running`.
- `_last_brush` — `time.monotonic()` of the most recent `running`
  advertisement, used by `poll_needed` (see _Deciding when to poll_
  below).

## Sensors exposed

Every advertisement update writes the values below. Names are the
`key` field on each `DeviceKey`; they match `OralBSensor` /
`OralBBinarySensor` string enum values.

| Sensor              | Type | Source          | Notes                                                                                                                                            |
| ------------------- | ---- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `signal_strength`   | int  | RSSI            | Filled in by `bluetooth_sensor_state_data` from the `BluetoothServiceInfo`. Unit: dBm. Device class: `signal_strength`.                          |
| `time`              | int  | ad bytes        | Elapsed brushing time in seconds (`data[5] * 60 + data[6]`). Resets to `0` on a fresh session; the brush keeps reporting it after stop.          |
| `sector`            | str  | ad bytes        | Decoded via `SECTOR_MAP` (`"sector 1"`–`"sector 4"`, `"success"`, or `"unknown sector code N"`). Overridden to `"no sector"` whenever idle.      |
| `number_of_sectors` | int  | ad bytes        | Configured sector count (commonly `4` or `6`). Only present on length-11 payloads.                                                               |
| `sector_timer`      | int  | ad bytes        | Seconds elapsed in the current sector. Resets when the brush moves to the next sector. Only present on length-11 payloads.                       |
| `toothbrush_state`  | str  | ad bytes        | Decoded via `STATES` — `idle`, `running`, `charging`, `setup`, `sleeping`, `transport`, `final test`, etc. `running` drives the `brushing` flag. |
| `pressure`          | str  | ad bytes / GATT | `normal`, `high`, `button pressed`, or `power button pressed` from the advertisement; or `low`/`normal`/`high` if `async_poll()` ran last.       |
| `mode`              | str  | ad bytes        | Decoded via the per-model mode dict (`SMART_SERIES_MODES` for D-line, `IO_SERIES_MODES` for the IO Series).                                      |
| `battery_percent`   | int  | GATT            | Integer 0–100. Populated only after a successful `async_poll()`. Device class: `battery`. Unit: `%`.                                             |
| `brushing` (binary) | bool | ad bytes        | `True` exactly when `toothbrush_state == "running"`. Drives the `_brushing` / `_last_brush` book-keeping the poll scheduler reads.               |

A few footguns worth knowing:

- **`sector` while idle is sticky in firmware.** The brush keeps
  broadcasting the last visited sector after a session ends. The parser
  rewrites it to `"no sector"` whenever the state is not `running` to
  avoid stale UI.
- **`time` does not reset between sessions.** The brush keeps the last
  session's elapsed time visible until it actually starts the next run.
  Consumers that need a clean "this session" counter should watch for
  the `idle → running` transition.
- **`pressure` is double-sourced.** Advertisements report
  `normal / high / button pressed / power button pressed`. The GATT
  read reports `low / normal / high`. Both write to the same sensor,
  so the most recent successful read wins. See the _Pressure byte
  bit-encoding_ section of [Wire format](wire-format.md) for the bit
  layout used in the advertisement variant.

## Brushing-session lifecycle

A typical brushing session traces this state path:

```
idle ──▶ running ──▶ running ──▶ ... ──▶ idle
            │                       │
            └─ time, sector_timer,  └─ sector → "no sector"
               sector advance         time keeps last value
               while running          until next run starts
```

While `running`, each advertisement carries:

- monotonically increasing `time` (in seconds)
- `sector` cycling 1 → 2 → 3 → 4 → `success` on the four-sector
  cadence; `sector_timer` rises within each sector and resets at the
  boundary
- `mode` reflecting the user-selected program (model-dependent)
- `pressure` updating to `high` when the brush detects too much force

When the user lifts the brush, the state returns to `idle` and the
binary sensor `brushing` flips back to `False`. Time and number of
sectors stay at their last advertised values until the next session
starts.

> What the library does **not** synthesize today: a post-session
> coverage score, per-sector durations across a finished session, or
> historical brushing data. Issue
> [#46](https://github.com/Bluetooth-Devices/oralb-ble/issues/46)
> tracks the brushing-result feature; the GATT characteristics that
> would carry that data (e.g. `CHARACTERISTIC_SESSION_INFO`,
> `CHARACTERISTIC_BRUSHING_TIME`) are catalogued in `const.py` but not
> yet wired up.

## Active mode (GATT polling)

`async_poll(ble_device)` opens a connection and reads two
characteristics:

| Constant                  | UUID                                   | Decoded as                                    |
| ------------------------- | -------------------------------------- | --------------------------------------------- |
| `CHARACTERISTIC_BATTERY`  | `a0f0ff05-5047-4d53-8208-4f72616c2d42` | Single byte → `battery_percent` (0–100).      |
| `CHARACTERISTIC_PRESSURE` | `a0f0ff0b-5047-4d53-8208-4f72616c2d42` | Single byte → `pressure` (`low/normal/high`). |

```python
import asyncio
from bleak import BLEDevice
from oralb_ble import OralBBluetoothDeviceData

async def poll(parser: OralBBluetoothDeviceData, device: BLEDevice):
    update = await parser.async_poll(device)
    for key, value in update.entity_values.items():
        print(f"{key.key}: {value.native_value}")

asyncio.run(poll(parser, ble_device))
```

`async_poll` swallows two failure modes so they don't propagate as
unhandled exceptions:

- `BleakError` — the connection failed or the read errored. Logged at
  `WARNING`; the `SensorUpdate` still returns with whatever state was
  already known.
- `IndexError` — an empty payload came back from a successful read.
  Also logged at `WARNING`; protects against a `pressure_payload[0]`
  on a zero-byte buffer.

Connections always close in a `finally` block, even if the read failed.

### Deciding when to poll

For most callers a passive listener is enough — battery and the
finer pressure value are the only fields polling adds, and battery
moves slowly. The library offers
`poll_needed(service_info, last_poll)` as the canonical heuristic:

- If `last_poll is None`, poll. (First time.)
- If the brush is currently `running`, or finished brushing within the
  last `TIMEOUT_RECENTLY_BRUSHING` seconds (120s by default), use the
  short interval (`BRUSHING_UPDATE_INTERVAL_SECONDS`, 60s).
- Otherwise use the long interval
  (`NOT_BRUSHING_UPDATE_INTERVAL_SECONDS`, 24h).
- Return `True` only when `last_poll` exceeds the chosen interval.

The thresholds live in `oralb_ble.const`; they're tuned for Home
Assistant's polling cadence and shouldn't normally need overriding.

## Supported models

The parser maps `data[1]` to a `Models` enum value; unknown ids fall
back to `Models.Unknown` with the smart-series mode dictionary. The
full coverage today:

- **D-line (older smart brushes)** — Triumph D36, Smart Series D21,
  Pro D601, Smart Series D700, Genius D701, Genius X D706.
- **IO Series** — IO Series 4, IO Series 5, and a generic IO Series
  fallback for unrecognised IO model ids (issues
  [#51](https://github.com/Bluetooth-Devices/oralb-ble/issues/51) and
  [#65](https://github.com/Bluetooth-Devices/oralb-ble/issues/65)
  document specific misclassifications that have since been folded
  into the map).

When a user reports an unrecognised brush, follow the _Adding a new
model_ workflow in [Wire format](wire-format.md) to add a fixture and
an entry to `MODEL_ID_TO_MODEL`.

## Home Assistant integration

The primary consumer of this library is Home Assistant's
[Bluetooth integration][ha-bluetooth]. The integration handles
advertisement capture, calls `update()` on each new advertisement, and
calls `async_poll()` on the cadence `poll_needed()` recommends.
Out-of-tree consumers that want the same behaviour can replicate that
loop directly against `bleak` (see the
[bleak documentation][bleak-scan] for advertisement scanning).

[parser]: https://github.com/Bluetooth-Devices/oralb-ble/blob/main/src/oralb_ble/parser.py
[ha-bluetooth]: https://www.home-assistant.io/integrations/bluetooth/
[bleak-scan]: https://bleak.readthedocs.io/en/latest/scanning.html
