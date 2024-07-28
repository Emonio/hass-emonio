from homeassistant import config_entries
import voluptuous as vol
import ipaddress
from pymodbus.client.sync import ModbusTcpClient

from .const import DOMAIN

def validate_ip(value):
    """Validate if the value is a valid IP address."""
    try:
        ipaddress.ip_address(value)
        return value
    except ValueError:
        raise vol.Invalid("Invalid IP address")

class EmonioModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Emonio Modbus."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate the IP address here
            try:
                validate_ip(user_input['host'])
                return await self.async_step_test_connection(user_input)
            except vol.Invalid:
                errors["host"] = "Invalid IP address. Check your Emonio IP."

        # Define the data schema with a legend and IP validation
        data_schema = vol.Schema(
            {
                vol.Required("host", description="Emonio IP"): str,
                vol.Required("port", default=502, description="Modbus Port"): int,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_test_connection(self, user_input):
        """Test the connection to the Modbus device."""
        errors = {}
        host = user_input['host']
        port = user_input['port']

        client = ModbusTcpClient(host, port)
        if client.connect():
            client.close()
            return self.async_create_entry(title=f"Emonio P3 {host}", data=user_input)
        else:
            errors["base"] = "Connection was not possible. Ensure Modbus server is enabled."
            client.close()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("host", description="Emonio IP"): str,
                    vol.Required("port", default=502, description="Modbus Port"): int,
                }
            ),
            errors=errors,
        )