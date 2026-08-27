from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import CONF_CALENDAR_URL, CONF_TOWN, DOMAIN
from .parser import parse_url


class AdaxConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                await self.hass.async_add_executor_job(
                    parse_url, user_input[CONF_CALENDAR_URL]
                )
            except ValueError:
                errors["base"] = "invalid_document"
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                await self.async_set_unique_id(user_input[CONF_TOWN].casefold())
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_TOWN], data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_TOWN): str,
                    vol.Required(CONF_CALENDAR_URL): str,
                }
            ),
            errors=errors,
        )


async def validate_input(hass: HomeAssistant, data: dict) -> None:
    await hass.async_add_executor_job(parse_url, data[CONF_CALENDAR_URL])
