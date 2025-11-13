# How to Add Your OpenWeatherMap API Key - Step by Step Guide

## Step 1: Get Your API Key from OpenWeatherMap

1. **Visit OpenWeatherMap**
   - Go to [https://openweathermap.org/api](https://openweathermap.org/api)

2. **Sign Up / Log In**
   - Click "Sign Up" if you don't have an account
   - Or click "Sign In" if you already have an account
   - Complete the registration (it's free!)

3. **Navigate to API Keys**
   - After logging in, go to your account dashboard
   - Click on "API keys" in the navigation menu
   - Or visit directly: [https://home.openweathermap.org/api_keys](https://home.openweathermap.org/api_keys)

4. **Create a New API Key**
   - You'll see a default key named "Default" (or create a new one)
   - If creating new: Click "Create" and give it a name (e.g., "Weather App")
   - **Copy your API key** - it looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`

⚠️ **Important**: It may take 10-60 minutes for a new API key to activate. Be patient!

---

## Step 2: Add the API Key to Your Project

You have **two options**. Choose the one you prefer:

### Option A: Using a `.env` File (Recommended - More Secure)

1. **Create a `.env` file in your project root**
   - Navigate to: `C:\Users\NAGESWARARAO VAKA\Desktop\Weather App`
   - Create a new file named `.env` (note the dot at the beginning)

2. **Add your API key to the file**
   - Open `.env` in a text editor (Notepad, VS Code, etc.)
   - Add this line (replace `your_actual_api_key_here` with your real key):
     ```
     OPENWEATHER_API_KEY=your_actual_api_key_here
     ```
   - Example:
     ```
     OPENWEATHER_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
     ```

3. **Optional: Add other settings**
   - You can also add these optional lines:
     ```
     WEATHER_UNITS=metric
     WEATHER_LANGUAGE=en
     ```

4. **Save the file**
   - Make sure the file is saved as `.env` (not `.env.txt`)

### Option B: Using Environment Variable (Temporary - Only for Current Session)

1. **Open PowerShell** (in your project directory)

2. **Set the environment variable**
   ```powershell
   $env:OPENWEATHER_API_KEY="your_actual_api_key_here"
   ```
   - Replace `your_actual_api_key_here` with your real API key

⚠️ **Note**: This only works for the current PowerShell session. If you close the terminal, you'll need to set it again.

---

## Step 3: Verify It Works

1. **Test with CLI** (Command Line)
   ```powershell
   python cli.py "London,UK" --units metric
   ```
   - If successful, you'll see weather data
   - If you see an error about API key, check:
     - Did you copy the key correctly? (no extra spaces)
     - Did you wait 10-60 minutes after creating the key?
     - Is the `.env` file in the correct location?

2. **Test with GUI** (Graphical Interface)
   ```powershell
   python main.py --mode gui
   ```
   - A window will open
   - Enter a city name (e.g., "New York") and click "Fetch Weather"
   - You should see weather information displayed

---

## Troubleshooting

### Error: "Missing OpenWeatherMap API key"
- **Solution**: Make sure your `.env` file exists in the project root directory
- Check that the file is named exactly `.env` (not `.env.txt` or `env.txt`)
- Verify the line format: `OPENWEATHER_API_KEY=your_key` (no spaces around `=`)

### Error: "Invalid API key" (401 error)
- **Solution**: 
  - Double-check you copied the entire API key correctly
  - Wait 10-60 minutes if you just created the key
  - Make sure there are no extra spaces or quotes in your `.env` file

### Error: "Unable to reach the OpenWeatherMap service"
- **Solution**: Check your internet connection

### The `.env` file doesn't show up in File Explorer
- **Solution**: File Explorer hides files starting with a dot by default
- In VS Code or other code editors, you can create it directly
- Or use PowerShell: `New-Item -Path .env -ItemType File`

---

## Quick Reference

**File Location**: `C:\Users\NAGESWARARAO VAKA\Desktop\Weather App\.env`

**File Contents**:
```
OPENWEATHER_API_KEY=your_api_key_here
WEATHER_UNITS=metric
WEATHER_LANGUAGE=en
```

**Test Command**:
```powershell
python cli.py "London,UK"
```

