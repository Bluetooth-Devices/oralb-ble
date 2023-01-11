"""Parser for OralB BLE advertisements.

This file is shamelessly copied from the following repository:
https://github.com/Ernst79/bleparser/blob/c42ae922e1abed2720c7fac993777e1bd59c0c93/package/bleparser/oral_b.py

MIT License applies.
"""
from __future__ import annotations

from sensor_state_data import (
    BinarySensorDeviceClass,
    BinarySensorValue,
    DeviceKey,
    SensorDescription,
    SensorDeviceClass,
    SensorDeviceInfo,
    SensorUpdate,
    SensorValue,
    Units,
)

from .const import CHARACTERISTIC_BATTERY, CHARACTERISTIC_MODEL, CHARACTERISTIC_PRESSURE
from .parser import OralBBinarySensor, OralBBluetoothDeviceData, OralBSensor

__version__ = "0.17.0"

__all__ = [
    "OralBSensor",
    "OralBBinarySensor",
    "OralBBluetoothDeviceData",
    "BinarySensorDeviceClass",
    "BinarySensorValue",
    "SensorDescription",
    "SensorDeviceInfo",
    "DeviceKey",
    "SensorUpdate",
    "SensorDeviceClass",
    "SensorDeviceInfo",
    "SensorValue",
    "Units",
    "CHARACTERISTIC_BATTERY",
    "CHARACTERISTIC_MODEL",
    "CHARACTERISTIC_PRESSURE",
]
