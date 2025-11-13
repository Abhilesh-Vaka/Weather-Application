"""Flask-powered interactive frontend for the weather application."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict

from flask import Flask, jsonify, render_template, request

from weather_app.api import OpenWeatherClient
from weather_app.config import ConfigurationError, get_settings
from weather_app.exceptions import WeatherAppError

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")


def _serialize_report(report) -> Dict[str, Any]:
    data = asdict(report)
    timestamp = report.timestamp.astimezone()
    data.update(
        {
            "display_name": report.display_name(),
            "timestamp_iso": timestamp.isoformat(),
            "timestamp_local": timestamp.strftime("%Y-%m-%d %H:%M"),
        }
    )
    return data


@app.route("/")
def index() -> str:
    try:
        settings = get_settings()
    except ConfigurationError as exc:
        warning = str(exc)
        settings = None
    else:
        warning = None

    return render_template(
        "index.html",
        default_units=settings.units if settings else "metric",
        default_language=settings.language if settings else "en",
        warning=warning,
    )


@app.route("/api/weather")
def weather_api():
    location = request.args.get("location", "").strip()
    units = request.args.get("units") or None
    language = request.args.get("language") or None

    if not location:
        return jsonify({"error": "Location query is required."}), 400

    try:
        settings = get_settings(units=units, language=language)
    except ConfigurationError as exc:
        return jsonify({"error": str(exc)}), 400

    client = OpenWeatherClient(settings=settings)

    try:
        report = client.get_weather(location, units=units, language=language)
    except WeatherAppError as exc:
        return jsonify({"error": str(exc)}), 502
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"data": _serialize_report(report)})


if __name__ == "__main__":
    app.run(debug=True)

