import asyncio
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Emonio component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Emonio from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": None,  # Placeholder for the Modbus client
        "entities": [],  # Placeholder for the entities
    }
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    if entry.entry_id in hass.data[DOMAIN]:
        # Close Modbus client connections for all entities
        for entity in hass.data[DOMAIN][entry.entry_id]["entities"]:
            entity.close_connection()

        # Remove the entry from hass.data
        hass.data[DOMAIN].pop(entry.entry_id)

    await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    return True
