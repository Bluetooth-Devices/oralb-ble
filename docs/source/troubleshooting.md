# Troubleshooting

A field guide to the things people most often hit when integrating
`oralb-ble` — what the symptom means, where to look in the library,
and what to capture before opening an issue.

The companion pages are [usage](usage.md) (sensor semantics, polling
cadence) and [wire-format](wire-format.md) (byte-level layout of the
advertisement). When a symptom traces back to a specific byte or
sensor, those pages explain the wiring; this page explains what to do
about it.

## Symptom: the brush shows up as "Unknown"

`update.title` reads `Unknown <last4>` and the `device_type` is
`"Unknown"`.

What happened: the parser received a valid Oral-B advertisement
(manufacturer id `0x00DC`, length 9 or 11) but byte 1 — the model
identifier — is not in `MODEL_ID_TO_MODEL`. The parser fell back to
`Models.Unknown`, which is mapped to the smart-series mode dictionary.

What to do:

1. Capture an advertisement frame from the brush. Manufacturer key
   `220` (`0x00DC`) is Procter & Gamble's company id — every Oral-B
   payload lives under that key. Home Assistant exposes raw frames
   when the bluetooth manager logger is set to debug; a stand-alone
   capture with `bluetoothctl --monitor` or a BLE sniffer works just
   as well.
2. Read off byte 1 of `manufacturer_data[220]`.
3. Check `MODEL_ID_TO_MODEL` in `src/oralb_ble/parser.py` for the
   closest existing line. If the brush is plausibly a new SKU of an
   existing product (e.g. another IO Series variant), add the byte-1
   value pointing at the existing `Models.X`. If it is genuinely new,
   add a new `Models.X` enum value plus a matching `DEVICE_TYPES`
   row, choosing between `SMART_SERIES_MODES` and `IO_SERIES_MODES`
   based on the brush's mode list. The byte layout you'll be matching
   against lives in [wire-format](wire-format.md).

