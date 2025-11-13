## Weather App

Python weather application providing both a CLI and a Tkinter GUI powered by the OpenWeatherMap API.

### Features
- Real-time weather lookups via OpenWeatherMap.
- Secure API key management with environment variables or `.env`.
- Robust validation and error handling for network issues and bad inputs.
- Modular, object-oriented design with reusable client and models.
- Tkinter GUI with responsive worker thread to keep the UI reactive.

### Getting Started
1. **Install dependencies**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # PowerShell
   pip install -r requirements.txt
   ```
2. **Configure API credentials**
   - Obtain an API key from [https://openweathermap.org/api](https://openweathermap.org/api).
   - Set the `OPENWEATHER_API_KEY` environment variable, or create a `.env` file in the project root containing:
     ```
     OPENWEATHER_API_KEY=your_api_key_here
     ```
   - Optional settings:
     ```
     WEATHER_UNITS=metric   # or imperial, standard
     WEATHER_LANGUAGE=en    # ISO-639 code
     ```

### Usage
#### CLI
```bash
python cli.py "London,UK" --units metric
```

#### GUI
```bash
python main.py --mode gui
```

#### Unified launcher
```bash
python main.py --mode cli "San Francisco,US"
```

#### Interactive Web Frontend (Flask)
```bash
python web_app.py
```
- Visit `http://127.0.0.1:5000/` in your browser.
- Enjoy the animated dashboard with search history and live updates.

#### Streamlit Web App (Recommended for Deployment)
```bash
streamlit run streamlit_app.py
```
- Automatically opens in your browser at `http://localhost:8501`
- Beautiful, interactive UI with sidebar settings
- Search history, refresh functionality, and real-time updates
- Perfect for deployment to Streamlit Cloud (free hosting)

### Project Structure
- `weather_app/` reusable modules (`api`, `config`, `models`, `exceptions`).
- `cli.py` command-line interface.
- `gui.py` Tkinter GUI.
- `main.py` unified launcher.
- `web_app.py` Flask app serving the interactive frontend.
- `streamlit_app.py` Streamlit web application (recommended for deployment).
- `frontend/` HTML, CSS, and JavaScript assets for the Flask web experience.
- `.streamlit/` Streamlit configuration files.

### Deployment

**Streamlit Cloud (Free Hosting)**
- See `STREAMLIT_DEPLOYMENT.md` for detailed deployment instructions
- Push to GitHub and deploy in minutes
- Free hosting with automatic updates

### Development Notes
- Network failures and API errors raise descriptive exceptions that surface in the UI/CLI.
- Configuration validation ensures unit and language codes are valid.
- GUI fetches data on a background thread to avoid blocking the Tkinter event loop.
- Streamlit app uses session state for search history and caching.

