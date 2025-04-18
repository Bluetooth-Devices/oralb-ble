from __future__ import annotations

from unittest import mock

import pytest
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
ORALB_9000_SERIES = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="9000",
    manufacturer_data={220: b"\x03!\x0c\x020\x00\x06\x01\x01\x14\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
# https://github.com/home-assistant/core/issues/81967
ORALB_9000_BLACK_SERIES = BluetoothServiceInfo(
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
ORALB_4000_SERIES = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="4000",
    manufacturer_data={220: b"\x03V\x04\x030\x00\x00\x01\x01\x00\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_6000_SERIES_DAILY_CLEAN_MODE = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="6000",
    manufacturer_data={220: b"\x04'\r\x032\x00\x06\x01\x01\x14\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_6000_SERIES_DAILY_CLEAN_MODE_HIGH_PRESSURE = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="6000",
    manufacturer_data={220: b"\x04'\r\x032\x00\x04\x01\x01\r\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_6000_SERIES_DAILY_CLEAN_MODE_NORMAL_PRESSURE = BluetoothServiceInfo(
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
GENIUS_8000 = BluetoothServiceInfo(
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    name="GENIUS8000",
    manufacturer_data={220: b'\x03"\x0c\x02 \x00\x00\x07\x0f\x00\x04'},
    service_uuids=[],
    service_data={},
    source="local",
)
GENIUS_8000_HIGH_PRESSURE = BluetoothServiceInfo(
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


def test_can_create():
    OralBBluetoothDeviceData()


def test_dataset_1():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_DATA_1
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Smart Series 7000 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Smart Series 7000 48BE",
                model="Smart Series 7000",
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
        title="Smart Series 7000 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Smart Series 7000 48BE",
                model="Smart Series 7000",
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
        title="Smart Series 7000 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Smart Series 7000 48BE",
                model="Smart Series 7000",
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
                native_value="sector " "1",
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
        title="Smart Series 7000 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Smart Series 7000 48BE",
                model="Smart Series 7000",
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
        title="IO Series 6/7 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 6/7 48BE",
                model="IO Series 6/7",
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
        title="IO Series 6/7 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 6/7 48BE",
                model="IO Series 6/7",
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
        title="IO Series 6/7 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 6/7 48BE",
                model="IO Series 6/7",
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
        title="IO Series 6/7 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 6/7 48BE",
                model="IO Series 6/7",
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
        title="IO Series 6/7 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 6/7 48BE",
                model="IO Series 6/7",
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
        title="IO Series 6/7 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 6/7 48BE",
                model="IO Series 6/7",
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
                native_value="sector " "1",
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


def test_9000_series():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_9000_SERIES
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Smart Series 9000/10000 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Smart Series 9000/10000 48BE",
                model="Smart Series 9000/10000",
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
                native_value="sector " "1",
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


def test_9000_black_series():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_9000_BLACK_SERIES
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Smart Series 9000/10000 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Smart Series 9000/10000 48BE",
                model="Smart Series 9000/10000",
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
        title="IO Series 8/9 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 8/9 48BE",
                model="IO Series 8/9",
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


def test_smart_series_4000():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_4000_SERIES
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Smart Series 4000 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Smart Series 4000 48BE",
                model="Smart Series 4000",
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
        title="Triumph V2 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Triumph V2 48BE",
                model="Triumph V2",
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
        title="Triumph V2 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Triumph V2 48BE",
                model="Triumph V2",
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
        title="Pro 6000 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Pro 6000 48BE",
                model="Pro 6000",
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


def test_smart_series_6000_daily_clean_mode():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_6000_SERIES_DAILY_CLEAN_MODE
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Smart Series 6000 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Smart Series 6000 48BE",
                model="Smart Series 6000",
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


def test_smart_series_6000_daily_clean_mode_high_pressure():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_6000_SERIES_DAILY_CLEAN_MODE_HIGH_PRESSURE
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Smart Series 6000 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Smart Series 6000 48BE",
                model="Smart Series 6000",
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


def test_smart_series_6000_daily_clean_mode_normal_pressure():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_6000_SERIES_DAILY_CLEAN_MODE_NORMAL_PRESSURE
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Smart Series 6000 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Smart Series 6000 48BE",
                model="Smart Series 6000",
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
                native_value="off",
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
    service_info = GENIUS_8000
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="Smart Series 8000 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Smart Series 8000 48BE",
                model="Smart Series 8000",
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
    service_info = GENIUS_8000_HIGH_PRESSURE
    result = parser.update(service_info)
    assert parser.brush_modes == SMART_SERIES_MODES
    assert result == SensorUpdate(
        title="Smart Series 8000 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Smart Series 8000 48BE",
                model="Smart Series 8000",
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
        title="IO Series 8/9 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 8/9 48BE",
                model="IO Series 8/9",
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
