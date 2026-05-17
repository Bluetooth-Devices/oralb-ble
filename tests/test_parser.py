from __future__ import annotations

from unittest import mock

import pytest
from bleak.exc import BleakError
from bluetooth_sensor_state_data import BluetoothServiceInfo, SensorUpdate
from sensor_state_data import (
    BinarySensorDescription,
    BinarySensorValue,
    DeviceKey,
    SensorDescription,
    SensorDeviceClass,
    SensorDeviceInfo,
    SensorValue,
    Units,
)

from oralb_ble.parser import SMART_SERIES_MODES, OralBBluetoothDeviceData

from . import generate_ble_device

# 2022-10-24 18:10:10.048 DEBUG (MainThread) [homeassistant.components.bluetooth.manager] 00:E0:43:87:4B:03: 78:DB:2F:C2:48:BE AdvertisementData(manufacturer_data={220: b'\x02\x01\x08\x02 \x00\x00\x01\x01\x00\x04'}, rssi=-64) connectable: True match: set() rssi: -64
# 2022-10-24 18:10:12.604 DEBUG (MainThread) [homeassistant.components.bluetooth.manager] 00:E0:43:87:4B:03: 78:DB:2F:C2:48:BE AdvertisementData(manufacturer_data={220: b'\x02\x01\x08\x03\x00\x00\x00\x01\x01\x00\x04'}, rssi=-56) connectable: True match: set() rssi: -56
# 2022-10-24 18:10:13.798 DEBUG (MainThread) [homeassistant.components.bluetooth.manager] 00:E0:43:87:4B:03: 78:DB:2F:C2:48:BE AdvertisementData(manufacturer_data={220: b'\x02\x01\x08\x02\x00\x00\x01\x01\x01\x03\x04'}, rssi=-54) connectable: True match: set() rssi: -54
# 2022-10-24 18:10:14.930 DEBUG (MainThread) [homeassistant.components.bluetooth.manager] 00:E0:43:87:4B:03: 78:DB:2F:C2:48:BE AdvertisementData(manufacturer_data={220: b'\x02\x01\x08\x02 \x00\x01\x01\x01\x03\x04'}, rssi=-64) connectable: True match: set() rssi: -64

