"""Parser for OralB BLE advertisements.

This file is shamelessly copied from the following repository:
https://github.com/Ernst79/bleparser/blob/c42ae922e1abed2720c7fac993777e1bd59c0c93/package/bleparser/oral_b.py

MIT License applies.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum, auto

from bluetooth_data_tools import short_address
from bluetooth_sensor_state_data import BluetoothData
from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data.enum import StrEnum

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


class OralBBinarySensor(StrEnum):
    BRUSHING = "brushing"


class Models(Enum):

    IOSeries78 = auto()
    IOSeries4 = auto()
    SmartSeries7000 = auto()
    SmartSeries9000 = auto()


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
    8: "settings",
}


DEVICE_TYPES = {
    Models.IOSeries78: ModelDescription(
        device_type="IO Series 7/8",
        modes=IO_SERIES_MODES,
    ),
    Models.IOSeries4: ModelDescription(
        device_type="IO Series 4",
        modes=IO_SERIES_MODES,
    ),
    Models.SmartSeries7000: ModelDescription(
        device_type="Smart Series 7000",
        modes=SMART_SERIES_MODES,
    ),
    Models.SmartSeries9000: ModelDescription(
        device_type="Smart Series 9000",
        modes=SMART_SERIES_MODES,
    ),
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
    114: "normal",
    82: "normal",
    90: "power button pressed",
    86: "button pressed",
    56: "power button pressed",
    118: "button pressed",
    178: "high",
    146: "high",
    240: "high",
}


ORALB_MANUFACTURER = 0x00DC


BYTES_TO_MODEL = {
    b"\x062k": Models.IOSeries78,
    b"\x074\x0c": Models.IOSeries4,
    b"\x03!\x0c": Models.SmartSeries9000,
}
SECTOR_MAP = {
    254: "last sector",
    255: "no sector",
}


class OralBBluetoothDeviceData(BluetoothData):
    """Data for OralB BLE sensors."""

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
        if msg_length != 11:
            return

        device_bytes = data[0:3]
        state = data[3]
        pressure = data[4]
        time = data[5] * 60 + data[6]
        mode = data[7]
        sector = data[8]
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
        tb_sector = SECTOR_MAP.get(sector, f"sector {sector}")

        self.update_sensor(str(OralBSensor.TIME), None, time, None, "Time")
        self.update_sensor(str(OralBSensor.SECTOR), None, tb_sector, None, "Sector")
        self.update_sensor(
            str(OralBSensor.NUMBER_OF_SECTORS),
            None,
            no_of_sectors,
            None,
            "Number of sectors",
        )
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
