# Adding a new toothbrush model

This is a contributor walk-through for teaching the parser about an
Oral-B brush it doesn't yet recognise (typical symptom: the device
shows up as `Unknown` in Home Assistant even though it's clearly
broadcasting Oral-B manufacturer data).

The companion to this page is [wire-format](wire-format.md), which
documents the byte-level layout of the advertisement payload, plus
`src/oralb_ble/parser.py` itself for the current `Models`,
`MODEL_ID_TO_MODEL`, and mode dicts. Skim both before starting — most
"new" brushes turn out to be an unrecognised **model id** for a
protocol the parser already speaks, so the change boils down to one
table entry plus a test fixture.

## 1. Capture an advertisement

You need at least one real advertisement frame from the brush.
Two practical sources:

- **Home Assistant** Bluetooth debug logs, with
  `logger: homeassistant.components.bluetooth.manager: debug` set.
  Look for lines like:

  ```
  AdvertisementData(manufacturer_data={220: b'\x06\x32\x6b\x02\x72\x00\x00\x01\x01\x00\x04'}, rssi=-63)
  ```

  Manufacturer key `220` is `0x00DC` — Procter & Gamble's company id,
  exposed by the parser as `ORALB_MANUFACTURER`.

- **`bluetoothctl --monitor`** on Linux, or any BLE sniffer that
  dumps raw manufacturer data.

You want to capture **both states** if you can: one frame while the
brush is idle (state byte `2`), and one while it's actively brushing
(state byte `3`). The brushing frame is the one that exercises sector
decoding, so test coverage is meaningfully better when both are
present.

## 2. Read off the protocol and model bytes

Index the captured payload as raw bytes (zero-based). The two bytes
that matter for adding a new model are:

| Byte | Field            | Notes                                                            |
| ---: | ---------------- | ---------------------------------------------------------------- |
|    0 | Protocol version | Determines the per-byte layout. The parser already supports 1–7. |
|    1 | Model identifier | What you look up in `MODEL_ID_TO_MODEL`.                         |

If byte 0 is in the range `1–7` and the overall payload length is
**9 or 11 bytes**, the existing parser will handle the frame end-to-end
— you only need to teach it the new byte-1 value. Any other length is
silently dropped, and a brand-new protocol version would need real
reverse-engineering work that is out of scope for this guide.

See [wire-format](wire-format.md) for what bytes 2–10 mean.

## 3. Pick (or add) a `Models` enum value

`src/oralb_ble/parser.py` defines a `Models` enum and a `DEVICE_TYPES`
dict that maps each enum to a human-readable name and a mode dict.

- **If the brush is a new SKU of an existing product line** (e.g.
  another D700 variant, another IO Series), reuse the existing
  `Models.X` — the only required change is a new row in
  `MODEL_ID_TO_MODEL`.
- **If it is a genuinely new product line**, add a new `Models.X`
  entry, then a matching row in `DEVICE_TYPES` choosing between
  `SMART_SERIES_MODES` and `IO_SERIES_MODES` based on the brush's
  actual mode list. Mode `0` is the canonical "is this Smart Series or
  IO Series?" tell: Smart Series uses `0 = "off"`, IO Series uses
  `0 = "daily clean"`. Watching the brush's display while cycling
  modes is the fastest way to be sure.

## 4. Wire the model id

Add a row to `MODEL_ID_TO_MODEL` in `parser.py`:

```python
MODEL_ID_TO_MODEL: dict[int, Models] = {
    ...
    # D706 line (Genius X)
    112: Models.D706,
    113: Models.D706,
    ...
    # Your new id here:
    250: Models.YourModel,  # <human-readable suffix from firmware>
}
```

The trailing comment after each row is firmware metadata
(`X_MODE` / `6_MODE` / `CHINA` / …) — it has no behavioural effect on
the parser but is useful when grepping for a specific SKU later.
Keep ids grouped by product line in numeric order so future readers
can spot conflicts at a glance.

## 5. Add a fixture and a regression test

Tests in `tests/test_parser.py` follow a consistent shape: a top-level
`BluetoothServiceInfo` fixture for the raw advertisement, and a
`test_<descriptive_name>` function that calls
`OralBBluetoothDeviceData().update(service_info)` and asserts the full
expected `SensorUpdate`.

Fixture template (drop next to the existing ones, near the top of the
file):

```python
ORALB_MY_NEW_BRUSH = BluetoothServiceInfo(
    name="78:DB:2F:C2:48:BE",
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    manufacturer_data={220: b"<raw bytes you captured>"},
    service_uuids=[],
    service_data={},
    source="local",
)
```

Test template (compare against any existing `test_io_series_*` for a
copy-pasteable starting point — the assertion blocks are mechanical
once you know the model name, mode, state, sector, and brush-time):

```python
def test_my_new_brush():
    parser = OralBBluetoothDeviceData()
    result = parser.update(ORALB_MY_NEW_BRUSH)
    assert result.title == "My Model Name 48BE"
    assert result.devices[None].model == "My Model Name"
    # ...assert on the entity_values you expect for this fixture...
```

If you don't want to hand-write the full `entity_descriptions` /
`entity_values` blocks, the pragmatic shortcut is: run the test once
with a minimal `result == SensorUpdate(...)` assertion, copy the
`AssertionError` diff into the test, and tweak any fields that are
genuinely wrong (rather than just unexpected). Most existing tests
were grown this way.

## 6. Run the suite

```bash
poetry run pytest
```

A passing run of the existing 40-plus parser tests plus your new one
is what gets merged — there is no separate "fixture" or "model
registry" check.

## 7. Open the PR

Title it after the brush, e.g. `feat(parser): recognise Oral-B
<model> (id <NN>)`. Link the original Home Assistant issue or forum
thread where the unrecognised advertisement was reported, paste the
raw captured frame, and call out whether you reused an existing
`Models.X` or added a new one — that single sentence is what reviewers
look for first.

## Common gotchas

- **The `Unknown` fallback is silent.** A brush with an unmapped
  model id parses fine, just under `Models.Unknown` /
  `"Unknown"` / `SMART_SERIES_MODES`. The integration won't crash;
  the user just sees the wrong product name and possibly wrong mode
  strings. A test that asserts on `model == "Unknown"` is the
  cheapest way to lock in the current behaviour before you change it.
- **Mode lookup is per-model, not global.** Mode `2` is `"sensitive"`
  on Smart Series and `"gum care"` on IO Series. Picking the wrong
  mode dict in `DEVICE_TYPES` is the single most common subtle bug
  when adding a new model.
- **State `3` is the only "actively brushing" value.** Sectors are
  forced to `"no sector"` whenever the state byte is anything else —
  this is intentional, so the sensor doesn't get stuck on the last
  reported sector during idle / charging.
- **`MODEL_ID_TO_MODEL` is sparse.** Missing numeric ids are
  intentional — only ids actually emitted by real firmware are
  listed. Don't fill the gaps "to be safe"; an entry without a real
  captured fixture is a guess waiting to bite.
