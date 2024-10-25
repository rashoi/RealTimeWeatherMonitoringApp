from flask import Flask, render_template_string, request
import requests
import pandas as pd
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

API_KEY = '972b161a90efbcb20708f6784c172d8f'  # Replace with your OpenWeatherMap API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

# Create SQLite database and table if not exists
conn = sqlite3.connect('weather_data.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS weather_data (
    timestamp DATETIME PRIMARY KEY,
    city TEXT,
    temperature REAL,
    feels_like REAL,
    humidity REAL,
    wind_speed REAL,
    description TEXT
)
''')
conn.commit()


def fetch_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            'description': data['weather'][0]['description'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
        }
    else:
        return None


def store_weather_summary():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    for city in CITIES:
        weather_data = fetch_weather(city)
        if weather_data:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
            INSERT OR REPLACE INTO weather_data (timestamp, city, temperature, feels_like, humidity, wind_speed, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (timestamp, city, weather_data['temperature'], weather_data['feels_like'], weather_data['humidity'],
                  weather_data['wind_speed'], weather_data['description']))

    conn.commit()
    conn.close()


def update_weather():
    store_weather_summary()


scheduler = BackgroundScheduler()
scheduler.add_job(func=update_weather, trigger="interval", minutes=5)
scheduler.start()


@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Weather Monitoring</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Arial', sans-serif; 
                background: linear-gradient(to right, #83a4d4, #b6fbff);
                color: #333; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                min-height: 100vh; 
            }
            .container { 
                max-width: 600px; 
                width: 90%; 
                padding: 30px; 
                background-color: #fff; 
                border-radius: 12px; 
                box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
                text-align: center;
                transition: all 0.3s ease;
            }
            .container:hover {
                box-shadow: 0px 12px 20px rgba(0, 0, 0, 0.2);
            }
            h1 { font-size: 36px; margin-bottom: 20px; }
            select, button {
                padding: 12px 20px;
                font-size: 16px;
                margin: 10px 0;
                border: none;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                cursor: pointer;
            }
            select:hover, button:hover {
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
                transform: scale(1.05);
            }
            a { 
                display: block; 
                margin-top: 20px; 
                text-decoration: none; 
                color: #007bff; 
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Select a City</h1>
            <form action="/weather" method="POST">
                <select name="city">
                    {% for city in cities %}
                        <option value="{{ city }}">{{ city }}</option>
                    {% endfor %}
                </select>
                <button type="submit">Get Weather</button>
            </form>
            <a href="/plot">View Temperature Plot</a>
        </div>
    </body>
    </html>
    ''', cities=CITIES)


@app.route('/weather', methods=['POST'])
def weather():
    city = request.form.get('city')
    weather_data = fetch_weather(city)

    if weather_data:
        store_weather_summary()
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Weather for {{ city }}</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Arial', sans-serif; 
                    background: linear-gradient(to right, #83a4d4, #b6fbff);
                    color: #333; 
                    display: flex; 
                    justify-content: center; 
                    align-items: center; 
                    min-height: 100vh; 
                }
                .container { 
                    max-width: 600px; 
                    width: 90%; 
                    padding: 30px; 
                    background-color: #fff; 
                    border-radius: 12px; 
                    box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
                    text-align: center;
                    transition: all 0.3s ease;
                }
                .container:hover {
                    box-shadow: 0px 12px 20px rgba(0, 0, 0, 0.2);
                }
                h1 { font-size: 36px; margin-bottom: 20px; }
                .temperature { font-size: 64px; color: #ff7f50; font-weight: bold; }
                .details p { font-size: 18px; margin: 8px 0; }
                a { 
                    display: block; 
                    margin-top: 20px; 
                    text-decoration: none; 
                    color: #007bff; 
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Weather in {{ city }}</h1>
                <div class="temperature">{{ weather.temperature }}°C</div>
                <div class="details">
                    <p>Humidity: {{ weather.humidity }}%</p>
                    <p>Wind Speed: {{ weather.wind_speed }} km/h</p>
                    <p>Feels Like: {{ weather.feels_like }}°C</p>
                </div>
                <a href="/">Go back</a>
                <a href="/plot">View Temperature Plot</a>
            </div>
        </body>
        </html>
        ''', weather=weather_data, city=city)
    else:
        return "Weather data not available."


@app.route('/plot')
def plot():
    conn = sqlite3.connect('weather_data.db')
    data = pd.read_sql_query("SELECT * FROM weather_data WHERE city = 'Delhi' ORDER BY timestamp DESC LIMIT 50", conn)
    conn.close()

    if not data.empty:
        data['timestamp'] = pd.to_datetime(data['timestamp'])

        plt.figure(figsize=(10, 5))
        plt.plot(data['timestamp'], data['temperature'], color='orange', marker='o', linestyle='-', linewidth=2,
                 markersize=6)
        plt.fill_between(data['timestamp'], data['temperature'], color='orange', alpha=0.2)
        plt.title('Temperature over Time (5-Minute Intervals)', fontsize=16)
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Temperature (°C)', fontsize=12)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('static/temperature_plot.png')
        plt.close()

        return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Temperature Plot</title>
            <style>
                body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; background: #f0f4f8; }
                .container { text-align: center; margin: 50px auto; padding: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Temperature Over Time (5-Minute Intervals)</h1>
                <img src="{{ url_for('static', filename='temperature_plot.png') }}" alt="Temperature Plot">
                <a href="/">Go back</a>
            </div>
        </body>
        </html>
        ''')
    else:
        return "No temperature data available."


if __name__ == '__main__':
    app.run(debug=True)
