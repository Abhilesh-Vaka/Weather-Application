"""Interactive Streamlit web application for weather data."""

from __future__ import annotations

import streamlit as st
from streamlit import session_state

from weather_app.api import OpenWeatherClient
from weather_app.config import Settings, get_settings
from weather_app.exceptions import ConfigurationError, NetworkError, WeatherAppError, WeatherServiceError


# Page configuration
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling
st.markdown(
    """
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        margin: 0;
        font-size: 3rem;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    .weather-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .temperature-display {
        font-size: 4rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.4);
    }
    .error-box {
        background: #fee;
        border-left: 4px solid #f00;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-box {
        background: #efe;
        border-left: 4px solid #0a0;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_session_state() -> None:
    """Initialize session state variables."""
    if "weather_client" not in session_state:
        try:
            settings = get_settings()
            session_state.weather_client = OpenWeatherClient(settings=settings)
            session_state.settings = settings
        except ConfigurationError as exc:
            st.error(f"Configuration Error: {exc}")
            st.stop()

    if "search_history" not in session_state:
        session_state.search_history = []

    if "last_result" not in session_state:
        session_state.last_result = None


def get_weather_emoji(icon_code: str | None) -> str:
    """Map OpenWeatherMap icon codes to emojis."""
    if not icon_code:
        return "🌤️"
    
    icon_map = {
        "01d": "☀️",  # clear sky day
        "01n": "🌙",  # clear sky night
        "02d": "⛅",  # few clouds day
        "02n": "☁️",  # few clouds night
        "03d": "☁️",  # scattered clouds
        "03n": "☁️",
        "04d": "☁️",  # broken clouds
        "04n": "☁️",
        "09d": "🌧️",  # shower rain
        "09n": "🌧️",
        "10d": "🌦️",  # rain day
        "10n": "🌧️",  # rain night
        "11d": "⛈️",  # thunderstorm
        "11n": "⛈️",
        "13d": "❄️",  # snow
        "13n": "❄️",
        "50d": "🌫️",  # mist
        "50n": "🌫️",
    }
    return icon_map.get(icon_code, "🌤️")


def format_temperature(temp: float, units: str) -> tuple[str, str]:
    """Format temperature with appropriate unit symbol."""
    unit_map = {
        "metric": ("°C", "m/s"),
        "imperial": ("°F", "mph"),
        "standard": ("K", "m/s"),
    }
    temp_unit, wind_unit = unit_map.get(units, ("°C", "m/s"))
    return f"{temp:.1f}{temp_unit}", wind_unit


def display_weather_result(report, units: str) -> None:
    """Display weather results in a beautiful format."""
    temp_str, wind_unit = format_temperature(report.temperature, units)
    feels_like_str, _ = format_temperature(report.feels_like, units)
    
    emoji = get_weather_emoji(report.icon)
    
    # Header with location and emoji
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"""
            <div style="text-align: center;">
                <h1 style="font-size: 3rem; margin: 0;">{emoji}</h1>
                <h2>{report.display_name()}</h2>
                <p style="color: #666;">{report.description}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # Temperature display
    st.markdown(
        f'<div class="temperature-display">{temp_str}</div>',
        unsafe_allow_html=True,
    )
    
    # Main metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Feels Like</div>
                <div class="metric-value">{feels_like_str}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Humidity</div>
                <div class="metric-value">{report.humidity}%</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Pressure</div>
                <div class="metric-value">{report.pressure} hPa</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Wind Speed</div>
                <div class="metric-value">{report.wind_speed:.1f} {wind_unit}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # Additional info
    local_time = report.timestamp.astimezone()
    st.info(f"📅 Last updated: {local_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")


def main() -> None:
    """Main application entry point."""
    initialize_session_state()
    
    # Header
    st.markdown(
        """
        <div class="main-header">
            <h1>☀️ Weather Dashboard</h1>
            <p>Real-time weather conditions, beautifully presented • Done by Jagadeeshwari</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        units = st.selectbox(
            "Temperature Units",
            options=["metric", "imperial", "standard"],
            index=["metric", "imperial", "standard"].index(session_state.settings.units),
        )
        
        language = st.text_input(
            "Language Code",
            value=session_state.settings.language,
            help="ISO-639 code (e.g., 'en', 'es', 'fr')",
            max_chars=5,
        )
        
        st.divider()
        
        # Search history
        st.subheader("📚 Recent Searches")
        if session_state.search_history:
            for idx, location in enumerate(reversed(session_state.search_history[-10:])):
                if st.button(f"📍 {location}", key=f"history_{idx}", use_container_width=True):
                    st.session_state.location_input = location
                    st.rerun()
            
            if st.button("🗑️ Clear History", use_container_width=True):
                session_state.search_history = []
                st.rerun()
        else:
            st.info("No search history yet.")
    
    # Main content area
    st.header("🔍 Search Weather")
    
    # Search form
    with st.form("weather_search_form"):
        location = st.text_input(
            "Enter City or City,Country Code",
            value=st.session_state.get("location_input", ""),
            placeholder="e.g., Hyderabad,IN or London,UK",
            help="Enter a city name. For better results, include country code (e.g., 'New York,US')",
        )
        
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button("🌤️ Get Weather", use_container_width=True)
        with col2:
            if session_state.last_result:
                refresh_button = st.form_submit_button("🔄 Refresh", use_container_width=True)
            else:
                refresh_button = False
        
        if submit_button or refresh_button:
            if not location.strip() and not refresh_button:
                st.warning("⚠️ Please enter a location to search.")
            else:
                query = location.strip() if location.strip() else session_state.last_result.display_name()
                
                with st.spinner("🌍 Fetching weather data..."):
                    try:
                        report = session_state.weather_client.get_weather(
                            query,
                            units=units,
                            language=language if language else None,
                        )
                        
                        session_state.last_result = report
                        
                        # Add to search history
                        location_name = report.display_name()
                        if location_name not in session_state.search_history:
                            session_state.search_history.append(location_name)
                        
                        st.success("✅ Weather data retrieved successfully!")
                        display_weather_result(report, units)
                        
                    except WeatherServiceError as exc:
                        st.error(f"❌ API Error: {exc}")
                    except NetworkError as exc:
                        st.error(f"🌐 Network Error: {exc}")
                    except ValueError as exc:
                        st.error(f"⚠️ Invalid Input: {exc}")
                    except WeatherAppError as exc:
                        st.error(f"❌ Error: {exc}")
                    except Exception as exc:
                        st.error(f"❌ Unexpected Error: {exc}")
                        st.exception(exc)
    
    # Display last result if available and no new search
    if session_state.last_result and not submit_button and not refresh_button:
        st.divider()
        st.subheader("📊 Current Weather")
        display_weather_result(session_state.last_result, units)
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style="text-align: center; color: #666; padding: 2rem 0;">
            <p>Powered by <strong>OpenWeatherMap</strong> • Built with ❤️ using Streamlit</p>
            <p style="font-size: 0.8rem;">Done by Jagadeeshwari</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

