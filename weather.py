import requests
import sys

# Constants for API Endpoints
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Weather condition mapping according to WMO Weather interpretation codes
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm: Slight or moderate", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
}

def get_coordinates(city):
    """
    Fetch latitude and longitude for a given city.
    Returns: (lat, lon, name) or (None, None, None)
    """
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    try:
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "results" in data and data["results"]:
            location = data["results"][0]
            return location["latitude"], location["longitude"], location["name"]
        
        print(f"Error: Could not find city '{city}'.")
        return None, None, None
        
    except requests.exceptions.Timeout:
        print("Error: The request timed out.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the geocoding service.")
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred: {e}")
        
    return None, None, None

def get_weather(lat, lon, unit="celsius"):
    """
    Fetch current weather data for given coordinates.
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "temperature_unit": unit
    }
    try:
        response = requests.get(WEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def display_weather(data, city_name, unit="C"):
    """
    Displays the weather information in a formatted way.
    """
    if not data or "current_weather" not in data:
        print(f"Error: Weather data for {city_name} is unavailable.")
        return

    current = data["current_weather"]
    temp = current.get("temperature", "N/A")
    wind = current.get("windspeed", "N/A")
    code = current.get("weathercode", "Unknown")
    
    # Map weather code to description
    condition = WEATHER_CODES.get(code, "Unknown condition")

    print("-" * 30)
    print(f"Weather in {city_name}:")
    print(f"Temperature: {temp}°{unit}")
    print(f"Wind Speed: {wind} km/h")
    print(f"Condition: {condition}")
    print("-" * 30)

def main():
    print("Welcome to the Modular Weather App!")
    print("Type 'exit' to quit at any time.")

    unit_choice = input("Select temperature unit (C/F) [Default: C]: ").strip().upper()
    unit = "fahrenheit" if unit_choice == "F" else "celsius"
    unit_label = "F" if unit_choice == "F" else "C"

    while True:
        city = input("\nEnter city name: ").strip()
        
        if city.lower() == 'exit':
            print("Goodbye!")
            break
        
        if not city:
            print("Please enter a valid city name.")
            continue

        # 1. Fetch Coordinates
        lat, lon, formatted_name = get_coordinates(city)
        
        if lat and lon:
            # 2. Fetch Weather
            weather_data = get_weather(lat, lon, unit=unit)
            
            # 3. Display Result
            display_weather(weather_data, formatted_name, unit=unit_label)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        sys.exit(0)
