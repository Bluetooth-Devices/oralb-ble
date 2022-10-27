"""Parser for OralB BLE advertisements.

This file is shamelessly copied from the following repository:
https://github.com/Ernst79/bleparser/blob/c42ae922e1abed2720c7fac993777e1bd59c0c93/package/bleparser/oral_b.py

MIT License applies.
"""
from __future__ import annotations

import logging
import struct
from dataclasses import dataclass
from enum import Enum, auto

from bluetooth_data_tools import short_address
from bluetooth_sensor_state_data import BluetoothData
from home_assistant_bluetooth import BluetoothServiceInfo
from sensor_state_data.enum import StrEnum

_LOGGER = logging.getLogger(__name__)


UNPACK_BBBBBBBB = struct.Struct(">BBBBBBBB").unpack


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

    IOSeries7 = auto()
    IOSeries4 = auto()
    SmartSeries7000 = auto()


@dataclass
class ModelDescription:

    device_type: str
    modes: dict[int, str]


DEVICE_TYPES = {
    Models.IOSeries7: ModelDescription(
        device_type="IO Series 7",
        modes={
            0: "daily clean",
            1: "sensitive",
            2: "gum care",
            3: "whiten",
            4: "intense",
            8: "settings",
        },
    ),
    Models.IOSeries4: ModelDescription(
        device_type="IO Series 4",
        modes={
            0: "daily clean",
            1: "sensitive",
            2: "gum care",
            3: "whiten",
            4: "intense",
            8: "settings",
        },
    ),
    Models.SmartSeries7000: ModelDescription(
        device_type="Smart Series 7000",
        modes={
            0: "off",
            1: "daily clean",
            2: "sensitive",
            3: "massage",
            4: "whitening",
            5: "deep clean",
            6: "tongue cleaning",
            7: "turbo",
            255: "unknown",
        },
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
    113: "final test",
    114: "pcb test",
    115: "sleeping",
    116: "transport",
}

PRESSURE = {114: "normal", 118: "button pressed", 178: "high"}


ORALB_MANUFACTURER = 0x00DC


class OralBBluetoothDeviceData(BluetoothData):
    """Data for OralB BLE sensors."""

    def _start_update(self, service_info: BluetoothServiceInfo) -> None:
        """Update from BLE advertisement data."""
        _LOGGER.debug("Parsing OralB BLE advertisement data: %s", service_info)
        manufacturer_data = service_info.manufacturer_data
        local_name = service_info.name
        address = service_info.address
        if ORALB_MANUFACTURER not in manufacturer_data:
            return None

        mfr_data = manufacturer_data[ORALB_MANUFACTURER]
        self.set_device_manufacturer("Oral-B")

        self._process_mfr_data(address, local_name, mfr_data)

    def _process_mfr_data(
        self,
        address: str,
        local_name: str,
        data: bytes,
    ) -> None:
        """Parser for OralB sensors."""
        _LOGGER.debug("Parsing OralB sensor: %s", data)
        msg_length = len(data)
        if msg_length != 11:
            return
        state = data[3]
        pressure = data[4]
        time = data[5] * 60 + data[6]
        mode = data[7]
        sector = data[8]
        sector_timer = data[9]
        no_of_sectors = data[10]

        device_bytes = data[0:3]
        if device_bytes == b"\x062k":
            model = Models.IOSeries7
        elif device_bytes == b"\x074\x0c":
            model = Models.IOSeries4
        else:
            model = Models.SmartSeries7000

        model_info = DEVICE_TYPES[model]
        modes = model_info.modes
        self.set_device_type(model_info.device_type)
        name = f"{model_info.device_type} {short_address(address)}"
        self.set_device_name(name)
        self.set_title(name)

        tb_state = STATES.get(state, "unknown state " + str(state))
        tb_mode = modes.get(mode, "unknown mode " + str(mode))
        tb_pressure = PRESSURE.get(pressure, "unknown pressure " + str(pressure))

        if sector == 254:
            tb_sector = "last sector"
        elif sector == 255:
            tb_sector = "no sector"
        else:
            tb_sector = "sector " + str(sector)

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
