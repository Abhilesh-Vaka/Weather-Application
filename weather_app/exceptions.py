"""Custom exception types for the weather application."""

from __future__ import annotations


class WeatherAppError(Exception):
    """Base class for weather app exceptions."""


class ConfigurationError(WeatherAppError):
    """Raised when required configuration is missing or invalid."""


class WeatherServiceError(WeatherAppError):
    """Raised when the weather service returns an unrecoverable error."""


class NetworkError(WeatherAppError):
    """Raised when network communication fails."""

