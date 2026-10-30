"""Read the brushing session history stored on Oral-B iO toothbrushes.

iO brushes keep a ring of recent brushing sessions. A session is fetched by
writing ``02 <index>`` to the control characteristic (ff21) and then reading
the session info characteristic (ff29), which returns a 21 byte record.
Index 0 is the newest session.

Record layout (all values little endian):

======  ===========================================================
Bytes   Meaning
======  ===========================================================
0..3    start time, seconds since 2000-01-01 on the brush clock
4..5    session id (low 13 bits), user id (high 3 bits)
6..7    target time in seconds (low 13 bits), sectors (high 3 bits)
8..9    brushing time in seconds
10..11  time with too much pressure, 0.1 s units
12..13  time with too little pressure, 0.1 s units
14      average pressure, 0.1 N units
15      maximum pressure, 0.1 N units
16      number of too much pressure events
17      number of too little pressure events
18      number of times the brush was switched on
19      brushing mode
20      battery level in percent at the end of the session
======  ===========================================================

Empty slots read as all zeros, all ``0x44`` or with a zero start time.

The brush clock (ff22) uses the same epoch, so the wall clock start of a
session is derived from the difference between the brush clock and the host
clock at the time of the read. The brush clock is never written.

This module is opt in: nothing here runs as part of the passive advertisement
parsing or :meth:`OralBBluetoothDeviceData.async_poll`.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone

from bleak import BLEDevice
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.exc import BleakCharacteristicNotFoundError
from bleak_retry_connector import BleakClientWithServiceCache, establish_connection

from .const import (
    CHARACTERISTIC_ACCESS_CONTROL,
    CHARACTERISTIC_CONTROL,
    CHARACTERISTIC_CURRENT_TIME,
    CHARACTERISTIC_SESSION_INFO,
)

_LOGGER = logging.getLogger(__name__)

BRUSH_EPOCH = datetime(2000, 1, 1, tzinfo=timezone.utc)
IO_SESSION_RECORD_LENGTH = 21

COMMAND_GET_SESSION = 0x02
COMMAND_EXTEND_CONNECTION = bytes([0x31, 0x1E])
ACCESS_CONTROL_UNLOCK = b"MGS"

DEFAULT_MAX_SESSIONS = 30
MAX_SESSION_INDEX = 0xFF
MAX_CONSECUTIVE_EMPTY = 3
# The brush drops idle connections after about 30 seconds.
KEEP_ALIVE_INTERVAL_SECONDS = 10.0


@dataclass(frozen=True)
class BrushingSession:
    """A brushing session read from the brush history."""

    index: int
    device_time: int
    session_id: int
    user_id: int
    target_time: int
    sectors: int
    brushing_time: int
    high_pressure_time: float
    low_pressure_time: float
    average_pressure: float
    max_pressure: float
    high_pressure_count: int
    low_pressure_count: int
    on_count: int
    mode: int
    battery_percent: int
    start: datetime | None = None


def _is_empty_record(data: bytes) -> bool:
    return (
        all(byte == 0x00 for byte in data)
        or all(byte == 0x44 for byte in data)
        or int.from_bytes(data[0:4], "little") == 0
    )


def parse_io_session_record(data: bytes, index: int = 0) -> BrushingSession | None:
    """Parse a 21 byte iO session record.

    Returns None for an empty slot. Raises ValueError if the record does not
    have the iO record length.
    """
    if len(data) != IO_SESSION_RECORD_LENGTH:
        raise ValueError(
            f"Expected a {IO_SESSION_RECORD_LENGTH} byte session record,"
            f" got {len(data)} bytes"
        )
    if _is_empty_record(data):
        return None
    session = int.from_bytes(data[4:6], "little")
    target = int.from_bytes(data[6:8], "little")
    return BrushingSession(
        index=index,
        device_time=int.from_bytes(data[0:4], "little"),
        session_id=session & 0x1FFF,
        user_id=session >> 13,
        target_time=target & 0x1FFF,
        sectors=target >> 13,
        brushing_time=int.from_bytes(data[8:10], "little"),
        high_pressure_time=int.from_bytes(data[10:12], "little") / 10,
        low_pressure_time=int.from_bytes(data[12:14], "little") / 10,
        average_pressure=data[14] / 10,
        max_pressure=data[15] / 10,
        high_pressure_count=data[16],
        low_pressure_count=data[17],
        on_count=data[18],
        mode=data[19],
        battery_percent=data[20],
    )


def device_time_to_datetime(device_time: int, clock_offset: float = 0.0) -> datetime:
    """Convert brush clock seconds to an aware UTC datetime.

    ``clock_offset`` is the host clock minus the brush clock, in seconds.
    """
    return BRUSH_EPOCH + timedelta(seconds=device_time + clock_offset)


def _get_characteristic(
    client: BleakClientWithServiceCache, uuid: str
) -> BleakGATTCharacteristic:
    char = client.services.get_characteristic(uuid)
    if char is None:
        raise BleakCharacteristicNotFoundError(uuid)
    return char


async def _async_read_clock_offset(
    client: BleakClientWithServiceCache,
) -> float | None:
    """Return host clock minus brush clock in seconds, None if unknown."""
    char = client.services.get_characteristic(CHARACTERISTIC_CURRENT_TIME)
    if char is None:
        return None
    payload = await client.read_gatt_char(char)
    host_time = time.time()
    if len(payload) < 4:
        return None
    device_time = int.from_bytes(payload[0:4], "little")
    if device_time == 0:
        return None
    return host_time - (BRUSH_EPOCH.timestamp() + device_time)


async def async_read_io_history(
    ble_device: BLEDevice,
    max_sessions: int = DEFAULT_MAX_SESSIONS,
    newer_than: int | None = None,
) -> list[BrushingSession]:
    """Connect to an iO brush and read its stored brushing sessions.

    Sessions are returned newest first. Reading stops after ``max_sessions``
    sessions, after a few consecutive empty slots, or at the first session
    whose ``device_time`` is not newer than ``newer_than``, which allows
    incremental reads. ``start`` is set when the brush clock could be read.

    The brush only accepts connections while it is awake, for example right
    after a brushing session.
    """
    _LOGGER.debug("Reading session history from %s", ble_device.address)
    client = await establish_connection(
        BleakClientWithServiceCache, ble_device, ble_device.address
    )
    sessions: list[BrushingSession] = []
    try:
        control = _get_characteristic(client, CHARACTERISTIC_CONTROL)
        session_info = _get_characteristic(client, CHARACTERISTIC_SESSION_INFO)
        clock_offset = await _async_read_clock_offset(client)
        if access := client.services.get_characteristic(CHARACTERISTIC_ACCESS_CONTROL):
            await client.write_gatt_char(access, ACCESS_CONTROL_UNLOCK, response=True)
        await client.write_gatt_char(control, COMMAND_EXTEND_CONNECTION, response=True)
        last_keep_alive = time.monotonic()
        empty = 0
        for index in range(MAX_SESSION_INDEX + 1):
            if len(sessions) >= max_sessions or empty >= MAX_CONSECUTIVE_EMPTY:
                break
            if time.monotonic() - last_keep_alive > KEEP_ALIVE_INTERVAL_SECONDS:
                await client.write_gatt_char(
                    control, COMMAND_EXTEND_CONNECTION, response=True
                )
                last_keep_alive = time.monotonic()
            await client.write_gatt_char(
                control, bytes([COMMAND_GET_SESSION, index]), response=True
            )
            payload = bytes(await client.read_gatt_char(session_info))
            session = parse_io_session_record(payload, index)
            if session is None:
                empty += 1
                continue
            empty = 0
            if newer_than is not None and session.device_time <= newer_than:
                break
            if clock_offset is not None:
                session = replace(
                    session,
                    start=device_time_to_datetime(session.device_time, clock_offset),
                )
            sessions.append(session)
    finally:
        await client.disconnect()
        _LOGGER.debug("Disconnected after reading %s sessions", len(sessions))
    return sessions