ORALB_DATA_1 = BluetoothServiceInfo(
    name="78:DB:2F:C2:48:BE",
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    manufacturer_data={220: b"\x02\x01\x08\x02 \x00\x00\x01\x01\x00\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_DATA_2 = BluetoothServiceInfo(
    name="78:DB:2F:C2:48:BE",
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    manufacturer_data={220: b"\x02\x01\x08\x03\x00\x00\x00\x01\x01\x00\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_DATA_3 = BluetoothServiceInfo(
    name="78:DB:2F:C2:48:BE",
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    manufacturer_data={220: b"\x02\x01\x08\x02\x00\x00\x01\x01\x01\x03\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_DATA_4 = BluetoothServiceInfo(
    name="78:DB:2F:C2:48:BE",
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    manufacturer_data={220: b"\x02\x01\x08\x02 \x00\x01\x01\x01\x03\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_IO_SERIES_6 = BluetoothServiceInfo(
    name="78:DB:2F:C2:48:BE",
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    manufacturer_data={220: b"\x062k\x02r\x00\x00\x01\x01\x00\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_IO_SERIES_7 = BluetoothServiceInfo(
    name="78:DB:2F:C2:48:BE",
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    manufacturer_data={220: b"\x062k\x02 \x00\x01\x01\x01\x03\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_IO_SERIES_8 = BluetoothServiceInfo(
    name="78:DB:2F:C2:48:BE",
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    manufacturer_data={220: b"\x061\x19\x08r\x00\x00\x00\x07\x00\x00"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_IO_SERIES_4 = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="GXB772CD\x00\x00\x00\x00\x00\x00\x00\x00\x00",
    manufacturer_data={220: b"\x074\x0c\x038\x00\x00\x02\x01\x00\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_D701_GENIUS_9000 = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="9000",
    manufacturer_data={220: b"\x03!\x0c\x020\x00\x06\x01\x01\x14\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
# https://github.com/home-assistant/core/issues/81967
ORALB_D701_GENIUS_9000_BLACK = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="9000",
    manufacturer_data={220: b"\x03!\x0b\x020\x00\x00\x01\x01\x80\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_IO_SERIES_9 = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="Oral-B Toothbrush",
    manufacturer_data={220: b"\x061\x16\x08r\x00\x00\x03\x02\x00\x04"},
    service_uuids=["0000fe0d-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
ORALB_D601 = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="4000",
    manufacturer_data={220: b"\x03V\x04\x030\x00\x00\x01\x01\x00\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_D700 = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="6000",
    manufacturer_data={220: b"\x04'\r\x032\x00\x06\x01\x01\x14\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_D700_HIGH_PRESSURE = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="6000",
    manufacturer_data={220: b"\x04'\r\x032\x00\x04\x01\x01\r\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_D700_NORMAL_PRESSURE = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="6000",
    manufacturer_data={220: b"\x04'\r\x032\x00\x1b\x02\x01Z\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_TRIUMPH_V2 = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="T2",
    manufacturer_data={220: b"\x02\x02\x06\x02 \x00\x00\x01\x0f\x00\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_TRIUMPH_V2_DATA_2 = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="T2",
    manufacturer_data={220: b"\x02\x02\x06\x03\x00\x00\x01\x01\x01\x03\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_PRO_SERIES_6000 = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="PRO6000",
    manufacturer_data={220: b"\x01\x02\x05\x03\x00\x00\x08\x04\x01"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_D701_GENIUS_8000 = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="GENIUS8000",
    manufacturer_data={220: b'\x03"\x0c\x02 \x00\x00\x07\x0f\x00\x04'},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_D701_GENIUS_8000_HIGH_PRESSURE = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="GENIUS8000",
    manufacturer_data={220: b'\x03"\x0c\x03\xc0\x010\x07\x04<\x04'},
    service_uuids=[],
    service_data={},
    source="local",
)

ORALB_IO_SERIES_6_DAILY_CLEAN = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="Oral-B Toothbrush",
    manufacturer_data={220: b"\x062k\x02r\x00\x00\x00\x01\x00\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_IO_SERIES_6_SENSITIVE = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="Oral-B Toothbrush",
    manufacturer_data={220: b"\x062k\x02r\x00\x00\x01\x01\x00\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_IO_SERIES_6_GUM_CARE = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="Oral-B Toothbrush",
    manufacturer_data={220: b"\x062k\x02r\x00\x00\x02\x01\x00\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_IO_SERIES_6_WHITEN = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="Oral-B Toothbrush",
    manufacturer_data={220: b"\x062k\x02r\x00\x00\x03\x01\x00\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)


# https://github.com/Bluetooth-Devices/oralb-ble/issues/65
# User has IO Series 9, byte 1 = 0x32 (50) = SONOS IO BIG_TI
ORALB_IO_SERIES_9_ISSUE_65 = BluetoothServiceInfo(
    address="2C:A7:74:50:70:F3",
    rssi=-85,
    name="Oral-B Toothbrush",
    manufacturer_data={220: b"\x062k\x08r\x00\x00\x00\x07\x00\x04"},
    service_uuids=["0000fe0d-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
# https://github.com/Bluetooth-Devices/oralb-ble/issues/51
# User has Pro 5000, byte 1 = 0x27 (39) = D700 5_MODE
ORALB_D700_PRO_5000_ISSUE_51 = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-93,
    name="Oral-B Toothbrush",
    manufacturer_data={220: b"\x04'\r\x032\x00\n\x01\x01!\x04"},
    service_uuids=["0000fe0d-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
# https://github.com/home-assistant/core/issues/133940
# User has IO Series 9N, byte 1 = 0x32 (50) = SONOS IO BIG_TI
ORALB_IO_SERIES_9N_HA_133940 = BluetoothServiceInfo(
    address="20:0B:16:3F:20:9F",
    rssi=-100,
    name="Oral-B Toothbrush",
    manufacturer_data={220: b"\x062k\x08z\x00\x00\x00\x01\x00\x04"},
    service_uuids=["0000fe0d-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
# https://github.com/home-assistant/core/issues/133940#issuecomment-2479268850
# User has IO Series 9, byte 1 = 0x36 (54) = SONOS EPLATFORM
ORALB_IO_SERIES_9_HA_133940_EPLATFORM = BluetoothServiceInfo(
    address="88:0F:62:48:5A:14",
    rssi=-94,
    name="Oral-B Toothbrush",
    manufacturer_data={220: b"\x086R\x082\x00\x00\x05\x00\x01\x00"},
    service_uuids=["0000fe0d-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
# https://github.com/home-assistant/core/issues/133934
# User has IO Series 5, byte 1 = 0x35 (53) = SONOS GALAXY IO5
ORALB_IO_SERIES_5_HA_133934 = BluetoothServiceInfo(
    address="30:FB:10:4E:AC:5C",
    rssi=-78,
    name="GX4EAC5C",
    manufacturer_data={220: b"\x075\x1e\t6\x00\x05\x05\x01\x00\x04"},
    service_uuids=[
        "00001801-0000-1000-8000-00805f9b34fb",
        "0000fe0d-0000-1000-8000-00805f9b34fb",
    ],
    service_data={},
    source="local",
)
# https://github.com/home-assistant/core/issues/87413
# User has IO Series 9, byte 1 = 0x32 (50) = SONOS IO BIG_TI
ORALB_IO_SERIES_9_HA_87413 = BluetoothServiceInfo(
    address="B0:D2:78:1D:67:78",
    rssi=-68,
    name="Oral-B Toothbrush",
    manufacturer_data={220: b"\x062k\x08R\x00\x00\x00\x01\x00\x04"},
    service_uuids=[
        "00001800-0000-1000-8000-00805f9b34fb",
        "00001801-0000-1000-8000-00805f9b34fb",
    ],
    service_data={},
    source="local",
)
# https://github.com/Bluetooth-Devices/oralb-ble/issues/45
# User has IO Series 10, byte 1 = 0x32 (50) = SONOS IO BIG_TI
ORALB_IO_SERIES_10_ISSUE_45 = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-61,
    name="Oral-B Toothbrush",
    manufacturer_data={220: b"\x062k\x03r\x00\x00\x06\x00\x00\x01"},
    service_uuids=["0000fe0d-0000-1000-8000-00805f9b34fb"],
    service_data={},
    source="local",
)
# https://github.com/home-assistant/core/issues/142787
# User has TriZone 5000 (Type 3754), byte 1 = 0x41 (65) = D21 4_MODE
ORALB_D21_TRIZONE_5000_HA_142787 = BluetoothServiceInfo(
    address="5C:31:3E:FC:05:58",
    rssi=-52,
    name="5C:31:3E:FC:05:58",
    manufacturer_data={220: b"\x01A\x05\x03\x00\x00\x00\x01\x01"},
    service_uuids=[],
    service_data={},
    source="local",
)


def test_can_create():
    OralBBluetoothDeviceData()


def test_dataset_1():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_DATA_1
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Triumph D36 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Triumph D36 48BE",
                model="Triumph D36",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=0,
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="no " "sector",
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=0,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="idle",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="daily " "clean",
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=False,
            )
        },
        events={},
    )


def test_dataset_2():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_DATA_2
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Triumph D36 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Triumph D36 48BE",
                model="Triumph D36",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="sector " "1",
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="running",
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=0,
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="daily " "clean",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=0,
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=True,
            )
        },
        events={},
    )


def test_dataset_3():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_DATA_3
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Triumph D36 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Triumph D36 48BE",
                model="Triumph D36",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="no " "sector",
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=3,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="idle",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="daily " "clean",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=1,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=False,
            )
        },
        events={},
    )


def test_dataset_4():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_DATA_4
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Triumph D36 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Triumph D36 48BE",
                model="Triumph D36",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="daily " "clean",
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="idle",
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=3,
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="no " "sector",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=1,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=False,
            )
        },
        events={},
    )


def test_io_series_6():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_IO_SERIES_6
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="IO Series 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 48BE",
                model="IO Series",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="no " "sector",
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="idle",
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="sensitive",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=0,
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=False,
            )
        },
        events={},
    )


def test_io_series_6_daily_clean_mode():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_IO_SERIES_6_DAILY_CLEAN
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="IO Series 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 48BE",
                model="IO Series",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="no " "sector",
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="idle",
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="daily clean",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=0,
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=False,
            )
        },
        events={},
    )


def test_io_series_6_sensitive_mode():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_IO_SERIES_6_SENSITIVE
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="IO Series 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 48BE",
                model="IO Series",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="no " "sector",
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="idle",
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="sensitive",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=0,
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=False,
            )
        },
        events={},
    )


def test_io_series_6_gum_care_mode():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_IO_SERIES_6_GUM_CARE
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="IO Series 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 48BE",
                model="IO Series",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="no " "sector",
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="idle",
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="gum care",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=0,
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=False,
            )
        },
        events={},
    )


def test_io_series_6_whiten_mode():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_IO_SERIES_6_WHITEN
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="IO Series 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 48BE",
                model="IO Series",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="no " "sector",
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="idle",
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="whiten",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=0,
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=False,
            )
        },
        events={},
    )


def test_io_series_7():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_IO_SERIES_7
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="IO Series 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 48BE",
                model="IO Series",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=3,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="no " "sector",
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="idle",
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="sensitive",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=1,
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=False,
            )
        },
        events={},
    )


