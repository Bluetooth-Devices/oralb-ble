from __future__ import annotations

import struct
from datetime import datetime, timezone
from unittest import mock

import pytest
from bleak.exc import BleakCharacteristicNotFoundError

from oralb_ble import (
    BrushingSession,
    async_read_io_history,
    device_time_to_datetime,
    parse_io_session_record,
)
from oralb_ble.const import (
    CHARACTERISTIC_ACCESS_CONTROL,
    CHARACTERISTIC_CONTROL,
    CHARACTERISTIC_CURRENT_TIME,
    CHARACTERISTIC_SESSION_INFO,
)


def make_record(
    device_time: int,
    session_id: int = 1,
    user_id: int = 0,
    target_time: int = 120,
    sectors: int = 4,
    brushing_time: int = 125,
    high_pressure: int = 35,
    low_pressure: int = 12,
    average_pressure: int = 15,
    max_pressure: int = 31,
    high_pressure_count: int = 2,
    low_pressure_count: int = 1,
    on_count: int = 1,
    mode: int = 0,
    battery: int = 80,
) -> bytes:
    """Build a synthetic 21 byte iO session record."""
    return struct.pack(
        "<IHHHHHBBBBBBB",
        device_time,
        (user_id << 13) | session_id,
        (sectors << 13) | target_time,
        brushing_time,
        high_pressure,
        low_pressure,
        average_pressure,
        max_pressure,
        high_pressure_count,
        low_pressure_count,
        on_count,
        mode,
        battery,
    )


def test_parse_io_session_record() -> None:
    record = make_record(
        device_time=1000,
        session_id=42,
        user_id=1,
        mode=0x0B,
    )
    assert len(record) == 21
    assert parse_io_session_record(record, 3) == BrushingSession(
        index=3,
        device_time=1000,
        session_id=42,
        user_id=1,
        target_time=120,
        sectors=4,
        brushing_time=125,
        high_pressure_time=3.5,
        low_pressure_time=1.2,
        average_pressure=1.5,
        max_pressure=3.1,
        high_pressure_count=2,
        low_pressure_count=1,
        on_count=1,
        mode=0x0B,
        battery_percent=80,
    )


@pytest.mark.parametrize(
    "record",
    [
        pytest.param(bytes(21), id="zeros"),
        pytest.param(bytes([0x44] * 21), id="filler"),
        pytest.param(make_record(device_time=0), id="zero_time"),
    ],
)
def test_parse_io_session_record_empty(record: bytes) -> None:
    assert parse_io_session_record(record) is None


@pytest.mark.parametrize("length", [16, 20, 22])
def test_parse_io_session_record_wrong_length(length: int) -> None:
    with pytest.raises(ValueError):
        parse_io_session_record(bytes([1] * length))


def test_device_time_to_datetime() -> None:
    assert device_time_to_datetime(0) == datetime(2000, 1, 1, tzinfo=timezone.utc)
    assert device_time_to_datetime(86400, clock_offset=60) == datetime(
        2000, 1, 2, 0, 1, tzinfo=timezone.utc
    )


def _mock_client(
    records: list[bytes],
    clock: bytes | None = struct.pack("<I", 2000),
    with_access_control: bool = True,
) -> mock.Mock:
    """Return a mock client that serves records by the requested index."""
    client = mock.AsyncMock()
    chars = {
        CHARACTERISTIC_CONTROL: mock.Mock(name="control"),
        CHARACTERISTIC_SESSION_INFO: mock.Mock(name="session_info"),
    }
    if clock is not None:
        chars[CHARACTERISTIC_CURRENT_TIME] = mock.Mock(name="clock")
    if with_access_control:
        chars[CHARACTERISTIC_ACCESS_CONTROL] = mock.Mock(name="access")
    client.services = mock.Mock()
    client.services.get_characteristic = mock.Mock(side_effect=chars.get)
    selected = {"index": 0}

    async def _write(char, data, response=False):
        if char is chars[CHARACTERISTIC_CONTROL] and data[0] == 0x02:
            selected["index"] = data[1]

    async def _read(char):
        if char is chars.get(CHARACTERISTIC_CURRENT_TIME):
            return bytearray(clock or b"")
        index = selected["index"]
        return bytearray(records[index] if index < len(records) else bytes(21))

    client.write_gatt_char.side_effect = _write
    client.read_gatt_char.side_effect = _read
    client.chars = chars
    return client


