# Streamlit Weather App - Deployment Guide

## 🚀 Running Locally

### Step 1: Activate Virtual Environment
```powershell
cd "C:\Users\NAGESWARARAO VAKA\Desktop\Weather App"
.\.venv\Scripts\Activate.ps1
```

### Step 2: Run Streamlit App
```powershell
streamlit run streamlit_app.py
```

The app will automatically open in your browser at `http://localhost:8501`

---

## 🌐 Deploying to Streamlit Cloud (Free)

### Option 1: Deploy via Streamlit Cloud Website

1. **Push your code to GitHub**
   - Create a new repository on GitHub
   - Push your code:
     ```powershell
     git init
     git add .
     git commit -m "Initial commit: Weather App with Streamlit"
     git remote add origin https://github.com/yourusername/weather-app.git
     git push -u origin main
     ```

2. **Deploy on Streamlit Cloud**
   - Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set **Main file path**: `streamlit_app.py`
   - Click "Deploy!"

3. **Add Environment Variables**
   - In Streamlit Cloud dashboard, go to your app settings
   - Click "Secrets" tab
   - Add your API key:
     ```toml
     OPENWEATHER_API_KEY = "your_api_key_here"
     ```
   - Optionally add:
     ```toml
     WEATHER_UNITS = "metric"
     WEATHER_LANGUAGE = "en"
     ```

### Option 2: Deploy via Streamlit CLI

```powershell
streamlit login
streamlit deploy streamlit_app.py
```

---

## 🔐 Environment Variables for Deployment

### For Streamlit Cloud (Secrets)
Create a `.streamlit/secrets.toml` file (or use the Secrets tab in Streamlit Cloud):
```toml
OPENWEATHER_API_KEY = "your_api_key_here"
WEATHER_UNITS = "metric"
WEATHER_LANGUAGE = "en"
```

### For Local Development
Use your existing `.env` file:
```
OPENWEATHER_API_KEY=your_api_key_here
WEATHER_UNITS=metric
WEATHER_LANGUAGE=en
```

---

## 📦 Required Files for Deployment

Make sure these files are in your repository:
- ✅ `streamlit_app.py` - Main Streamlit application
- ✅ `weather_app/` - Python package with API client
- ✅ `requirements.txt` - All dependencies
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ `.env` or `.streamlit/secrets.toml` - API key (don't commit `.env` to GitHub!)

---

## 🎯 Features of the Streamlit App

- ✨ **Beautiful UI** with gradient headers and card-based layout
- 🔍 **Interactive Search** with city/country code support
- 📊 **Real-time Weather Data** with emoji icons
- ⚙️ **Customizable Settings** (units, language) in sidebar
- 📚 **Search History** - Quick access to recent searches
- 🔄 **Refresh Button** - Update current weather
- 📱 **Responsive Design** - Works on desktop and mobile
- 🎨 **Modern Styling** - Custom CSS with gradients and animations

---

## 🐛 Troubleshooting

### App won't start
- Make sure virtual environment is activated
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify API key is set in `.env` file

### API Key Error
- Ensure `OPENWEATHER_API_KEY` is set in `.env` or Streamlit Cloud secrets
- Wait 10-60 minutes if you just created a new API key

### Port Already in Use
- Change port: `streamlit run streamlit_app.py --server.port 8502`
- Or stop other Streamlit instances

---

## 📝 Quick Commands

```powershell
# Run locally
streamlit run streamlit_app.py

# Run on custom port
streamlit run streamlit_app.py --server.port 8502

# View app in browser automatically
streamlit run streamlit_app.py --server.headless false

# Clear cache and rerun
streamlit run streamlit_app.py --server.runOnSave true
```

---

## 🌟 Next Steps

- Add weather forecast (5-day/3-hour)
- Add weather maps/charts
- Add location-based search (GPS)
- Add weather alerts/notifications
- Add multiple city comparison

---

**Happy Weather Tracking! ☀️🌧️⛈️❄️**