def test_io_series_4():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_IO_SERIES_4
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="IO Series 4 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 4 48BE",
                model="IO Series 4",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="sector " "1",
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="running",
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="gum " "care",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=0,
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="power button pressed",
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=True,
            )
        },
        events={},
    )


def test_d701_genius_9000():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_D701_GENIUS_9000
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Genius Series D701 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Genius Series D701 48BE",
                model="Genius Series D701",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=20,
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="daily " "clean",
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="idle",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=6,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="no " "sector",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=False,
            )
        },
        events={},
    )


def test_d701_genius_9000_black():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_D701_GENIUS_9000_BLACK
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Genius Series D701 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Genius Series D701 48BE",
                model="Genius Series D701",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=128,
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="daily " "clean",
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="no " "sector",
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="idle",
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=False,
            )
        },
        events={},
    )


def test_io_series_9():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_IO_SERIES_9
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="IO Series 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 48BE",
                model="IO Series",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="no " "sector",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=0,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="selection " "menu",
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="whiten",
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=False,
            )
        },
        events={},
    )


def test_d601():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_D601
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Pro Series D601 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Pro Series D601 48BE",
                model="Pro Series D601",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=0,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="sector " "1",
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="daily " "clean",
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=0,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="running",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=True,
            )
        },
        events={},
    )


