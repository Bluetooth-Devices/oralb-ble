from bluetooth_sensor_state_data import BluetoothServiceInfo, DeviceClass, SensorUpdate
from sensor_state_data import (
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
    device_name="78:DB:2F:C2:48:BE",
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    manufacturer_data={220: b"\x02\x01\x08\x02 \x00\x00\x01\x01\x00\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_DATA_2 = BluetoothServiceInfo(
    device_name="78:DB:2F:C2:48:BE",
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    manufacturer_data={220: b"\x02\x01\x08\x03\x00\x00\x00\x01\x01\x00\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_DATA_3 = BluetoothServiceInfo(
    device_name="78:DB:2F:C2:48:BE",
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    manufacturer_data={220: b"\x02\x01\x08\x02\x00\x00\x01\x01\x01\x03\x04"},
    service_uuids=[],
    service_data={},
    source="local",
)
ORALB_DATA_4 = BluetoothServiceInfo(
    device_name="78:DB:2F:C2:48:BE",
    address="78:DB:2F:C2:48:BE",
    rssi=-63,
    manufacturer_data={220: b"\x02\x01\x08\x02 \x00\x01\x01\x01\x03\x04"},
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
        title=None,
        devices={
            None: SensorDeviceInfo(
                name="H5052 E81B",
                model="H5052",
                manufacturer="OralB",
                sw_version=None,
                hw_version=None,
            )
        },
        entity_descriptions={
            DeviceKey(key="temperature", device_id=None): SensorDescription(
                device_key=DeviceKey(key="temperature", device_id=None),
                device_class=DeviceClass.TEMPERATURE,
                native_unit_of_measurement=Units.TEMP_CELSIUS,
            ),
            DeviceKey(key="humidity", device_id=None): SensorDescription(
                device_key=DeviceKey(key="humidity", device_id=None),
                device_class=DeviceClass.HUMIDITY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="battery", device_id=None): SensorDescription(
                device_key=DeviceKey(key="battery", device_id=None),
                device_class=DeviceClass.BATTERY,
                native_unit_of_measurement=Units.PERCENTAGE,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorDescription(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                device_class=DeviceClass.SIGNAL_STRENGTH,
                native_unit_of_measurement=Units.SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
            ),
        },
        entity_values={
            DeviceKey(key="temperature", device_id=None): SensorValue(
                device_key=DeviceKey(key="temperature", device_id=None),
                name="Temperature",
                native_value=2.84,
            ),
            DeviceKey(key="humidity", device_id=None): SensorValue(
                device_key=DeviceKey(key="humidity", device_id=None),
                name="Humidity",
                native_value=52.87,
            ),
            DeviceKey(key="battery", device_id=None): SensorValue(
                device_key=DeviceKey(key="battery", device_id=None),
                name="Battery",
                native_value=59,
            ),
            DeviceKey(key="signal_strength", device_id=None): SensorValue(
                device_key=DeviceKey(key="signal_strength", device_id=None),
                name="Signal Strength",
                native_value=-63,
            ),
        },
    )
