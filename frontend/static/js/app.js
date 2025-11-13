const form = document.getElementById("search-form");
const locationInput = document.getElementById("location");
const unitsSelect = document.getElementById("units");
const languageInput = document.getElementById("language");
const messageEl = document.getElementById("form-message");
const clearHistoryBtn = document.getElementById("clear-history");
const historyList = document.getElementById("history-list");
const resultCard = document.getElementById("result-card");

const resultLocation = document.getElementById("result-location");
const resultTimestamp = document.getElementById("result-timestamp");
const resultIcon = document.getElementById("result-icon");
const resultConditions = document.getElementById("result-conditions");
const resultTemperature = document.getElementById("result-temperature");
const resultFeelsLike = document.getElementById("result-feels-like");
const resultHumidity = document.getElementById("result-humidity");
const resultPressure = document.getElementById("result-pressure");
const resultWind = document.getElementById("result-wind");

const HISTORY_KEY = "weather-app-history-v1";
const MAX_HISTORY = 8;

function setFormLoading(isLoading) {
    const submitBtn = form.querySelector("button[type='submit']");
    if (!submitBtn) return;
    submitBtn.classList.toggle("btn--loading", isLoading);
    submitBtn.disabled = isLoading;
}

function showMessage(text, type = "info") {
    messageEl.textContent = text;
    messageEl.dataset.type = type;
}

function clearMessage() {
    messageEl.textContent = "";
    messageEl.removeAttribute("data-type");
}

function loadHistory() {
    try {
        const data = localStorage.getItem(HISTORY_KEY);
        return data ? JSON.parse(data) : [];
    } catch {
        return [];
    }
}

function saveHistory(history) {
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(0, MAX_HISTORY)));
}

function addToHistory(entry) {
    const history = loadHistory();
    const filtered = history.filter((item) => item.location.toLowerCase() !== entry.location.toLowerCase());
    filtered.unshift(entry);
    saveHistory(filtered);
    renderHistory();
}

function renderHistory() {
    const history = loadHistory();
    historyList.innerHTML = "";

    if (!history.length) {
        const placeholder = document.createElement("li");
        placeholder.className = "history__placeholder";
        placeholder.textContent = "Your latest locations appear here.";
        historyList.appendChild(placeholder);
        return;
    }

    history.forEach((item) => {
        const li = document.createElement("li");
        li.className = "history__item";
        li.innerHTML = `
            <span>
                <span class="history__item-location">${item.location}</span>
                <span class="history__item-meta">${item.timestamp}</span>
            </span>
            <span class="history__item-meta">${item.temp}</span>
        `;
        li.addEventListener("click", () => {
            locationInput.value = item.location;
            unitsSelect.value = item.units;
            languageInput.value = item.language;
            form.dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
        });
        historyList.appendChild(li);
    });
}

function describeWind(units, speed) {
    if (units === "imperial") {
        return `${speed.toFixed(1)} mph`;
    }
    return `${speed.toFixed(1)} m/s`;
}

function describeTemperature(units, temp) {
    const suffix = units === "imperial" ? "°F" : units === "metric" ? "°C" : "K";
    return `${temp.toFixed(1)}${suffix}`;
}

async function fetchWeather({ location, units, language }) {
    const params = new URLSearchParams({ location });
    if (units) params.set("units", units);
    if (language) params.set("language", language);

    const response = await fetch(`/api/weather?${params.toString()}`);
    const payload = await response.json();

    if (!response.ok) {
        const error = payload?.error || "Unexpected error while contacting server.";
        throw new Error(error);
    }

    return payload.data;
}

function updateResultCard(data, units) {
    resultLocation.textContent = data.display_name;
    resultTimestamp.textContent = `Updated ${data.timestamp_local}`;
    resultConditions.textContent = data.description;

    resultTemperature.textContent = describeTemperature(units, data.temperature);
    resultFeelsLike.textContent = `Feels like ${describeTemperature(units, data.feels_like)}`;
    resultHumidity.textContent = `${data.humidity}%`;
    resultPressure.textContent = `${data.pressure} hPa`;
    resultWind.textContent = describeWind(units, data.wind_speed);

    if (data.icon) {
        resultIcon.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
        resultIcon.hidden = false;
    } else {
        resultIcon.hidden = true;
        resultIcon.removeAttribute("src");
    }

    resultCard.hidden = false;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const location = locationInput.value.trim();
    const units = unitsSelect.value;
    const language = languageInput.value.trim();

    if (!location) {
        showMessage("Please enter a location to continue.", "error");
        return;
    }

    clearMessage();
    setFormLoading(true);

    try {
        const data = await fetchWeather({ location, units, language });
        updateResultCard(data, units);
        clearMessage();
        addToHistory({
            location: data.display_name,
            units,
            language,
            timestamp: new Date(data.timestamp_iso).toLocaleString(),
            temp: describeTemperature(units, data.temperature),
        });
    } catch (error) {
        showMessage(error.message, "error");
    } finally {
        setFormLoading(false);
    }
});

clearHistoryBtn.addEventListener("click", () => {
    localStorage.removeItem(HISTORY_KEY);
    renderHistory();
});

document.addEventListener("DOMContentLoaded", () => {
    if (window.appConfig) {
        unitsSelect.value = window.appConfig.defaultUnits || "metric";
        languageInput.value = window.appConfig.defaultLanguage || "en";
    }

    renderHistory();
    locationInput.focus();
});

