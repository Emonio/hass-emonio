import voluptuous as vol
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    UnitOfEnergy,
    UnitOfPower,
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
    UnitOfFrequency,
    POWER_VOLT_AMPERE_REACTIVE,
    UnitOfApparentPower
)
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers import config_validation as cv
import logging
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=5)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: cv.config_entry_only_config_schema,
}, extra=vol.ALLOW_EXTRA)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Emonio Modbus sensor platform."""
    host = config_entry.data["host"]
    port = config_entry.data.get("port", 502)

    device_info = {
        "identifiers": {(DOMAIN, host)},
        "name": "Emonio P3 caca",
        "model": "Emonio P3 pedo",
        "manufacturer": "Berliner Energie Institut",
    }

    # Create a shared Modbus client
    modbus_client = ModbusTcpClient(host, port)

    # Sensors definitions
    sensors = [
        EmonioModbusSensor(
            name="Emonio_Phase_A_Voltage",
            unit_of_measurement=UnitOfElectricPotential.VOLT,
            address=0,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_a_voltage",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_B_Voltage",
            unit_of_measurement=UnitOfElectricPotential.VOLT,
            address=100,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_b_voltage",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_C_Voltage",
            unit_of_measurement=UnitOfElectricPotential.VOLT,
            address=200,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_c_voltage",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Total_Voltage",
            unit_of_measurement=UnitOfElectricPotential.VOLT,
            address=300,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.VOLTAGE,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_total_voltage",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_A_Power",
            unit_of_measurement=UnitOfPower.WATT,
            address=4,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_a_power",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_B_Power",
            unit_of_measurement=UnitOfPower.WATT,
            address=104,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_b_power",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_C_Power",
            unit_of_measurement=UnitOfPower.WATT,
            address=204,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_c_power",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Total_Power",
            unit_of_measurement=UnitOfPower.WATT,
            address=304,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.POWER,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_total_power",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_A_Energy",
            unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            address=12,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_a_energy",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_B_Energy",
            unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            address=112,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_b_energy",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_C_Energy",
            unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            address=212,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_c_energy",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Total_Energy",
            unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
            address=312,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.ENERGY,
            state_class=SensorStateClass.TOTAL,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_total_energy",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_A_Current",
            unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            address=2,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_a_current",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_B_Current",
            unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            address=102,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_b_current",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_C_Current",
            unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            address=202,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_c_current",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Total_Current",
            unit_of_measurement=UnitOfElectricCurrent.AMPERE,
            address=302,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.CURRENT,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_total_current",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_A_Apparent_Power_Reactive",
            unit_of_measurement=POWER_VOLT_AMPERE_REACTIVE,
            address=6,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.REACTIVE_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_a_apparent_power_reactive",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_B_Apparent_Power_Reactive",
            unit_of_measurement=POWER_VOLT_AMPERE_REACTIVE,
            address=106,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.REACTIVE_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_b_apparent_power_reactive",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_C_Apparent_Power_Reactive",
            unit_of_measurement=POWER_VOLT_AMPERE_REACTIVE,
            address=206,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.REACTIVE_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_c_apparent_power_reactive",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Total_Apparent_Power_Reactive",
            unit_of_measurement=POWER_VOLT_AMPERE_REACTIVE,
            address=306,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.REACTIVE_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_total_apparent_power_reactive",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_A_Apparent_Power",
            unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
            address=8,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.APPARENT_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_a_apparent_power",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_B_Apparent_Power",
            unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
            address=108,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.APPARENT_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_b_apparent_power",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_C_Apparent_Power",
            unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
            address=208,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.APPARENT_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_c_apparent_power",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Total_Apparent_Power",
            unit_of_measurement=UnitOfApparentPower.VOLT_AMPERE,
            address=308,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.APPARENT_POWER,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_total_apparent_power",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_A_Frequency",
            unit_of_measurement=UnitOfFrequency.HERTZ,
            address=10,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.FREQUENCY,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_a_frequency",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_B_Frequency",
            unit_of_measurement=UnitOfFrequency.HERTZ,
            address=110,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.FREQUENCY,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_b_frequency",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_C_Frequency",
            unit_of_measurement=UnitOfFrequency.HERTZ,
            address=210,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.FREQUENCY,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_c_frequency",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Total_Frequency",
            unit_of_measurement=UnitOfFrequency.HERTZ,
            address=310,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.FREQUENCY,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_total_frequency",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_A_Power_Factor",
            unit_of_measurement="%",
            address=14,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.POWER_FACTOR,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_a_power_factor",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_B_Power_Factor",
            unit_of_measurement="%",
            address=114,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.POWER_FACTOR,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_b_power_factor",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Phase_C_Power_Factor",
            unit_of_measurement="%",
            address=214,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.POWER_FACTOR,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_phase_c_power_factor",
            device_info=device_info,
        ),
        EmonioModbusSensor(
            name="Emonio_Total_Power_Factor",
            unit_of_measurement="%",
            address=314,
            data_type="float32",
            swap="word",
            device_class=SensorDeviceClass.POWER_FACTOR,
            state_class=SensorStateClass.MEASUREMENT,
            hub_name="modbus_hub",
            modbus_client=modbus_client,
            unique_id="emonio_total_power_factor",
            device_info=device_info,
        ),
    ]
    async_add_entities(sensors, True)

class EmonioModbusSensor(SensorEntity):
    def __init__(self, name, unit_of_measurement, address, data_type, swap, device_class, state_class, hub_name, modbus_client, unique_id, device_info):
        self._name = name
        self._unit_of_measurement = unit_of_measurement
        self._address = address
        self._data_type = data_type
        self._swap = swap
        self._device_class = device_class
        self._state_class = state_class
        self._hub_name = hub_name
        self._modbus_client = modbus_client
        self._state = None
        self._unique_id = unique_id
        self._device_info = device_info

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
            if not self._modbus_client.is_socket_open():
                self._modbus_client.connect()

            result = self._modbus_client.read_holding_registers(self._address, 2, unit=1)
            if result.isError():
                _LOGGER.error(f"Error reading {self._name} at address {self._address}")
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
            _LOGGER.error(f"Error updating {self._name}: {e}")
            self._state = self._state  # Retain the last known value
        finally:
            # Do not close the client to keep the connection persistent
            pass