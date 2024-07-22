from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    UnitOfEnergy,
    UnitOfPower,
)
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from homeassistant.helpers.device_registry import DeviceEntryType
from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=5)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Emonio Modbus sensor platform."""
    host = config_entry.data["host"]
    port = config_entry.data.get("port", 502)

    device_info = {
        "identifiers": {(DOMAIN, host)},
        "name": "Emonio Modbus Device",
        "model": "Emonio P3",
        "manufacturer": "Berliner Energie Institut",
    }

    # Define your sensors here
    sensors = [
        EmonioModbusSensor(
            name="Emonio_Total_Power",
            unit_of_measurement=UnitOfPower.WATT,
            address=304,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            host=host,
            port=port,
            unique_id="emonio_total_power",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Total_Energy",
            unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            address=312,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL_INCREASING,
            hub_name="modbus_hub",
            host=host,
            port=port,
            unique_id="emonio_total_energy",
            device_info=device_info,
        ),
    ]
    async_add_entities(sensors, True)

class EmonioModbusSensor(SensorEntity):
    def __init__(self, name, unit_of_measurement, address, data_type, swap, device_class, state_class, hub_name, host, port, unique_id, device_info):
        self._name = name
        self._unit_of_measurement = unit_of_measurement
        self._address = address
        self._data_type = data_type
        self._swap = swap
        self._device_class = device_class
        self._state_class = state_class
        self._hub_name = hub_name
        self._host = host
        self._port = port
        self._state = None
        self._unique_id = unique_id
        self._device_info = device_info
        self._client = ModbusTcpClient(host, port)

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

    @property
    def device_class(self):
        return self._device_class

    @property
    def state_class(self):
        return self._state_class

    @property
    def state(self):
        return self._state

    @property
    def device_info(self):
        return self._device_info

    async def async_update(self):
        """Fetch new state data for the sensor."""
        try:
            self._client.connect()
            result = self._client.read_holding_registers(self._address, 2, unit=1)
            if result.isError():
                return

            registers = result.registers
            if self._swap == 'word':
                registers.reverse()

            decoder = BinaryPayloadDecoder.fromRegisters(
                registers, 
                byteorder=Endian.Big
            )
            raw_value = decoder.decode_32bit_float()
            self._state = round(raw_value, 2)  # Format to two decimal places
        except Exception as e:
            # Log the error
            self._state = self._state  # Retain the last known value
        finally:
            self._client.close()

