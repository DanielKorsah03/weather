import os

from flask import Flask, jsonify, request

try:
    from flask_cors import CORS
except ImportError:  # Flask-CORS is optional when frontend/backend share an origin.
    CORS = None

from weather import WEATHER_CODES, get_coordinates, get_weather


app = Flask(__name__)

if CORS:
    allowed_origins = os.environ.get(
        "CORS_ORIGINS",
        "http://127.0.0.1:4300,http://localhost:4300",
    ).split(",")
    CORS(app, origins=[origin.strip() for origin in allowed_origins if origin.strip()])


@app.get("/")
def health_check():
    return jsonify(
        {
            "message": "Weather API is running",
            "weather_endpoint": "/weather?city=London&unit=celsius",
        }
    )


@app.get("/weather")
def weather_by_city():
    city = request.args.get("city", "").strip()
    unit = request.args.get("unit", "celsius").strip().lower()

    if not city:
        return jsonify({"error": "Bad Request", "message": "City is required"}), 400

    if unit not in {"celsius", "fahrenheit"}:
        return jsonify({"error": "Bad Request", "message": "Unit must be celsius or fahrenheit"}), 400

    lat, lon, formatted_name = get_coordinates(city)

    if lat is None or lon is None:
        return jsonify({"error": "Not Found", "message": f"Could not find city '{city}'"}), 404

    weather_data = get_weather(lat, lon, unit=unit)

    if not weather_data or "current_weather" not in weather_data:
        return jsonify({"error": "Bad Gateway", "message": "Weather data is unavailable"}), 502

    current = weather_data["current_weather"]
    code = current.get("weathercode")

    return jsonify(
        {
            "city": formatted_name,
            "temperature": current.get("temperature"),
            "windspeed": current.get("windspeed"),
            "condition": WEATHER_CODES.get(code, "Unknown condition"),
            "weathercode": code,
        }
    )


@app.errorhandler(404)
def not_found(_error):
    return jsonify({"error": "Not Found", "message": "Endpoint not found"}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5050"))
    debug = os.environ.get("FLASK_DEBUG", "").lower() in {"1", "true", "yes"}
    app.run(host="127.0.0.1", port=port, debug=debug)
