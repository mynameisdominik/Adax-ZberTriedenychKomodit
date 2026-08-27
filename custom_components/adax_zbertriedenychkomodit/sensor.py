from __future__ import annotations

import logging
from datetime import date

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import COMMODITIES, CONF_CALENDAR_URL, DOMAIN
from .parser import Collection, parse_url

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = DataUpdateCoordinator(
        hass,
        logger=_LOGGER,
        name=DOMAIN,
        update_method=lambda: hass.async_add_executor_job(
            parse_url, entry.data[CONF_CALENDAR_URL]
        ),
    )
    await coordinator.async_config_entry_first_refresh()
    async_add_entities(
        [AdaxSensor(coordinator, entry, commodity) for commodity in COMMODITIES]
    )


class AdaxSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry: ConfigEntry, commodity: str) -> None:
        super().__init__(coordinator)
        self._commodity = commodity
        self._attr_unique_id = f"{entry.entry_id}_{commodity.casefold()}"
        self._attr_name = commodity
        self._attr_native_unit_of_measurement = "days"

    @property
    def native_value(self) -> int | None:
        upcoming = self._upcoming()
        return (upcoming - date.today()).days if upcoming else None

    @property
    def extra_state_attributes(self) -> dict[str, str | None]:
        upcoming = self._upcoming()
        return {"next_collection": upcoming.isoformat() if upcoming else None}

    def _upcoming(self) -> date | None:
        today = date.today()
        dates = [
            item.date
            for item in self.coordinator.data or []
            if isinstance(item, Collection)
            and item.commodity == self._commodity
            and item.date >= today
        ]
        return min(dates) if dates else None
