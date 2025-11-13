"""Data models for the weather application."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass(frozen=True)
class WeatherReport:
    """Represents a normalized weather report."""

    city: str
    country: str
    description: str
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    wind_speed: float
    icon: str | None
    timestamp: datetime

    @classmethod
    def from_openweather(cls, payload: Dict[str, Any]) -> "WeatherReport":
        """Convert an OpenWeatherMap API response into a WeatherReport."""
        sys_block = payload.get("sys", {})
        weather_block = (payload.get("weather") or [{}])[0]
        main_block = payload.get("main", {})
        wind_block = payload.get("wind", {})

        return cls(
            city=payload.get("name", "Unknown location"),
            country=sys_block.get("country", ""),
            description=weather_block.get("description", "n/a").title(),
            temperature=float(main_block.get("temp", 0.0)),
            feels_like=float(main_block.get("feels_like", 0.0)),
            humidity=int(main_block.get("humidity", 0)),
            pressure=int(main_block.get("pressure", 0)),
            wind_speed=float(wind_block.get("speed", 0.0)),
            icon=weather_block.get("icon"),
            timestamp=datetime.fromtimestamp(payload.get("dt", 0), tz=timezone.utc),
        )

    def display_name(self) -> str:
        """Compose a human-friendly location label."""
        if self.country:
            return f"{self.city}, {self.country}"
        return self.city

