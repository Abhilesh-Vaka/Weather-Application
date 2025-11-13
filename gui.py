"""Tkinter graphical interface for the weather application."""

from __future__ import annotations

import threading
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional

from weather_app.api import OpenWeatherClient
from weather_app.config import Settings, get_settings
from weather_app.exceptions import ConfigurationError, WeatherAppError
from weather_app.models import WeatherReport


class WeatherAppGUI(tk.Tk):
    """Tkinter main window for the weather application."""

    def __init__(self, settings: Optional[Settings] = None) -> None:
        super().__init__()
        self.title("Weather App")
        self.resizable(False, False)

        try:
            self._settings = settings or get_settings()
        except ConfigurationError as exc:
            messagebox.showerror("Configuration Error", str(exc))
            raise

        self._client = OpenWeatherClient(settings=self._settings)

        self._location_var = tk.StringVar()
        self._units_var = tk.StringVar(value=self._settings.units)
        self._language_var = tk.StringVar(value=self._settings.language)
        self._status_var = tk.StringVar(value="Enter a city and click Fetch.")

        self._build_widgets()

    def _build_widgets(self) -> None:
        padding = {"padx": 10, "pady": 5}

        frm = ttk.Frame(self)
        frm.grid(row=0, column=0, sticky="NSEW")

        ttk.Label(frm, text="City or City,Country Code").grid(row=0, column=0, sticky="W", **padding)
        city_entry = ttk.Entry(frm, textvariable=self._location_var, width=30)
        city_entry.grid(row=0, column=1, **padding)
        city_entry.focus()

        ttk.Label(frm, text="Units").grid(row=1, column=0, sticky="W", **padding)
        units_combo = ttk.Combobox(
            frm,
            textvariable=self._units_var,
            values=("standard", "metric", "imperial"),
            state="readonly",
        )
        units_combo.grid(row=1, column=1, sticky="EW", **padding)

        ttk.Label(frm, text="Language").grid(row=2, column=0, sticky="W", **padding)
        language_entry = ttk.Entry(frm, textvariable=self._language_var, width=10)
        language_entry.grid(row=2, column=1, sticky="W", **padding)

        fetch_button = ttk.Button(frm, text="Fetch Weather", command=self._on_fetch_clicked)
        fetch_button.grid(row=3, column=0, columnspan=2, **padding)
        self._fetch_button = fetch_button

        separator = ttk.Separator(frm)
        separator.grid(row=4, column=0, columnspan=2, sticky="EW", pady=(5, 10))

        result_frame = ttk.Frame(frm)
        result_frame.grid(row=5, column=0, columnspan=2, sticky="NSEW")

        self._result_text = tk.Text(result_frame, width=50, height=10, state="disabled")
        self._result_text.pack(fill="both", expand=True)

        status_label = ttk.Label(self, textvariable=self._status_var, relief="sunken", anchor="w")
        status_label.grid(row=1, column=0, sticky="EW", padx=5, pady=(0, 5))

    def _on_fetch_clicked(self) -> None:
        location = self._location_var.get().strip()
        if not location:
            messagebox.showwarning("Input Required", "Please enter a location.")
            return

        self._set_loading_state(True)
        thread = threading.Thread(
            target=self._fetch_weather_thread,
            args=(location, self._units_var.get(), self._language_var.get()),
            daemon=True,
        )
        thread.start()

    def _fetch_weather_thread(self, location: str, units: str, language: str) -> None:
        try:
            report = self._client.get_weather(location, units=units, language=language)
        except WeatherAppError as exc:
            self.after(0, lambda: self._handle_error(str(exc)))
        except ValueError as exc:
            self.after(0, lambda: self._handle_error(str(exc)))
        else:
            self.after(0, lambda: self._display_report(report, units))
        finally:
            self.after(0, lambda: self._set_loading_state(False))

    def _handle_error(self, message: str) -> None:
        self._status_var.set(f"Error: {message}")
        messagebox.showerror("Weather Error", message)

    def _display_report(self, report: WeatherReport, units: str) -> None:
        unit_suffix = {
            "standard": "K",
            "metric": "°C",
            "imperial": "°F",
        }.get(units, "units")

        wind_suffix = {
            "standard": "m/s",
            "metric": "m/s",
            "imperial": "mph",
        }.get(units, "m/s")

        local_time = report.timestamp.astimezone()
        lines = [
            f"Weather for {report.display_name()}",
            f"Observed: {local_time:%Y-%m-%d %H:%M}",
            f"Conditions: {report.description}",
            f"Temperature: {report.temperature:.1f}{unit_suffix}",
            f"Feels Like: {report.feels_like:.1f}{unit_suffix}",
            f"Humidity: {report.humidity}%",
            f"Pressure: {report.pressure} hPa",
            f"Wind Speed: {report.wind_speed:.1f} {wind_suffix}",
        ]

        self._result_text.configure(state="normal")
        self._result_text.delete("1.0", tk.END)
        self._result_text.insert(tk.END, "\n".join(lines))
        self._result_text.configure(state="disabled")
        self._status_var.set("Weather data updated successfully.")

    def _set_loading_state(self, is_loading: bool) -> None:
        self._fetch_button.configure(state="disabled" if is_loading else "normal")
        self._status_var.set("Fetching weather data..." if is_loading else "Ready.")


def main() -> None:
    app = WeatherAppGUI()
    app.mainloop()


if __name__ == "__main__":
    main()

