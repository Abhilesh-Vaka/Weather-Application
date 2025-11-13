"""Command-line interface for the weather application."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime

from weather_app.api import OpenWeatherClient
from weather_app.config import get_settings
from weather_app.exceptions import ConfigurationError, WeatherAppError


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Get current weather data using the OpenWeatherMap API.",
    )
    parser.add_argument(
        "location",
        help="City name or city,country code (e.g. London or London,UK)",
    )
    parser.add_argument(
        "--units",
        choices=("standard", "metric", "imperial"),
        help="Preferred units system. Defaults to value from configuration.",
    )
    parser.add_argument(
        "--language",
        help="Language code for weather description (default taken from configuration).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    try:
        settings = get_settings(
            units=args.units if args.units else None,
            language=args.language if args.language else None,
        )
    except ConfigurationError as exc:
        print(f"[config] {exc}", file=sys.stderr)
        return 2

    client = OpenWeatherClient(settings=settings)

    try:
        report = client.get_weather(
            args.location,
            units=args.units,
            language=args.language,
        )
    except WeatherAppError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"[input] {exc}", file=sys.stderr)
        return 1

    _print_report(report, units=args.units or settings.units)
    return 0


def _print_report(report, *, units: str) -> None:
    unit_suffix = {
        "standard": "K",
        "metric": "°C",
        "imperial": "°F",
    }[units]
    wind_suffix = {
        "standard": "m/s",
        "metric": "m/s",
        "imperial": "mph",
    }[units]

    local_time = report.timestamp.astimezone()

    print(f"Weather for {report.display_name()} @ {local_time:%Y-%m-%d %H:%M}")
    print("-" * 60)
    print(f"Conditions : {report.description}")
    print(f"Temperature: {report.temperature:.1f}{unit_suffix} (feels like {report.feels_like:.1f}{unit_suffix})")
    print(f"Humidity   : {report.humidity}%")
    print(f"Pressure   : {report.pressure} hPa")
    print(f"Wind Speed : {report.wind_speed:.1f} {wind_suffix}")


if __name__ == "__main__":
    raise SystemExit(main())

