# Weather API

Flask API for fetching current weather by city. The API receives a city name from the Angular frontend, finds the city coordinates with Open-Meteo Geocoding, fetches current weather from Open-Meteo Forecast, and returns a small JSON response for the UI.

## Architecture

```text
Angular Frontend
      |
      v
Flask API: api.py
      |
      v
Weather logic: weather.py
      |
      v
Open-Meteo Geocoding API + Forecast API
```

## Files

```text
Weather/
  app.py                  # Vercel Flask entrypoint
  api.py                  # Flask API server
  weather.py              # Weather lookup functions and CLI app
  requirements.txt        # Python dependencies
  weather-frontend/       # Angular frontend
  templates/              # Older HTML template
```

## Setup

Install Python dependencies:

```bash
pip install -r requirements.txt
```

If `python` does not point to your installed Python on Windows, use the full Python path or configure your IDE interpreter.

## Run The API

Start the Flask server:

```bash
python api.py
```

The API runs at:

```text
http://127.0.0.1:5050
```

## Deploying The API To Vercel

Vercel looks for Flask apps in default files such as `app.py`, `index.py`, or `server.py`.
This project keeps the real API in `api.py`, so `app.py` imports and exposes the same Flask
application for Vercel:

```python
from api import app
```

Deploy the API from the repository root. Vercel should detect `app.py` as the Flask entrypoint.

If Vercel asks for settings, use:

```text
Framework Preset: Flask
Root Directory: ./
Build Command: empty/default
Output Directory: empty/default
Install Command: pip install -r requirements.txt
```

Set this environment variable in the Vercel API project:

```text
CORS_ORIGINS=https://YOUR_FRONTEND_DEPLOYMENT.vercel.app,http://localhost:4300,http://127.0.0.1:4300
```

After deployment, test:

```text
https://YOUR_API_DEPLOYMENT.vercel.app/weather?city=London&unit=celsius
```

## Endpoints

### Health Check

```http
GET /
```

Example response:

```json
{
  "message": "Weather API is running",
  "weather_endpoint": "/weather?city=London&unit=celsius"
}
```

### Get Weather

```http
GET /weather?city=London&unit=celsius
```

Query parameters:

| Parameter | Required | Values | Description |
| --- | --- | --- | --- |
| `city` | Yes | Any city name | City to search for |
| `unit` | No | `celsius`, `fahrenheit` | Temperature unit. Defaults to `celsius` |

Example request:

```text
http://127.0.0.1:5050/weather?city=London&unit=celsius
```

Example success response:

```json
{
  "city": "London",
  "temperature": 23.2,
  "windspeed": 11.2,
  "condition": "Clear sky",
  "weathercode": 0
}
```

## How It Works

1. The frontend calls `/weather` with a city and temperature unit.
2. `api.py` validates the query parameters.
3. `get_coordinates(city)` in `weather.py` calls Open-Meteo Geocoding.
4. `get_weather(lat, lon, unit)` calls Open-Meteo Forecast using the returned coordinates.
5. The API maps the Open-Meteo weather code to readable text using `WEATHER_CODES`.
6. Flask returns JSON to the Angular frontend.

## Error Responses

Missing city:

```json
{
  "error": "Bad Request",
  "message": "City is required"
}
```

Invalid unit:

```json
{
  "error": "Bad Request",
  "message": "Unit must be celsius or fahrenheit"
}
```

Unknown city:

```json
{
  "error": "Not Found",
  "message": "Could not find city 'ExampleCity'"
}
```

Unknown endpoint:

```json
{
  "error": "Not Found",
  "message": "Endpoint not found"
}
```

## Frontend Connection

The Angular frontend is configured to call:

```text
http://127.0.0.1:5050
```

The setting is in:

```text
weather-frontend/src/environments/environment.ts
weather-frontend/src/environments/environment.development.ts
```

Run the frontend:

```bash
cd weather-frontend
npm install
npm start -- --host 127.0.0.1 --port 4300
```

Open:

```text
http://127.0.0.1:4300
```

## Notes

- The API uses Open-Meteo, which does not require an API key.
- CORS is enabled for `http://127.0.0.1:4300` and `http://localhost:4300`.
- `weather.py` can still run as a terminal app with `python weather.py`.
