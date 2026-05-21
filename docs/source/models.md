# Supported models, modes, and states

This page is a quick reference for the lookup tables that
[`oralb_ble.parser`](https://github.com/Bluetooth-Devices/oralb-ble/blob/main/src/oralb_ble/parser.py)
uses to turn raw bytes from the BLE advertisement into the human-readable
strings exposed on each sensor. It complements [wire format](wire-format.md),
which describes _where_ each byte sits in the payload — this page describes
_what each byte's value means_.

If you are debugging an unknown brush ("why does my D700 show up as
`Unknown`?") or wiring up a new fixture, start here.

## Model lines

The parser groups every brush into one of ten `Models` enum entries.
Eight are real product lines; `Unknown` is the fallback for byte-1
values that are not in `MODEL_ID_TO_MODEL`, and `IOSeries` is the
"generic IO" bucket used when the variant cannot be narrowed down to
IO 4 or IO 5.

| `Models` entry | `device_type` string | Mode dictionary      |
| -------------- | -------------------- | -------------------- |
| `D21`          | Smart Series D21     | `SMART_SERIES_MODES` |
| `D36`          | Triumph D36          | `SMART_SERIES_MODES` |
| `D601`         | Pro Series D601      | `SMART_SERIES_MODES` |
| `D700`         | Smart Series D700    | `SMART_SERIES_MODES` |
| `D701`         | Genius Series D701   | `SMART_SERIES_MODES` |
| `D706`         | Genius X D706        | `SMART_SERIES_MODES` |
| `IOSeries4`    | IO Series 4          | `IO_SERIES_MODES`    |
| `IOSeries5`    | IO Series 5          | `IO_SERIES_MODES`    |
| `IOSeries`     | IO Series            | `IO_SERIES_MODES`    |
| `Unknown`      | Unknown              | `SMART_SERIES_MODES` |

The `device_type` is what appears in the sensor name (e.g. `IO Series 4
A1B2`) — `short_address` is appended at runtime.

## Model identifier byte (byte 1)

Byte 1 of the manufacturer-specific advertisement payload is the
model identifier. The parser maps it through `MODEL_ID_TO_MODEL`;
unmapped values fall back to `Models.Unknown` (which still parses
sector / pressure / state / time, but uses `SMART_SERIES_MODES` to
decode byte 7).

| Byte 1 (dec) | Byte 1 (hex) | Maps to     | Source-of-truth comment |
| -----------: | -----------: | ----------- | ----------------------- |
|            0 |       `0x00` | `D36`       | D36 X_MODE              |
|            1 |       `0x01` | `D36`       | D36 6_MODE              |
|            2 |       `0x02` | `D36`       | D36 5_MODE              |
|           32 |       `0x20` | `D701`      | D701 X_MODE             |
|           33 |       `0x21` | `D701`      | D701 6_MODE             |
|           34 |       `0x22` | `D701`      | D701 5_MODE             |
|           39 |       `0x27` | `D700`      | D700 5_MODE             |
|           40 |       `0x28` | `D700`      | D700 4_MODE             |
|           41 |       `0x29` | `D700`      | D700 6_MODE             |
|           48 |       `0x30` | `IOSeries`  | SONOS X_MODE            |
|           49 |       `0x31` | `IOSeries`  | SONOS IO                |
|           50 |       `0x32` | `IOSeries`  | SONOS IO BIG_TI         |
|           52 |       `0x34` | `IOSeries4` | SONOS GALAXY IO4        |
|           53 |       `0x35` | `IOSeries5` | SONOS GALAXY IO5        |
|           54 |       `0x36` | `IOSeries`  | SONOS EPLATFORM         |
|           64 |       `0x40` | `D21`       | D21 X_MODE              |
|           65 |       `0x41` | `D21`       | D21 4_MODE              |
|           66 |       `0x42` | `D21`       | D21 3_MODE              |
|           67 |       `0x43` | `D21`       | D21 2A_MODE             |
|           68 |       `0x44` | `D21`       | D21 2B_MODE             |
|           69 |       `0x45` | `D21`       | D21 3_MODE_WHITENING    |
|           70 |       `0x46` | `D21`       | D21 1_MODE              |
|           80 |       `0x50` | `D601`      | D601 X_MODE             |
|           81 |       `0x51` | `D601`      | D601 5_MODE             |
|           82 |       `0x52` | `D601`      | D601 4_MODE             |
|           83 |       `0x53` | `D601`      | D601 3A_MODE            |
|           84 |       `0x54` | `D601`      | D601 2A_MODE            |
|           85 |       `0x55` | `D601`      | D601 2B_MODE            |
|           86 |       `0x56` | `D601`      | D601 3B_MODE            |
|           87 |       `0x57` | `D601`      | D601 1_MODE             |
|          112 |       `0x70` | `D706`      | D706 X_MODE             |
|          113 |       `0x71` | `D706`      | D706 6_MODE             |
|          114 |       `0x72` | `D706`      | D706 5_MODE             |
|          117 |       `0x75` | `D706`      | D706 X_MODE_CHINA       |
|          118 |       `0x76` | `D706`      | D706 6_MODE_CHINA       |
|          119 |       `0x77` | `D706`      | D706 5_MODE_CHINA       |

The `*_MODE` suffix encodes the number of cleaning modes the brush
exposes in its UI — this is firmware metadata and is _not_ used by
the parser. Two brushes with the same line but different `*_MODE`
suffixes (e.g. `D700 5_MODE` and `D700 6_MODE`) still decode through
the same `SMART_SERIES_MODES` table; the firmware simply hides modes
the hardware does not support.

> **Adding a new ID**: capture the advertisement, decode byte 1 by
> hand, then add an entry to `MODEL_ID_TO_MODEL`. If the brush ships
> a mode dict that does not match either `SMART_SERIES_MODES` or
> `IO_SERIES_MODES`, add a new `Models` enum value too (and a new
> `ModelDescription` in `DEVICE_TYPES`).

Reference for the byte-1 vocabulary above:
<https://github.com/MatrixEditor/oralb-io/blob/master/oralb/blesdk/brush.py>.

## Mode dictionaries (byte 7)

The Smart Series and IO Series ship completely different mode tables.
Byte 7 of the advertisement is decoded against the dictionary attached
to the brush's `ModelDescription` (see the table at the top of this
page).

| Byte 7 | `SMART_SERIES_MODES` | `IO_SERIES_MODES` |
| -----: | -------------------- | ----------------- |
|      0 | off                  | daily clean       |
|      1 | daily clean          | sensitive         |
|      2 | sensitive            | gum care          |
|      3 | massage              | whiten            |
|      4 | whitening            | intense           |
|      5 | deep clean           | super sensitive   |
|      6 | tongue cleaning      | tongue cleaning   |
|      7 | turbo                | _(not used)_      |
|      8 | _(not used)_         | settings          |
|      9 | _(not used)_         | off               |
|    255 | unknown              | _(not used)_      |

Two consequences worth keeping in mind:

- **Mode `0` is ambiguous** across product lines: on a Smart Series
  brush it means the motor is off, but on an IO Series brush it is
  the default daily-clean program. Always interpret byte 7 in the
  context of the brush's `Models` entry.
- **An unknown byte-7 value** does not fall back to anything — the
  sensor reports the literal string `unknown mode <N>` so the value
  surfaces in Home Assistant for triage rather than being silently
  dropped.

## Toothbrush state (byte 3)

Byte 3 of the advertisement drives both the human-readable
`toothbrush_state` sensor and the `brushing` binary sensor. Only the
value `3` flips the binary sensor on.

| Byte 3 | Meaning        | Notes                                                                             |
| -----: | -------------- | --------------------------------------------------------------------------------- |
|      0 | unknown        | Firmware default before any state is reported.                                    |
|      1 | initializing   | Brush is booting / handshaking with the charger.                                  |
|      2 | idle           | Powered on but not running. Sector is reported as `no sector`.                    |
|      3 | running        | **Actively brushing.** The only state that flips the `brushing` binary sensor on. |
|      4 | charging       | Brush is on the charger.                                                          |
|      5 | setup          | Initial user setup (IO Series).                                                   |
|      6 | flight menu    | Aircraft / transport mode menu (IO Series).                                       |
|      8 | selection menu | Mode selection UI (IO Series).                                                    |
|      9 | off            | Powered down.                                                                     |
|    113 | final test     | Factory diagnostic state.                                                         |
|    114 | pcb test       | Factory diagnostic state.                                                         |
|    115 | sleeping       | Low-power state — still advertises occasionally so battery / sector can refresh.  |
|    116 | transport      | Shipping mode — Bluetooth radio is gated until first charger contact.             |

Unknown values are reported as `unknown state <N>` so they show up in
the sensor (and in user-submitted issues) without crashing the
parser. The `0`, `113`, and `114` states are rarely seen in the wild;
they exist in the parser because upstream documented them.

## Sector codes (byte 8)

The `SECTOR_MAP` table reflects values observed in real captures
across the IO Series and Smart Series. Several bytes map to the same
sector — the firmware appears to use additional high-bit information
that this parser does not need to interpret.

| Byte 8 (dec)       | Decoded  |
| ------------------ | -------- |
| 1, 9               | sector 1 |
| 2, 10              | sector 2 |
| 3, 11, 19, 27      | sector 3 |
| 4, 7, 15, 31, 39   | sector 4 |
| 41, 42, 43, 47, 55 | success  |

When the brush is not in the `running` state, the parser overrides
the sector to `no sector` regardless of what byte 8 contains — the
firmware keeps reporting the last sector during idle / charging,
which would otherwise leave a stale value on the sensor forever.

## See also

- [wire format](wire-format.md) — the per-byte layout of the
  manufacturer payload, and the GATT characteristics used for
  battery and active-connection pressure.
- [`oralb_ble.parser`](https://github.com/Bluetooth-Devices/oralb-ble/blob/main/src/oralb_ble/parser.py)
  — the lookup tables on this page live at module scope and can be
  imported directly if you need them.
