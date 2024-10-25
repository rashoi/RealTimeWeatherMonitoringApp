# 🌦️ Real-Time Weather Monitoring System 🌦️

A comprehensive real-time weather monitoring application that collects, analyzes, and visualizes weather data for major metro cities in India. Using data from OpenWeatherMap, the system generates daily summaries, monitors trends, and triggers alerts based on customizable thresholds.


### 📑 Project Highlights
- **Real-time Data Retrieval**: Continuously fetches data from OpenWeatherMap for cities like Delhi, Mumbai, Chennai, Bangalore, Kolkata, and Hyderabad.
- **Daily Summary Rollups**: Generates average, maximum, and minimum temperatures, and determines the dominant weather condition each day.
- **Configurable Alerts**: Define thresholds for temperature or specific weather conditions to receive notifications when these limits are exceeded.
- **Data Visualization**: Visualizes weather summaries and alerts, making it easy to track trends and respond to changes.


### ⚙️ Technologies Used
- **Python**: Selected for its simplicity and powerful libraries for data processing.
- **SQLite3**: Serves as a local database for efficient storage of daily summaries and alerts.
- **Requests**: Handles API interactions with OpenWeatherMap.
- **Matplotlib**: Used for intuitive and customizable data visualization.


### 🚀 Quickstart Guide

#### 1. Clone & Navigate
```bash
git clone https://github.com/rashoi/RealTimeWeatherMonitoringApp
cd Real-Time-Weather-Monitoring
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. OpenWeatherMap API Key
   - [Sign up here](https://openweathermap.org/) to obtain a free API key.
   - Create a `.env` file in your project’s root directory and add the following:
     ```plaintext
     API_KEY=your_openweather_api_key
     ```

#### 4. Run the Application
```bash
python main.py
```


### ⚙️ Configuration Options
Edit `config.json` to customize intervals and thresholds:
```json
{
  "interval_seconds": 300,
  "temperature_threshold": 35
}
```

**Configurable Parameters:**
- `interval_seconds`: Frequency (in seconds) of API calls.
- `temperature_threshold`: Set a temperature threshold to trigger alerts (e.g., 35°C).


### 🛠️ Features & Functionality

#### 🌤️ Weather Data Rollups
- **Daily Summary**: Aggregates weather data by day, including:
  - **Average Temperature**
  - **Maximum & Minimum Temperatures**
  - **Dominant Weather Condition**: Based on frequency to determine the most common weather pattern.

#### 🚨 Alert System
- **Customizable Alerts**: Define thresholds to receive alerts for specific weather conditions (e.g., temperature exceeding 35°C).
- **Flexible Alerting Options**: Alerts display in the console, and future updates could include email notifications.

#### 📊 Data Visualization
- **Historical Weather Trends**: View trends and patterns across days.
- **Alerts Overview**: Track when and where specific conditions triggered alerts.


### 🧪 Testing Guide

| Test Scenario                    | Expected Outcome |
|----------------------------------|------------------|
| **System Initialization**        | Verify API key connection and successful system start. |
| **Data Retrieval Simulation**    | Ensure correct data parsing and handling. |
| **Temperature Conversion**       | Test Kelvin to Celsius/Fahrenheit conversion. |
| **Daily Summary Rollup**         | Confirm correct daily averages, max/min, and dominant conditions. |
| **Alert Triggering**             | Verify alerts trigger correctly on threshold breaches. |


### 📈 Future Enhancements
- **Extended Weather Parameters**: Add support for humidity, wind speed, and other parameters.
- **Multi-City Support**: Enable user-specified cities.
- **Email Notifications**: Implement notifications through email or SMS.

### 🎨 Why These Technologies?
- **Python**: Excellent for real-time data processing with powerful API interaction libraries.
- **SQLite3**: A reliable, lightweight database suitable for quick data persistence.
- **Matplotlib & Seaborn**: Robust tools for creating engaging and clear visualizations.
