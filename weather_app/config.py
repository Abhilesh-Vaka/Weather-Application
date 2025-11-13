"""Configuration utilities for the weather application."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from .exceptions import ConfigurationError

_DEFAULT_UNITS = "metric"
_DEFAULT_LANGUAGE = "en"
_DOTENV_PATHS = (
    Path(".env"),
    Path.home() / ".weather_app" / ".env",
)


def _load_dotenv_files() -> None:
    """Load environment variables from known .env locations."""
    for candidate in _DOTENV_PATHS:
        if candidate.exists():
            load_dotenv(dotenv_path=candidate, override=False)


_load_dotenv_files()


@dataclass(frozen=True)
class Settings:
    """Container for runtime configuration."""

    api_key: str
    units: str = _DEFAULT_UNITS
    language: str = _DEFAULT_LANGUAGE


def get_settings(
    *,
    units: Optional[str] = None,
    language: Optional[str] = None,
) -> Settings:
    """Construct validated settings from environment variables."""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ConfigurationError(
            "Missing OpenWeatherMap API key. "
            "Set the OPENWEATHER_API_KEY environment variable or define it in a .env file."
        )

    resolved_units = _validate_units(units or os.getenv("WEATHER_UNITS", _DEFAULT_UNITS))
    resolved_language = _validate_language(
        language or os.getenv("WEATHER_LANGUAGE", _DEFAULT_LANGUAGE)
    )

    return Settings(api_key=api_key, units=resolved_units, language=resolved_language)


def _validate_units(units: str) -> str:
    allowed = {"standard", "metric", "imperial"}
    if units not in allowed:
        raise ConfigurationError(
            f"Unsupported units '{units}'. Choose from: {', '.join(sorted(allowed))}."
        )
    return units


def _validate_language(language: str) -> str:
    if len(language) < 2 or len(language) > 5:
        raise ConfigurationError(
            "Language should be an ISO-639 code such as 'en' or 'en-US'."
        )
    return language.lower()

