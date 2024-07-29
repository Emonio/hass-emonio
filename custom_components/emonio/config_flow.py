from homeassistant import config_entries
import voluptuous as vol
import ipaddress
from pymodbus.client.sync import ModbusTcpClient
from scapy.all import ARP, Ether, srp

from .const import DOMAIN

def validate_ip(value):
    """Validate if the value is a valid IP address."""
    try:
        ipaddress.ip_address(value)
        return value
    except ValueError:
        raise vol.Invalid("Invalid IP address")

def get_mac_address(ip_address):
    """Get the MAC address of a device by IP address."""
    try:
        arp_request = ARP(pdst=ip_address)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = srp(arp_request_broadcast, timeout=1, verbose=False)[0]

        for sent, received in answered_list:
            return received.hwsrc

        return None
    except Exception as e:
        _LOGGER.error(f"Error getting MAC address for {ip_address}: {e}")
        return None

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

        def connect_client():
            client = ModbusTcpClient(host, port)
            connection_result = client.connect()
            client.close()
            return connection_result

        def fetch_mac_address():
            return get_mac_address(host)

        connection_result = await self.hass.async_add_executor_job(connect_client)
        if connection_result:
            mac_address = await self.hass.async_add_executor_job(fetch_mac_address)
            if mac_address:
                mac_suffix = mac_address.replace(':', '')[-6:].upper()
                return self.async_create_entry(title=f"Emonio P3 {mac_suffix}", data=user_input)
            else:
                errors["base"] = "Could not get MAC address. Ensure the device is reachable."
        else:
            errors["base"] = "Connection was not possible. Ensure Modbus server is enabled."

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
