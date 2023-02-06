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

from bleak import BLEDevice
from bleak_retry_connector import BleakClientWithServiceCache, establish_connection
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

    Pro6000 = auto()
    TriumphV2 = auto()
    IOSeries4 = auto()
    IOSeries67 = auto()
    IOSeries8 = auto()
    IOSeries9 = auto()
    IOSeries89 = auto()
    SmartSeries4000 = auto()
    SmartSeries6000 = auto()
    SmartSeries7000 = auto()
    SmartSeries8000 = auto()
    SmartSeries9000 = auto()
    GeniusX = auto()


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


SMART_SERIES_6000_MODES = SMART_SERIES_MODES | {2: "off"}


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
    Models.Pro6000: ModelDescription("Pro 6000", SMART_SERIES_MODES),
    Models.TriumphV2: ModelDescription("Triumph V2", SMART_SERIES_MODES),
    Models.IOSeries4: ModelDescription(
        device_type="IO Series 4",
        modes=IO_SERIES_MODES,
    ),
    Models.IOSeries67: ModelDescription(
        device_type="IO Series 6/7",
        modes=IO_SERIES_MODES,
    ),
    Models.IOSeries8: ModelDescription(
        device_type="IO Series 8",
        modes=IO_SERIES_MODES,
    ),
    Models.IOSeries9: ModelDescription(
        device_type="IO Series 9",
        modes=IO_SERIES_MODES,
    ),
    Models.IOSeries89: ModelDescription(
        device_type="IO Series 8/9",
        modes=IO_SERIES_MODES,
    ),
    Models.SmartSeries4000: ModelDescription(
        device_type="Smart Series 4000",
        modes=SMART_SERIES_MODES,
    ),
    Models.SmartSeries6000: ModelDescription(
        device_type="Smart Series 6000",
        modes=SMART_SERIES_6000_MODES,
    ),
    Models.SmartSeries7000: ModelDescription(
        device_type="Smart Series 7000",
        modes=SMART_SERIES_MODES,
    ),
    Models.SmartSeries8000: ModelDescription(
        device_type="Smart Series 8000",
        modes=SMART_SERIES_MODES,
    ),
    Models.SmartSeries9000: ModelDescription(
        device_type="Smart Series 9000/10000",
        modes=SMART_SERIES_MODES,
    ),
    Models.GeniusX: ModelDescription(device_type="Genius X", modes=SMART_SERIES_MODES),
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
    56: "power button pressed",
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


BYTES_TO_MODEL = {
    b"\x062k": Models.IOSeries67,
    b"\x074\x0c": Models.IOSeries4,
    b"\x074\x1a": Models.IOSeries4,
    b"\x03V\x04": Models.SmartSeries4000,
    b"\x04'\r": Models.SmartSeries6000,
    b'\x03"\x0c': Models.SmartSeries8000,
    b"\x03!\x0b": Models.SmartSeries9000,
    b"\x03!\x0c": Models.SmartSeries9000,
    b"\x061\x19": Models.IOSeries89,
    b"\x061\x16": Models.IOSeries89,
    b"\x02\x02\x06": Models.TriumphV2,
    b"\x01\x02\x05": Models.Pro6000,
    b"\x04q\x04": Models.GeniusX,
}

SECTOR_MAP = {
    1: "sector 1",
    9: "sector 1",
    2: "sector 2",
    10: "sector 2",
    3: "sector 3",
    11: "sector 3",
    19: "sector 3",
    27: "sector 3",
    4: "sector 4",
    7: "sector 4",
    15: "sector 4",
    31: "sector 4",
    39: "sector 4",
    41: "success",
    42: "success",
    43: "success",
    47: "success",
    55: "success",
}


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

        device_bytes = data[0:3]
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

        model = BYTES_TO_MODEL.get(device_bytes, Models.SmartSeries7000)
        model_info = DEVICE_TYPES[model]
        modes = model_info.modes
        self.set_device_type(model_info.device_type)
        name = f"{model_info.device_type} {short_address(address)}"
        self.set_device_name(name)
        self.set_title(name)
        tb_state = STATES.get(state, f"unknown state {state}")
        tb_mode = modes.get(mode, f"unknown mode {mode}")
        tb_pressure = PRESSURE.get(pressure, f"unknown pressure {pressure}")
        tb_sector = SECTOR_MAP.get(sector, f"unknown sector code {sector}")

        self.update_sensor(str(OralBSensor.TIME), None, brush_time, None, "Time")
        if brush_time == 0 and tb_state != "running":
            # When starting up, sector is not accurate.
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
            str(OralBBinarySensor.BRUSHING), bool(state == 3), None, "Brushing"
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

    async def async_poll(self, ble_device: BLEDevice) -> SensorUpdate:
        """
        Poll the device to retrieve any values we can't get from passive listening.
        """
        client = await establish_connection(
            BleakClientWithServiceCache, ble_device, ble_device.address
        )
        try:
            battery_char = client.services.get_characteristic(CHARACTERISTIC_BATTERY)
            battery_payload = await client.read_gatt_char(battery_char)
            pressure_char = client.services.get_characteristic(CHARACTERISTIC_PRESSURE)
            pressure_payload = await client.read_gatt_char(pressure_char)
        finally:
            await client.disconnect()
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
        return self._finish_update()
