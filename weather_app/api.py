"""Client for interacting with the OpenWeatherMap API."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import requests
from requests import Response

from .config import Settings, get_settings
from .exceptions import NetworkError, WeatherServiceError
from .models import WeatherReport

_logger = logging.getLogger(__name__)
_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
_DEFAULT_TIMEOUT = 10  # seconds


class OpenWeatherClient:
    """Typed interface to the OpenWeatherMap current weather endpoint."""

    def __init__(
        self,
        *,
        settings: Optional[Settings] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self._settings = settings or get_settings()
        self._session = session or requests.Session()

    def get_weather(
        self,
        query: str,
        *,
        units: Optional[str] = None,
        language: Optional[str] = None,
    ) -> WeatherReport:
        """Fetch weather for the provided city or geographic query."""
        if not query or not query.strip():
            raise ValueError("Location query must be a non-empty string.")

        params = {
            "q": query.strip(),
            "appid": self._settings.api_key,
            "units": units or self._settings.units,
            "lang": language or self._settings.language,
        }

        try:
            response = self._session.get(_BASE_URL, params=params, timeout=_DEFAULT_TIMEOUT)
        except requests.RequestException as exc:
            _logger.exception("Network failure while fetching weather data.")
            raise NetworkError("Unable to reach the OpenWeatherMap service.") from exc

        payload = self._parse_response(response)
        return WeatherReport.from_openweather(payload)

    @staticmethod
    def _parse_response(response: Response) -> Dict[str, Any]:
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            try:
                payload: Dict[str, Any] = response.json()
            except ValueError:
                payload = {}

            message = payload.get("message") or response.reason
            raise WeatherServiceError(
                f"OpenWeatherMap request failed [{response.status_code}]: {message}"
            ) from exc

        try:
            return response.json()
        except ValueError as exc:
            raise WeatherServiceError("OpenWeatherMap returned invalid JSON.") from exc

