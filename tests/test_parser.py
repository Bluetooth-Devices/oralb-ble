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

from oralb_ble.parser import OralBBluetoothDeviceData

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
ORALB_IO_SERIES_7 = BluetoothServiceInfo(
    name="78:DB:2F:C2:48:BE",
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    manufacturer_data={220: b"\x062k\x02 \x00\x01\x01\x01\x03\x04"},
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
                native_value="sector " "1",
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
                native_value="unknown " "pressure " "32",
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
                native_value="unknown " "pressure " "0",
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
                native_value="unknown " "pressure " "0",
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
                native_value="unknown " "pressure " "32",
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


def test_io_series_7():
    parser = OralBBluetoothDeviceData()
    service_info = ORALB_IO_SERIES_7
    result = parser.update(service_info)
    assert result == SensorUpdate(
        title="IO Series 7/8 48BE",
        devices={
            None: SensorDeviceInfo(
                name="IO Series 7/8 48BE",
                model="IO Series 7/8",
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
                native_value="unknown " "pressure " "32",
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
        title="Smart Series 9000 48BE",
        devices={
            None: SensorDeviceInfo(
                name="Smart Series 9000 48BE",
                model="Smart Series 9000",
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
                native_value="unknown " "pressure " "48",
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