def test_triumph_v2():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_TRIUMPH_V2
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Triumph D36 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Triumph D36 48BE",
                model="Triumph D36",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=0,
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="daily " "clean",
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="no " "sector",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=0,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="idle",
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=False,
            )
        },
        events={},
    )


def test_triumph_v2_data_2():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_TRIUMPH_V2_DATA_2
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Triumph D36 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Triumph D36 48BE",
                model="Triumph D36",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=3,
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="daily " "clean",
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="sector " "1",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=1,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="running",
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=True,
            )
        },
        events={},
    )


def test_pro_series_6000():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_PRO_SERIES_6000
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Triumph D36 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Triumph D36 48BE",
                model="Triumph D36",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="whitening",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=8,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="running",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="sector " "1",
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=True,
            )
        },
        events={},
    )


def test_d700():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_D700
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Smart Series D700 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Smart Series D700 48BE",
                model="Smart Series D700",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=6,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=20,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="running",
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="sector " "1",
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="daily " "clean",
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=True,
            )
        },
        events={},
    )


def test_d700_high_pressure():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_D700_HIGH_PRESSURE
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Smart Series D700 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Smart Series D700 48BE",
                model="Smart Series D700",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="daily " "clean",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="running",
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=13,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="sector " "1",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=4,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=True,
            )
        },
        events={},
    )


