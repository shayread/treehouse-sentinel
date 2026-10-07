import requests

'''
Provider for retrieving weather information based on geolocation data.
API Documentation: https://open-meteo.com/en/docs
'''

class WeatherProvider:

    ENDPOINT = "https://api.open-meteo.com/v1/forecast"
    WEATHER_CODE_MAPPING = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        97: "Heavy thunderstorm",
        99: "Thunderstorm with heavy hail"
    }

    def get_weather_info(self, latitude, longitude):
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "weather_code"],
            "temperature_unit": "fahrenheit"
        }
        response = requests.get(url=self.ENDPOINT, params=params)

        if response.ok:
            response_json = response.json()
            current_weather = response_json['current']
            return {
                "temperature": current_weather['temperature_2m'],
                "weather": self.WEATHER_CODE_MAPPING[current_weather['weather_code']]
            }
        else:
            print(f"WARNING: Weather request failed with status code {response.status_code} and "
                  f"reason {response.reason}. Storing species identification without weather information...")
            return {
                "temperature": -50.0,
                "weather": "UNKNOWN"
            }