from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN

class EmonioModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Emonio Modbus."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Emonio Modbus", data=user_input)

        # Define the data schema with a legend
        data_schema = vol.Schema(
            {
                vol.Required("host", description="Emonio IP"): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors={},
        )