@mock.patch("oralb_ble.history.time.time", return_value=946684800 + 2000 + 30)
@mock.patch("oralb_ble.history.establish_connection")
@pytest.mark.asyncio
async def test_async_read_io_history(
    mock_establish_connection: mock.MagicMock, _mock_time: mock.MagicMock
) -> None:
    records = [make_record(1900, session_id=3), make_record(1500, session_id=2)]
    client = _mock_client(records)
    mock_establish_connection.return_value = client
    device = mock.Mock(address="x")

    sessions = await async_read_io_history(device)

    assert [s.session_id for s in sessions] == [3, 2]
    assert [s.index for s in sessions] == [0, 1]
    assert sessions[0].start == datetime(2000, 1, 1, 0, 32, 10, tzinfo=timezone.utc)
    client.write_gatt_char.assert_any_call(
        client.chars[CHARACTERISTIC_ACCESS_CONTROL], b"MGS", response=True
    )
    client.write_gatt_char.assert_any_call(
        client.chars[CHARACTERISTIC_CONTROL], bytes([0x31, 0x1E]), response=True
    )
    client.write_gatt_char.assert_any_call(
        client.chars[CHARACTERISTIC_CONTROL], bytes([0x02, 1]), response=True
    )
    client.disconnect.assert_awaited_once()


@mock.patch("oralb_ble.history.establish_connection")
@pytest.mark.asyncio
async def test_async_read_io_history_newer_than(
    mock_establish_connection: mock.MagicMock,
) -> None:
    records = [make_record(t, session_id=i) for i, t in enumerate((300, 200, 100))]
    mock_establish_connection.return_value = _mock_client(records)

    sessions = await async_read_io_history(mock.Mock(address="x"), newer_than=200)

    assert [s.device_time for s in sessions] == [300]


@mock.patch("oralb_ble.history.establish_connection")
@pytest.mark.asyncio
async def test_async_read_io_history_max_sessions(
    mock_establish_connection: mock.MagicMock,
) -> None:
    records = [make_record(1000 - i, session_id=i) for i in range(10)]
    mock_establish_connection.return_value = _mock_client(records)

    sessions = await async_read_io_history(mock.Mock(address="x"), max_sessions=4)

    assert [s.session_id for s in sessions] == [0, 1, 2, 3]


@mock.patch("oralb_ble.history.establish_connection")
@pytest.mark.asyncio
async def test_async_read_io_history_skips_isolated_empty_slot(
    mock_establish_connection: mock.MagicMock,
) -> None:
    records = [make_record(300), bytes(21), make_record(100)]
    client = _mock_client(records)
    mock_establish_connection.return_value = client

    sessions = await async_read_io_history(mock.Mock(address="x"))

    assert [s.index for s in sessions] == [0, 2]
    # Stops after three empty slots following the last record.
    assert client.read_gatt_char.await_count == 1 + 6


@mock.patch("oralb_ble.history.establish_connection")
@pytest.mark.asyncio
async def test_async_read_io_history_without_clock(
    mock_establish_connection: mock.MagicMock,
) -> None:
    client = _mock_client([make_record(300)], clock=bytes(4), with_access_control=False)
    mock_establish_connection.return_value = client

    sessions = await async_read_io_history(mock.Mock(address="x"))

    assert sessions[0].start is None
    written = [call.args[0] for call in client.write_gatt_char.await_args_list]
    assert all(char is client.chars[CHARACTERISTIC_CONTROL] for char in written)


@mock.patch("oralb_ble.history.establish_connection")
@pytest.mark.asyncio
async def test_async_read_io_history_missing_characteristic(
    mock_establish_connection: mock.MagicMock,
) -> None:
    client = _mock_client([])
    client.services.get_characteristic = mock.Mock(return_value=None)
    mock_establish_connection.return_value = client

    with pytest.raises(BleakCharacteristicNotFoundError):
        await async_read_io_history(mock.Mock(address="x"))
    client.disconnect.assert_awaited_once()


@mock.patch("oralb_ble.history.establish_connection")
@pytest.mark.asyncio
async def test_async_read_io_history_keep_alive(
    mock_establish_connection: mock.MagicMock,
) -> None:
    records = [make_record(1000 - i, session_id=i) for i in range(4)]
    client = _mock_client(records, clock=None)
    mock_establish_connection.return_value = client
    ticks = iter(range(0, 1000, 6))

    with mock.patch(
        "oralb_ble.history.time.monotonic", side_effect=lambda: next(ticks)
    ):
        sessions = await async_read_io_history(mock.Mock(address="x"))

    assert len(sessions) == 4
    assert sessions[0].start is None
    keep_alives = [
        call
        for call in client.write_gatt_char.await_args_list
        if call.args[1] == bytes([0x31, 0x1E])
    ]
    assert len(keep_alives) > 1
