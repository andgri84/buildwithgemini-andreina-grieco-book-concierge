# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types


MODEL = "gemini-3.8-flash"


import json
import urllib.parse
import urllib.request


def get_weather(query: str) -> str:
    """Fetches real-time current weather information for any city or location.

    Args:
        query: A string containing the city or location name.

    Returns:
        A string with the current weather details (temperature in Celsius, conditions, humidity, wind).
    """
    try:
        # Step 1: Geocode location to lat/long
        encoded_query = urllib.parse.quote(query.strip())
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_query}&count=1&language=en&format=json"
        req = urllib.request.Request(geo_url, headers={"User-Agent": "agent-weather/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            geo_data = json.loads(resp.read().decode())

        if not geo_data.get("results"):
            return f"Could not find coordinates for location: {query}"

        location_info = geo_data["results"][0]
        name = location_info.get("name", query)
        country = location_info.get("country", "")
        lat = location_info["latitude"]
        lon = location_info["longitude"]

        # Step 2: Fetch current weather
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m"
        )
        req_weather = urllib.request.Request(weather_url, headers={"User-Agent": "agent-weather/1.0"})
        with urllib.request.urlopen(req_weather, timeout=10) as resp:
            weather_data = json.loads(resp.read().decode())

        current = weather_data.get("current", {})
        temp_c = current.get("temperature_2m")
        apparent_temp_c = current.get("apparent_temperature")
        humidity = current.get("relative_humidity_2m")
        wind_speed = current.get("wind_speed_10m")
        w_code = current.get("weather_code", 0)

        # WMO Weather interpretation codes
        weather_descriptions = {
            0: "Clear sky",
            1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Fog", 48: "Depositing rime fog",
            51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
            61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
            71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
            80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
            95: "Thunderstorm",
        }
        condition = weather_descriptions.get(w_code, "Partly cloudy")
        temp_f = round((temp_c * 9 / 5) + 32, 1) if temp_c is not None else None

        loc_str = f"{name}, {country}" if country else name
        return (
            f"Weather in {loc_str}: {condition}. "
            f"Temperature: {temp_c}°C ({temp_f}°F), "
            f"Feels like: {apparent_temp_c}°C, "
            f"Humidity: {humidity}%, "
            f"Wind speed: {wind_speed} km/h."
        )
    except Exception as e:
        return f"Error fetching weather for {query}: {str(e)}"


def get_current_time(query: str) -> str:
    """Simulates getting the current time for a city.

    Args:
        city: The name of the city to get the current time for.

    Returns:
        A string with the current time information.
    """
    if "sf" in query.lower() or "san francisco" in query.lower():
        tz_identifier = "America/Los_Angeles"
    else:
        return f"Sorry, I don't have timezone information for query: {query}."

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    return f"The current time for query {query} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="You are a helpful AI assistant designed to provide accurate and useful information.",
    tools=[get_weather, get_current_time],
)

app = App(
    root_agent=root_agent,
    name="app",
)