The misclassification trail is worth scanning before filing a new
issue — past examples like
[#51](https://github.com/Bluetooth-Devices/oralb-ble/issues/51) and
[#65](https://github.com/Bluetooth-Devices/oralb-ble/issues/65)
documented IO Series ids that have since been folded into the table.

## Symptom: state shows as "unknown state N"

The `toothbrush_state` sensor reads `unknown state 7` (or any other
number).

What happened: byte 3 of the advertisement carries a value that is
not in `STATES` (defined in `src/oralb_ble/parser.py`). The parser
returns the literal `f"unknown state {state}"` rather than guessing.

The known set today is:

| Byte value | State            |
| ---------: | ---------------- |
|          0 | `unknown`        |
|          1 | `initializing`   |
|          2 | `idle`           |
|          3 | `running`        |
|          4 | `charging`       |
|          5 | `setup`          |
|          6 | `flight menu`    |
|          8 | `selection menu` |
|          9 | `off`            |
|        113 | `final test`     |
|        114 | `pcb test`       |
|        115 | `sleeping`       |
|        116 | `transport`      |

If you reproduce a missing value reliably, open an issue with the
captured advertisement and a one-line note on what the brush was
physically doing when the value appeared (e.g. "charging on dock, lid
closed"). The diagnostic byte is `data[3]`.

## Symptom: pressure shows as "unknown pressure N"

The `pressure` sensor reads `unknown pressure 42` (or any other
number).

What happened: byte 4 of the advertisement carries a value that is
not in `PRESSURE`. That dictionary is wide because Oral-B encodes
several flags into the same byte — pressure level (low/normal/high),
which button is currently being held, plus some unused high bits.
See the _Pressure byte bit-encoding_ section of
[wire-format](wire-format.md) for the full bit layout.

The shipped `PRESSURE` table enumerates the byte values seen in
practice; firmware revisions occasionally introduce new combinations.
If you reproduce a missing value reliably, open an issue with the
captured byte and the physical state of the brush — was a button
held, which one, and what was the brush head pressure at the time.

Note that `pressure` is double-sourced: the values from
`async_poll()` go through `ACTIVE_CONNECTION_PRESSURE` (`0=low`,
`1=normal`, `2=high`) and never produce an `unknown pressure` label
unless the brush returns a fourth byte value.

## Symptom: sector keeps reading "unknown sector code N"

The `sector` sensor reads `unknown sector code 17` (or similar) while
the brush is `running`.

What happened: byte 8 of the advertisement carries a sector code not
present in `SECTOR_MAP`. The known codes cover the standard four
quadrants plus the post-session `success` marker; multi-sector or
multi-region modes can produce values outside the table.

The mapping today (excerpted from `src/oralb_ble/parser.py`):

| Codes                        | Meaning    |
| ---------------------------- | ---------- |
| `1`, `9`                     | `sector 1` |
| `2`, `10`                    | `sector 2` |
| `3`, `11`, `19`, `27`        | `sector 3` |
| `4`, `7`, `15`, `31`, `39`   | `sector 4` |
| `41`, `42`, `43`, `47`, `55` | `success`  |

If a brush reliably reports an unmapped code, capture the byte 8
value during the session along with `number_of_sectors`
(`data[10]` on length-11 payloads) — the high bits of the code carry
the sector count selector, so a six-sector brush will use codes the
four-sector table does not cover.

## Symptom: sector "freezes" after a session

The `sector` sensor reads `sector 4` (or any value) long after the
brush stopped running.

What happened: this is a firmware quirk. The brush keeps broadcasting
the last visited sector in `data[8]` after the session ends. The
parser detects this and rewrites the sensor to `"no sector"`
whenever `toothbrush_state != "running"`. If you see the sticky
value, the parser thinks the brush is still `running` — check the
state byte. The most common cause is the brush going to `idle` for a
moment and then back to `running` because of motion; another is a
state value the parser sees as `unknown state N` and therefore not
equal to the literal `"running"`.

## Symptom: time never resets between sessions

The `time` sensor shows the previous session's duration even though
no one is brushing.

What happened: the brush keeps reporting the last session's elapsed
time in `data[5] * 60 + data[6]` until a new session starts. The
library reports the brush's own value verbatim. Consumers that want
a clean per-session counter should watch the `brushing` binary
sensor and treat the `False → True` edge as session start, snapshotting
`time` at that moment to use as a baseline.

## Symptom: battery never updates

The `battery_percent` sensor stays at its initial value (or never
appears at all).

What happened: `battery_percent` is **only** populated by
`async_poll()` — there is no battery field in the advertisement
payload. If a caller only feeds advertisements through `update()`,
the battery sensor will never fill in.

What to do:

- Confirm the caller is invoking `async_poll(ble_device)` on the
  cadence `poll_needed()` recommends.
- Check the logs for `WARNING` lines like
  `Reading gatt characters failed with err: ...` or
  `Empty gatt payload while reading characters: ...`. Both are
  handled inside `async_poll()` and surface as warnings instead of
  exceptions, so a caller that ignores logging will not notice the
  failure mode.
- If GATT reads consistently fail, the brush is probably out of
  range or paired exclusively with the official app. The library
  retries via `bleak_retry_connector` but cannot recover from a
  permanent pairing block.

## Symptom: sensors update less often than expected

You feed advertisements continuously but the GATT-derived values
(`battery_percent`, the GATT-form `pressure`) only refresh
occasionally.

What happened: `poll_needed()` returns `True` on a deliberately
slow cadence — every 60 seconds while the brush is actively brushing
or within 120 seconds of the last brushing event, and only every
24 hours otherwise. The defaults live in `src/oralb_ble/const.py` as
`BRUSHING_UPDATE_INTERVAL_SECONDS`, `NOT_BRUSHING_UPDATE_INTERVAL_SECONDS`,
and `TIMEOUT_RECENTLY_BRUSHING`. They are tuned for battery-friendly
Home Assistant polling and are not configurable through the public
API.

If you need a faster cadence, call `async_poll()` directly on your
own schedule rather than relying on `poll_needed()` as the gate.

## Symptom: nothing happens — `update()` returns and no sensors change

You call `parser.update(service_info)` and the resulting
`SensorUpdate` is empty or unchanged.

What happened, in order of likelihood:

1. **Wrong manufacturer key.** The advertisement does not contain
   manufacturer id `0x00DC` (220). `_start_update()` returns early
   without touching any sensor. Confirm the `manufacturer_data` dict
   has key `220`.
2. **Unexpected payload length.** The payload is not 9 or 11 bytes.
   Length-9 payloads are produced by some older firmware variants;
   length-11 is the modern norm. Any other length is silently
   dropped — this protects against truncated or corrupted frames.
   If you need to see why, set `logging.getLogger("oralb_ble").setLevel(logging.DEBUG)` (next section) and look for the
   `Parsing OralB BLE advertisement data:` line that fires _before_
   the length check.
3. **Stale parser instance.** The parser is stateful per device
   (tracking `_brushing` and `_last_brush`). A fresh
   `OralBBluetoothDeviceData()` for every advertisement will not
   misbehave, but it will lose the brushing-session context that
   `poll_needed()` relies on. Keep one parser per address.

## Enabling debug logging

The parser logs to the `oralb_ble` logger at `DEBUG` level. Three
lines fire per advertisement:

```
DEBUG:oralb_ble.parser:Parsing OralB BLE advertisement data: <BluetoothServiceInfo …>
DEBUG:oralb_ble.parser:Parsing Oral-B sensor: <raw bytes>
```

Plus, when `async_poll()` runs:

```
DEBUG:oralb_ble.parser:Polling Oral-B device: <address>
DEBUG:oralb_ble.parser:Successfully read active gatt characters
DEBUG:oralb_ble.parser:Disconnected from active bluetooth client
```

To enable them from Home Assistant, set:

```yaml
logger:
  default: warning
  logs:
    oralb_ble: debug
```

From a standalone Python process:

```python
import logging
logging.getLogger("oralb_ble").setLevel(logging.DEBUG)
```

The first `DEBUG` line is the most useful — it prints the full
`BluetoothServiceInfo` including the raw `manufacturer_data` bytes,
which is exactly what you need to attach to an issue.

## Filing a useful bug report

When the symptoms above point at a parser gap (unknown model,
state, pressure, or sector code), the maintainers need three things
to act on it:

1. **The captured advertisement bytes**, in their raw form. Either
   the Python repr (`b'\x06\x32\x6b\x02\x72…'`), the hex string, or a
   `BluetoothServiceInfo` dump from a debug log line. The byte you
   think is the cause is rarely enough — the full payload often
   reveals that a different byte is the real signal.
2. **What the brush was physically doing** at the time. Charging on
   the dock? Brushing in sector 2 with the pressure sensor lit? Lid
   closed? Battery low? The mapping from byte values to firmware
   state is empirical, and the only way to confirm a guess is to
   correlate it with the brush's observable behaviour.
3. **The brush model and firmware version** if you know it. The
   model name printed on the handle or charger is enough; firmware
   versions are exposed by the official Oral-B app under
   _Settings → My toothbrush_.

Issues that ship all three usually get resolved in a single
round-trip; issues that ship only "my brush shows as Unknown" stall
on requests for more data.
