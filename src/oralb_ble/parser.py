"""Parser for OralB BLE advertisements.

This file is shamelessly copied from the following repository:
https://github.com/Ernst79/bleparser/blob/c42ae922e1abed2720c7fac993777e1bd59c0c93/package/bleparser/oral_b.py

MIT License applies.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from enum import Enum, auto

from bleak import BleakError, BLEDevice
from bleak_retry_connector import (
    BleakClientWithServiceCache,
    establish_connection,
    retry_bluetooth_connection_error,
)
from bluetooth_data_tools import short_address
from bluetooth_sensor_state_data import BluetoothData
from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data import SensorDeviceClass, SensorUpdate, Units
from sensor_state_data.enum import StrEnum

from .const import (
    BRUSHING_UPDATE_INTERVAL_SECONDS,
    CHARACTERISTIC_BATTERY,
    CHARACTERISTIC_PRESSURE,
    NOT_BRUSHING_UPDATE_INTERVAL_SECONDS,
    TIMEOUT_RECENTLY_BRUSHING,
)

_LOGGER = logging.getLogger(__name__)


class OralBSensor(StrEnum):

    TIME = "time"
    SECTOR = "sector"
    NUMBER_OF_SECTORS = "number_of_sectors"
    SECTOR_TIMER = "sector_timer"
    TOOTHBRUSH_STATE = "toothbrush_state"
    PRESSURE = "pressure"
    MODE = "mode"
    SIGNAL_STRENGTH = "signal_strength"
    BATTERY_PERCENT = "battery_percent"


class OralBBinarySensor(StrEnum):
    BRUSHING = "brushing"


class Models(Enum):

    D36 = auto()
    D21 = auto()
    D601 = auto()
    D700 = auto()
    D701 = auto()
    D706 = auto()
    IOSeries4 = auto()
    IOSeries5 = auto()
    IOSeries = auto()
    Unknown = auto()


@dataclass
class ModelDescription:

    device_type: str
    modes: dict[int, str]


SMART_SERIES_MODES = {
    0: "off",
    1: "daily clean",
    2: "sensitive",
    3: "massage",
    4: "whitening",
    5: "deep clean",
    6: "tongue cleaning",
    7: "turbo",
    255: "unknown",
}


IO_SERIES_MODES = {
    0: "daily clean",
    1: "sensitive",
    2: "gum care",
    3: "whiten",
    4: "intense",
    5: "super sensitive",
    6: "tongue cleaning",
    8: "settings",
    9: "off",
}


DEVICE_TYPES = {
    Models.D36: ModelDescription("Triumph D36", SMART_SERIES_MODES),
    Models.D21: ModelDescription("Smart Series D21", SMART_SERIES_MODES),
    Models.D601: ModelDescription("Pro Series D601", SMART_SERIES_MODES),
    Models.D700: ModelDescription("Smart Series D700", SMART_SERIES_MODES),
    Models.D701: ModelDescription("Genius Series D701", SMART_SERIES_MODES),
    Models.D706: ModelDescription("Genius X D706", SMART_SERIES_MODES),
    Models.IOSeries4: ModelDescription("IO Series 4", IO_SERIES_MODES),
    Models.IOSeries5: ModelDescription("IO Series 5", IO_SERIES_MODES),
    Models.IOSeries: ModelDescription("IO Series", IO_SERIES_MODES),
    Models.Unknown: ModelDescription("Unknown", SMART_SERIES_MODES),
}

STATES = {
    0: "unknown",
    1: "initializing",
    2: "idle",
    3: "running",
    4: "charging",
    5: "setup",
    6: "flight menu",
    8: "selection menu",
    9: "off",
    113: "final test",
    114: "pcb test",
    115: "sleeping",
    116: "transport",
}

PRESSURE = {
    0: "normal",
    16: "normal",
    32: "normal",
    48: "normal",
    50: "normal",
    54: "button pressed",
    56: "power button pressed",
    58: "power button pressed",
    80: "normal",
    82: "normal",
    86: "button pressed",
    90: "power button pressed",
    114: "normal",
    118: "button pressed",
    122: "power button pressed",
    144: "high",
    146: "high",
    150: "button pressed",
    154: "power button pressed",
    178: "high",
    182: "button pressed",
    186: "power button pressed",
    192: "high",
    240: "high",
    242: "high",
}

ACTIVE_CONNECTION_PRESSURE = {0: "low", 1: "normal", 2: "high"}

ORALB_MANUFACTURER = 0x00DC


# Model type is determined by byte 1 of the manufacturer data.
# Byte 0 is the protocol version, which determines how to parse the
# advertisement, but is NOT the model identifier.
# Reference: https://github.com/MatrixEditor/oralb-io/blob/master/oralb/blesdk/brush.py
MODEL_ID_TO_MODEL: dict[int, Models] = {
    # D36 line (Triumph / Professional Care)
    0: Models.D36,  # D36 X_MODE
    1: Models.D36,  # D36 6_MODE
    2: Models.D36,  # D36 5_MODE
    # D701 line (Genius)
    32: Models.D701,  # D701 X_MODE
    33: Models.D701,  # D701 6_MODE
    34: Models.D701,  # D701 5_MODE
    # D700 line (Smart/Pro Series)
    39: Models.D700,  # D700 5_MODE
    40: Models.D700,  # D700 4_MODE
    41: Models.D700,  # D700 6_MODE
    # SONOS line (IO Series)
    48: Models.IOSeries,  # SONOS X_MODE
    49: Models.IOSeries,  # SONOS IO
    50: Models.IOSeries,  # SONOS IO BIG_TI
    52: Models.IOSeries4,  # SONOS GALAXY IO4
    53: Models.IOSeries5,  # SONOS GALAXY IO5
    54: Models.IOSeries,  # SONOS EPLATFORM
    # D21 line (Smart Series - older generation)
    64: Models.D21,  # D21 X_MODE
    65: Models.D21,  # D21 4_MODE
    66: Models.D21,  # D21 3_MODE
    67: Models.D21,  # D21 2A_MODE
    68: Models.D21,  # D21 2B_MODE
    69: Models.D21,  # D21 3_MODE_WHITENING
    70: Models.D21,  # D21 1_MODE
    # D601 line (Pro)
    80: Models.D601,  # D601 X_MODE
    81: Models.D601,  # D601 5_MODE
    82: Models.D601,  # D601 4_MODE
    83: Models.D601,  # D601 3A_MODE
    84: Models.D601,  # D601 2A_MODE
    85: Models.D601,  # D601 2B_MODE
    86: Models.D601,  # D601 3B_MODE
    87: Models.D601,  # D601 1_MODE
    # D706 line (Genius X)
    112: Models.D706,  # D706 X_MODE
    113: Models.D706,  # D706 6_MODE
    114: Models.D706,  # D706 5_MODE
    117: Models.D706,  # D706 X_MODE_CHINA
    118: Models.D706,  # D706 6_MODE_CHINA
    119: Models.D706,  # D706 5_MODE_CHINA
}


def _decode_sector(sector: int, no_of_sectors: int | None) -> str:
    """Decode the sector code (manufacturer data byte 8).

    The low three bits hold the quadrant index: ``1``-``6`` for a concrete
    quadrant, ``7`` is a "last quadrant" sentinel and ``0`` means no quadrant.
    The upper bits are a display flag (which feedback face the handle shows)
    and do not change the quadrant, so they are masked off.

    Because ``7`` only marks the *last* quadrant, its real number depends on
    how many sectors the brush is configured for (byte 10). Firmware that does
    not report a sector count (``no_of_sectors`` 0 or absent) falls back to the
    historical four-sector assumption.

    This replaces the old hand-built lookup table, which only covered 4-sector
    brushes: it returned ``"unknown sector code 5"`` for sector 5 and wrongly
    reused ``"sector 4"`` for the last-quadrant sentinel on 6-sector brushes
    (e.g. IO Series 10).

    The old table also mapped a few bytes (41, 42, 43, 47, 55) to ``"success"``.
    Those carry the end-of-session feedback face in the upper bits and only
    occur in non-running frames, which #151 already reports as ``"no sector"``
    regardless of the byte -- so ``"success"`` was already unreachable through
    the sensor and is intentionally not reproduced here. A finished session is
    better detected from the ``running`` state ending together with the elapsed
    brushing time than from a transient sector value.
    """
    quadrant = sector & 0x07
    if quadrant == 0:
        return "no sector"
    if quadrant == 7:
        count = (no_of_sectors or 0) & 0x07
        return f"sector {count or 4}"
    return f"sector {quadrant}"


class OralBBluetoothDeviceData(BluetoothData):
    """Data for OralB BLE sensors."""

    def __init__(self) -> None:
        super().__init__()
        # If this is True, we are currently brushing or were brushing as of the last advertisement data
        self._brushing = False
        self._last_brush = 0.0

    def _start_update(self, service_info: BluetoothServiceInfo) -> None:
        """Update from BLE advertisement data."""
        _LOGGER.debug("Parsing OralB BLE advertisement data: %s", service_info)
        manufacturer_data = service_info.manufacturer_data
        address = service_info.address
        if ORALB_MANUFACTURER not in manufacturer_data:
            return None
        data = manufacturer_data[ORALB_MANUFACTURER]
        self.set_device_manufacturer("Oral-B")
        _LOGGER.debug("Parsing Oral-B sensor: %s", data)
        msg_length = len(data)
        if msg_length not in (9, 11):
            return

        model_type = data[1]
        state = data[3]
        pressure = data[4]
        brush_time = data[5] * 60 + data[6]
        mode = data[7]
        sector = data[8]
        sector_timer = None
        no_of_sectors = None
        if msg_length >= 11:
            sector_timer = data[9]
            no_of_sectors = data[10]

        model = MODEL_ID_TO_MODEL.get(model_type, Models.Unknown)
        model_info = DEVICE_TYPES[model]
        self.brush_modes = model_info.modes
        self.set_device_type(model_info.device_type)
        name = f"{model_info.device_type} {short_address(address)}"
        self.set_device_name(name)
        self.set_title(name)
        tb_state = STATES.get(state, f"unknown state {state}")
        tb_mode = self.brush_modes.get(mode, f"unknown mode {mode}")
        tb_pressure = PRESSURE.get(pressure, f"unknown pressure {pressure}")
        tb_sector = _decode_sector(sector, no_of_sectors)

        self.update_sensor(str(OralBSensor.TIME), None, brush_time, None, "Time")
        if tb_state != "running":
            # Sector is only meaningful while actively brushing. When the brush
            # is idle/off/sleeping/etc., the firmware keeps reporting the last
            # sector, which would otherwise persist forever in the sensor.
            self.update_sensor(
                str(OralBSensor.SECTOR), None, "no sector", None, "Sector"
            )
        else:
            self.update_sensor(str(OralBSensor.SECTOR), None, tb_sector, None, "Sector")
        if no_of_sectors is not None:
            self.update_sensor(
                str(OralBSensor.NUMBER_OF_SECTORS),
                None,
                no_of_sectors,
                None,
                "Number of sectors",
            )
        if sector_timer is not None:
            self.update_sensor(
                str(OralBSensor.SECTOR_TIMER), None, sector_timer, None, "Sector Timer"
            )
        self.update_sensor(
            str(OralBSensor.TOOTHBRUSH_STATE), None, tb_state, None, "Toothbrush State"
        )
        self.update_sensor(
            str(OralBSensor.PRESSURE), None, tb_pressure, None, "Pressure"
        )
        self.update_sensor(str(OralBSensor.MODE), None, tb_mode, None, "Mode")
        self.update_binary_sensor(
            str(OralBBinarySensor.BRUSHING), state == 3, None, "Brushing"
        )
        if state == 3:
            self._brushing = True
            self._last_brush = time.monotonic()
        else:
            self._brushing = False

    def poll_needed(
        self, service_info: BluetoothServiceInfo, last_poll: float | None
    ) -> bool:
        """
        This is called every time we get a service_info for a device. It means the
        device is working and online.
        """
        if last_poll is None:
            return True
        update_interval = NOT_BRUSHING_UPDATE_INTERVAL_SECONDS
        if (
            self._brushing
            or time.monotonic() - self._last_brush <= TIMEOUT_RECENTLY_BRUSHING
        ):
            update_interval = BRUSHING_UPDATE_INTERVAL_SECONDS
        return last_poll > update_interval

    @retry_bluetooth_connection_error()
    async def _get_payload(self, client: BleakClientWithServiceCache) -> None:
        """Get the payload from the brush using its gatt_characteristics."""
        battery_char = client.services.get_characteristic(CHARACTERISTIC_BATTERY)
        battery_payload = await client.read_gatt_char(battery_char)
        pressure_char = client.services.get_characteristic(CHARACTERISTIC_PRESSURE)
        pressure_payload = await client.read_gatt_char(pressure_char)
        tb_pressure = ACTIVE_CONNECTION_PRESSURE.get(
            pressure_payload[0], f"unknown pressure {pressure_payload[0]}"
        )
        self.update_sensor(
            str(OralBSensor.PRESSURE), None, tb_pressure, None, "Pressure"
        )
        self.update_sensor(
            str(OralBSensor.BATTERY_PERCENT),
            Units.PERCENTAGE,
            battery_payload[0],
            SensorDeviceClass.BATTERY,
            "Battery",
        )
        _LOGGER.debug("Successfully read active gatt characters")

    async def async_poll(self, ble_device: BLEDevice) -> SensorUpdate:
        """
        Poll the device to retrieve any values we can't get from passive listening.
        """
        _LOGGER.debug("Polling Oral-B device: %s", ble_device.address)
        client = await establish_connection(
            BleakClientWithServiceCache, ble_device, ble_device.address
        )
        try:
            await self._get_payload(client)
        except BleakError as err:
            _LOGGER.warning("Reading gatt characters failed with err: %s", err)
        except IndexError as err:
            # An empty gatt read would otherwise raise an unhandled IndexError
            # when indexing pressure_payload[0] / battery_payload[0].
            _LOGGER.warning("Empty gatt payload while reading characters: %s", err)
        finally:
            await client.disconnect()
            _LOGGER.debug("Disconnected from active bluetooth client")
        return self._finish_update()