def test_d700_normal_pressure():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_D700_NORMAL_PRESSURE
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Smart Series D700 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Smart Series D700 48BE",
                model="Smart Series D700",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="sensitive",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=90,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="running",
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=27,
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="sector " "1",
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=True,
            )
        },
        events={},
    )


def test_genius_8000():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_D701_GENIUS_8000
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Genius Series D701 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Genius Series D701 48BE",
                model="Genius Series D701",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=0,
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=0,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="idle",
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="turbo",
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="no " "sector",
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=False,
            )
        },
        events={},
    )


def test_genius_8000_high_pressure():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_D701_GENIUS_8000_HIGH_PRESSURE
    result = parser.update(service_info)
    assert parser.brush_modes == SMART_SERIES_MODES
    assert result == SensorUpdate(
        title="Genius Series D701 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Genius Series D701 48BE",
                model="Genius Series D701",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="high",
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="running",
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=60,
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="turbo",
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="sector " "4",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=108,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=4,
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=True,
            )
        },
        events={},
    )


def test_io_series_8():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_IO_SERIES_8
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="IO Series 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 48BE",
                model="IO Series",
                manufacturer="Oral-B",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="sector_timer", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="mode", device_id=None): SensorDescription(
                device_key=DeviceKey(key="mode", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=SensorDeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
            DeviceKey(key="pressure", device_id=None): SensorDescription(
                device_key=DeviceKey(key="pressure", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="sector", device_id=None): SensorDescription(
                device_key=DeviceKey(key="sector", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="time", device_id=None): SensorDescription(
                device_key=DeviceKey(key="time", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorDescription(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorDescription(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                device_class=None,
                native_unit_of_measurement=None,
            ),
        },
        entity_values={
            DeviceKey(key="sector_timer", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector_timer", device_id=None),
                name="Sector " "Timer",
                native_value=0,
            ),
            DeviceKey(key="mode", device_id=None): SensorValue(
                device_key=DeviceKey(key="mode", device_id=None),
                name="Mode",
                native_value="daily " "clean",
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal " "Strength",
                native_value=-63,
            ),
            DeviceKey(key="pressure", device_id=None): SensorValue(
                device_key=DeviceKey(key="pressure", device_id=None),
                name="Pressure",
                native_value="normal",
            ),
            DeviceKey(key="sector", device_id=None): SensorValue(
                device_key=DeviceKey(key="sector", device_id=None),
                name="Sector",
                native_value="no " "sector",
            ),
            DeviceKey(key="time", device_id=None): SensorValue(
                device_key=DeviceKey(key="time", device_id=None),
                name="Time",
                native_value=0,
            ),
            DeviceKey(key="number_of_sectors", device_id=None): SensorValue(
                device_key=DeviceKey(key="number_of_sectors", device_id=None),
                name="Number " "of " "sectors",
                native_value=0,
            ),
            DeviceKey(key="toothbrush_state", device_id=None): SensorValue(
                device_key=DeviceKey(key="toothbrush_state", device_id=None),
                name="Toothbrush " "State",
                native_value="selection " "menu",
            ),
        },
        binary_entity_descriptions={
            DeviceKey(key="brushing", device_id=None): BinarySensorDescription(
                device_key=DeviceKey(key="brushing", device_id=None), device_class=None
            )
        },
        binary_entity_values={
            DeviceKey(key="brushing", device_id=None): BinarySensorValue(
                device_key=DeviceKey(key="brushing", device_id=None),
                name="Brushing",
                native_value=False,
            )
        },
        events={},
    )


@mock.patch("oralb_ble.parser.establish_connection")
@pytest.mark.asyncio
async def test_async_poll(mock_establish_connection):
    parser = OralBBluetoothDeviceData()
    device = generate_ble_device(address="abc", name="test_device")
    mock_establish_connection.return_value.read_gatt_char.side_effect = [
        bytearray(b";\x00\x00\x00"),
        bytearray(b"\x01\x89\x7f\xbe\x04`\x7f\xbe\x047"),
    ]
    res = await parser.async_poll(device)
    assert (
        res.entity_values.get(DeviceKey("battery_percent")).native_value == 59
        and res.entity_values.get(DeviceKey("pressure")).native_value == "normal"
    )


@mock.patch("oralb_ble.parser.establish_connection")
@pytest.mark.asyncio
async def test_async_poll_empty_gatt_payload(mock_establish_connection):
    """Empty gatt reads must not crash async_poll with an IndexError."""
    parser = OralBBluetoothDeviceData()
    device = generate_ble_device(address="abc", name="test_device")
    mock_establish_connection.return_value.read_gatt_char.side_effect = [
        bytearray(b""),
        bytearray(b""),
    ]
    res = await parser.async_poll(device)
    assert isinstance(res, SensorUpdate)


@mock.patch("oralb_ble.parser.establish_connection")
@pytest.mark.asyncio
async def test_async_poll_bleak_error(mock_establish_connection):
    """A BleakError raised while reading gatt characters is swallowed."""
    parser = OralBBluetoothDeviceData()
    device = generate_ble_device(address="abc", name="test_device")
    mock_establish_connection.return_value.read_gatt_char.side_effect = BleakError(
        "disconnected"
    )
    res = await parser.async_poll(device)
    assert isinstance(res, SensorUpdate)


def test_poll_needed_no_time():
    parser = OralBBluetoothDeviceData()
    assert parser.poll_needed(None, None)


def test_poll_needed_brushing():
    parser = OralBBluetoothDeviceData()
    parser._brushing = True
    assert parser.poll_needed(None, 61)


@mock.patch("oralb_ble.parser.time")
def test_poll_needed_brushing_recently(mocked_time):
    parser = OralBBluetoothDeviceData()
    mocked_time.monotonic.return_value = 5
    parser._brushing = False
    parser._last_brush = 0
    assert parser.poll_needed(None, 61)


def test_io_series_9_issue_65():
    """IO Series 9 reported as IO Series 6/7 - oralb-ble#65."""
    parser = OralBBluetoothDeviceData()
    result = parser.update(ORALB_IO_SERIES_9_ISSUE_65)
    assert result.devices[None].model == "IO Series"


def test_d700_pro_5000_issue_51():
    """Pro 5000 reported as Smart Series 6000 - oralb-ble#51."""
    parser = OralBBluetoothDeviceData()
    result = parser.update(ORALB_D700_PRO_5000_ISSUE_51)
    assert result.devices[None].model == "Smart Series D700"


def test_io_series_9n_ha_133940():
    """IO Series 9N reported as 6/7 - HA#133940."""
    parser = OralBBluetoothDeviceData()
    result = parser.update(ORALB_IO_SERIES_9N_HA_133940)
    assert result.devices[None].model == "IO Series"


def test_io_series_9_eplatform_ha_133940():
    """IO Series 9 on EPLATFORM reported as 6/7 - HA#133940."""
    parser = OralBBluetoothDeviceData()
    result = parser.update(ORALB_IO_SERIES_9_HA_133940_EPLATFORM)
    assert result.devices[None].model == "IO Series"


def test_io_series_5_ha_133934():
    """IO Series 5 reported as Smart Series 7000 - HA#133934."""
    parser = OralBBluetoothDeviceData()
    result = parser.update(ORALB_IO_SERIES_5_HA_133934)
    assert result.devices[None].model == "IO Series 5"


def test_io_series_9_ha_87413():
    """IO Series 9 reported as 6/7 - HA#87413."""
    parser = OralBBluetoothDeviceData()
    result = parser.update(ORALB_IO_SERIES_9_HA_87413)
    assert result.devices[None].model == "IO Series"


def test_io_series_10_issue_45():
    """IO Series 10 reported as IO Series 6/7 - oralb-ble#45."""
    parser = OralBBluetoothDeviceData()
    result = parser.update(ORALB_IO_SERIES_10_ISSUE_45)
    assert result.devices[None].model == "IO Series"


def test_d21_trizone_5000_ha_142787():
    """TriZone 5000 (D21) reported as Unknown - HA#142787."""
    parser = OralBBluetoothDeviceData()
    result = parser.update(ORALB_D21_TRIZONE_5000_HA_142787)
    assert result.devices[None].model == "Smart Series D21"


def test_sector_resets_when_not_running_issue_63():
    """Sector must report 'no sector' whenever the brush is not actively running.

    Regression test for oralb-ble#63: after the user finishes brushing the
    sensor was stuck on the last sector forever because the parser only
    reset to 'no sector' when brush_time was also zero.
    """
    parser = OralBBluetoothDeviceData()
    # ORALB_DATA_3: state=idle, brush_time=1, sector code=1
    result = parser.update(ORALB_DATA_3)
    sector_key = DeviceKey(key="sector", device_id=None)
    assert result.entity_values[sector_key].native_value == "no sector"
    state_key = DeviceKey(key="toothbrush_state", device_id=None)
    assert result.entity_values[state_key].native_value == "idle"

    # ORALB_IO_SERIES_5_HA_133934: state=off, brush_time=5, sector code=1
    parser = OralBBluetoothDeviceData()
    result = parser.update(ORALB_IO_SERIES_5_HA_133934)
    assert result.entity_values[sector_key].native_value == "no sector"
    assert result.entity_values[state_key].native_value == "off"

    # ORALB_DATA_2: state=running -> sector is reported normally.
    parser = OralBBluetoothDeviceData()
    result = parser.update(ORALB_DATA_2)
    assert result.entity_values[sector_key].native_value == "sector 1"
    assert result.entity_values[state_key].native_value == "running"


def test_start_update_ignores_advertisement_without_oralb_manufacturer():
    """Advertisements from non-Oral-B devices must early-return cleanly.

    Bluetooth scanners often pass every nearby advertisement through the
    parser. When the Oral-B manufacturer ID (0x00DC / 220) is absent the
    parser must skip without populating any sensors or raising.
    """
    parser = OralBBluetoothDeviceData()
    foreign_advertisement = BluetoothServiceInfo(
        name="Some Other Device",
        address="AA:BB:CC:DD:EE:FF",
        rssi=-50,
        manufacturer_data={0x004C: b"\x10\x05\x03\x18\xfe"},  # Apple, not Oral-B
        service_uuids=[],
        service_data={},
        source="local",
    )
    result = parser.update(foreign_advertisement)
    assert result.entity_values == {}
    assert result.binary_entity_values == {}


def test_poll_needed_not_brushing_within_interval_returns_false():
    """When idle and the last poll was recent, no repoll is needed.

    NOT_BRUSHING_UPDATE_INTERVAL_SECONDS is 86400; anything below that
    while idle must keep the radio quiet to spare the device's battery.
    """
    parser = OralBBluetoothDeviceData()
    parser._brushing = False
    parser._last_brush = 0.0
    assert parser.poll_needed(None, 3600) is False


@mock.patch("oralb_ble.parser.time")
def test_poll_needed_not_brushing_after_long_idle_returns_true(mocked_time):
    """After the long idle interval elapses the brush must be polled again.

    Covers the branch where ``time.monotonic() - _last_brush`` exceeds
    TIMEOUT_RECENTLY_BRUSHING (so the long NOT_BRUSHING interval applies)
    and ``last_poll`` is above that long interval.
    """
    parser = OralBBluetoothDeviceData()
    parser._brushing = False
    parser._last_brush = 0.0
    # Push monotonic past TIMEOUT_RECENTLY_BRUSHING so the long interval wins.
    mocked_time.monotonic.return_value = 10_000
    assert parser.poll_needed(None, 86401) is True
