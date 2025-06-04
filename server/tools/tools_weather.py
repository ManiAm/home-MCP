
import logging
from datetime import datetime

from apis.open_weather_client import Open_Weather_REST_API_Client
from tools.decorator import include_as_tool

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


class Weather_Info():

    def __init__(self):

        self.w_client = Open_Weather_REST_API_Client(url="https://api.openweathermap.org")


    @include_as_tool
    def get_current_weather(self, city_name=None, city_id=None, zip_code=None, unit="imperial"):
        """
        Retrieve the current weather conditions for a specific location.

        Parameters:
        - city_name (str, optional): Name of the city (e.g., "San Francisco").
        - city_id (str, optional): City ID if known (e.g., "5391959").
        - zip_code (str, optional): Zip code of the area (e.g., "94103").
        - unit (str, optional): Unit system to use. Options: "imperial" (Fahrenheit), "metric" (Celsius), or "standard" (Kelvin). Default is "imperial".

        Only one of city_name, city_id, or zip_code is required.

        Returns:
        - A human-readable summary of current weather:

            **Weather in Walnut Creek, US**
            - Conditions: Clear sky
            - Temperature: 71.85°F (Feels like 71.46°F)
            - Min/Max: 65.62°F / 76.86°F
            - Humidity: 58%
            - Pressure: 1014 hPa
            - Sea Level Pressure: 1014 hPa
            - Ground Level Pressure: 997 hPa
            - Wind: 5.99 m/s from 181° (gusts up to 8.99 m/s)
        """

        status, output = self.w_client.get_current_weather(
            city_name=city_name,
            city_id=city_id,
            zip_code=zip_code,
            unit=unit)

        if not status:
            return False, f"Failed to fetch current weather: {output}"

        return True, self._format_weather_summary(output, unit)


    def _format_weather_summary(self, data: dict, unit: str = "imperial") -> str:

        city = data.get("name", "")
        country = data.get("sys", {}).get("country", "")

        weather_desc = data.get("weather", [{}])[0].get("description", "")
        main = data.get("main", {})
        wind = data.get("wind", {})

        unit_symbol = self._get_unit_symbol(unit)

        parts = [f"**Weather in {city}, {country}**"]
        if weather_desc:
            parts.append(f"- Conditions: {weather_desc.capitalize()}")
        if "temp" in main:
            parts.append(f"- Temperature: {main['temp']}{unit_symbol} (Feels like {main.get('feels_like', '')}{unit_symbol})")
            parts.append(f"- Min/Max: {main.get('temp_min', '')}{unit_symbol} / {main.get('temp_max', '')}{unit_symbol}")
        if "humidity" in main:
            parts.append(f"- Humidity: {main['humidity']}%")
        if "pressure" in main:
            parts.append(f"- Pressure: {main['pressure']} hPa")
        if "sea_level" in main:
            parts.append(f"- Sea Level Pressure: {main['sea_level']} hPa")
        if "grnd_level" in main:
            parts.append(f"- Ground Level Pressure: {main['grnd_level']} hPa")
        if "speed" in wind:
            wind_str = f"- Wind: {wind['speed']} m/s"
            if "deg" in wind:
                wind_str += f" from {wind['deg']}°"
            if "gust" in wind:
                wind_str += f" (gusts up to {wind['gust']} m/s)"
            parts.append(wind_str)

        return "\n".join(parts)


    def _get_unit_symbol(self, unit: str) -> str:

        return "°F" if unit == "imperial" else "°C" if unit == "metric" else "K"


    @include_as_tool
    def get_forecast_5day_3hour(self, city_name, unit="imperial"):
        """
        Retrieve the 5-day weather forecast in 3-hour intervals for a specific city.

        Parameters:
        - city_name (str): The name of the city to retrieve the forecast for (e.g., "Walnut Creek").
        - unit (str, optional): Unit system to use. Options are:
            - "imperial" (default): Temperature in Fahrenheit, wind speed in mph
            - "metric": Temperature in Celsius, wind speed in m/s
            - "standard": Temperature in Kelvin

        Returns:
        - str: A human-readable multi-block summary of the forecast, with one block per 3-hour period.

        --- Forecast #1 ---
        2025-08-05 03:00:00

        - Weather: Clear sky
        - Temperature: 70.9°F (Feels like 70.4°F)
        - Low / High: 70.9°F / 72.6°F
        - Humidity: 58%
        - Wind: 8.8 m/s from 200° (gusts up to 12.8 m/s)
        - Pressure: 1014 hPa (Sea level: 1014 hPa, Ground level: 997 hPa)
        - Visibility: 10,000 meters
        """

        status, output = self.w_client.get_forecast_5day_3hour(city_name=city_name, unit=unit)
        if not status:
            return False, output

        forecast_list = output.get("list", [])
        if not forecast_list:
            return False, "No forecast data found."

        output_blocks = []

        for i, forecast in enumerate(forecast_list):
            block = self._format_weather_block_5day_3hour(forecast, unit=unit)
            output_blocks.append(f"--- Forecast #{i+1} ---\n{block}")

        return True, "\n\n".join(output_blocks)


    def _format_weather_block_5day_3hour(self, entry: dict, unit: str = "imperial"):

        dt_txt = entry.get("dt_txt", "")
        main = entry.get("main", {})
        wind = entry.get("wind", {})
        weather_list = entry.get("weather", [])
        visibility = entry.get("visibility")

        unit_symbol = self._get_unit_symbol(unit)
        desc = weather_list[0].get("description", "").capitalize() if weather_list else "Unknown"

        parts = [f"{dt_txt}", "", f"- Weather: {desc}"]

        if "temp" in main:
            parts.append(f"- Temperature: {main['temp']:.1f}{unit_symbol} (Feels like {main.get('feels_like', 0):.1f}{unit_symbol})")
            parts.append(f"- Low / High: {main.get('temp_min', 0):.1f}{unit_symbol} / {main.get('temp_max', 0):.1f}{unit_symbol}")
        if "humidity" in main:
            parts.append(f"- Humidity: {main['humidity']}%")
        if "speed" in wind:
            wind_str = f"- Wind: {wind['speed']:.1f} m/s"
            if "deg" in wind:
                wind_str += f" from {wind['deg']}°"
            if "gust" in wind:
                wind_str += f" (gusts up to {wind['gust']:.1f} m/s)"
            parts.append(wind_str)
        if "pressure" in main:
            pressure_str = f"- Pressure: {main['pressure']} hPa"
            extra = []
            if "sea_level" in main:
                extra.append(f"Sea level: {main['sea_level']} hPa")
            if "grnd_level" in main:
                extra.append(f"Ground level: {main['grnd_level']} hPa")
            if extra:
                pressure_str += " (" + ", ".join(extra) + ")"
            parts.append(pressure_str)
        if visibility is not None:
            parts.append(f"- Visibility: {visibility:,} meters")

        return "\n".join(parts)


    @include_as_tool
    def get_forecast_hourly(self, city_name=None, unit="imperial"):
        """
        Retrieve the hourly weather forecast for the next 48 hours for a given city.

        Parameters:
        - city_name (str, optional): The name of the city to retrieve the forecast for (e.g., "Walnut Creek").
        - unit (str, optional): Unit system to use. Options are:
            - "imperial" (default): Temperature in Fahrenheit, wind speed in mph
            - "metric": Temperature in Celsius, wind speed in m/s
            - "standard": Temperature in Kelvin

        Returns:
        - str: A human-readable summary of hourly forecast entries.

        --- Forecast #1 ---
        2025-08-05 02:00 UTC

        - Weather: Clear sky
        - Temperature: 68.5°F (Feels like 68.0°F)
        - Humidity: 62%
        - Dew Point: 55.0°F
        - Pressure: 1014 hPa
        - UV Index: 0.34
        - Cloud Cover: 0%
        - Precipitation Probability: 0%
        - Visibility: 10,000 meters
        - Wind: 9.3 m/s from 209° (gusts up to 12.9 m/s)
        """

        status, output = self.w_client.get_forecast_hourly(city_name=city_name, unit=unit)
        if not status:
            return False, output

        output_blocks = []

        for i, forecast in enumerate(output):
            block = self._format_weather_block_hourly(forecast, unit=unit)
            output_blocks.append(f"--- Forecast #{i+1} ---\n{block}")

        return True, "\n\n".join(output_blocks)


    def _format_weather_block_hourly(self, entry: dict, unit: str = "imperial") -> str:

        # Time formatting
        dt_unix = entry.get("dt")
        dt_str = datetime.utcfromtimestamp(dt_unix).strftime("%Y-%m-%d %H:%M UTC") if dt_unix else "Unknown time"

        # Unit symbol
        unit_symbol = self._get_unit_symbol(unit)

        # Weather description
        weather_list = entry.get("weather", [])
        description = weather_list[0].get("description", "").capitalize() if weather_list else "Unknown"

        # Core values
        temp = entry.get("temp")
        feels_like = entry.get("feels_like")
        pressure = entry.get("pressure")
        humidity = entry.get("humidity")
        dew_point = entry.get("dew_point")
        uvi = entry.get("uvi")
        clouds = entry.get("clouds")
        visibility = entry.get("visibility")
        pop = entry.get("pop")

        wind_speed = entry.get("wind_speed")
        wind_deg = entry.get("wind_deg")
        wind_gust = entry.get("wind_gust")

        parts = [f"{dt_str}", "", f"- Weather: {description}"]

        if temp is not None:
            parts.append(f"- Temperature: {temp:.1f}{unit_symbol} (Feels like {feels_like:.1f}{unit_symbol})")
        if humidity is not None:
            parts.append(f"- Humidity: {humidity}%")
        if dew_point is not None:
            parts.append(f"- Dew Point: {dew_point:.1f}{unit_symbol}")
        if pressure is not None:
            parts.append(f"- Pressure: {pressure} hPa")
        if uvi is not None:
            parts.append(f"- UV Index: {uvi}")
        if clouds is not None:
            parts.append(f"- Cloud Cover: {clouds}%")
        if pop is not None:
            parts.append(f"- Precipitation Probability: {pop*100:.0f}%")
        if visibility is not None:
            parts.append(f"- Visibility: {visibility:,} meters")
        if wind_speed is not None:
            wind = f"- Wind: {wind_speed:.1f} m/s"
            if wind_deg is not None:
                wind += f" from {wind_deg}°"
            if wind_gust is not None:
                wind += f" (gusts up to {wind_gust:.1f} m/s)"
            parts.append(wind)

        return "\n".join(parts)


    @include_as_tool
    def get_forecast_daily(self, city_name=None, unit="imperial"):
        """
        Retrieve the daily weather forecast for the next 7-8 days for a given city.

        Parameters:
        - city_name (str, optional): The name of the city to retrieve the forecast for (e.g., "Walnut Creek").
        - unit (str, optional): Unit system to use. Options are:
            - "imperial" (default): Temperature in Fahrenheit, wind speed in mph
            - "metric": Temperature in Celsius, wind speed in m/s
            - "standard": Temperature in Kelvin

        Returns:
        - str: A multi-block, human-readable summary of daily forecasts.

        --- Forecast #1 ---
        2025-08-04

        - Summary: There will be clear sky today
        - Sunrise: 13:14 UTC | Sunset: 03:14 UTC
        - Moonrise: 00:14 UTC | Moonset: 08:24 UTC
        - Temp: Day 81.19°F (Feels like 80.91°F)
        - Morning: 59.47°F / Feels like 58.64°F
        - Evening: 68.29°F / Feels like 67.73°F
        - Night: 64.26°F / Feels like 63.48°F
        - Min / Max: 56.48°F / 83.05°F
        - Humidity: 41%
        - Dew Point: 45.57°F
        - Pressure: 1015 hPa
        - Cloud Cover: 0%
        - UV Index: 9.2
        - Precipitation Probability: 0%
        - Wind: 10.3 m/s from 222° (gusts up to 13.8 m/s)
        """

        status, output = self.w_client.get_forecast_daily(city_name=city_name, unit=unit)
        if not status:
            return False, output

        output_blocks = []

        for i, forecast in enumerate(output):
            block = self._format_weather_block_daily(forecast, unit=unit)
            output_blocks.append(f"--- Forecast #{i+1} ---\n{block}")

        return True, "\n\n".join(output_blocks)


    def _format_weather_block_daily(self, entry: dict, unit: str = "imperial") -> str:

        # Time conversion
        dt_unix = entry.get("dt")
        date_str = datetime.utcfromtimestamp(dt_unix).strftime("%Y-%m-%d") if dt_unix else "Unknown date"

        sunrise = entry.get("sunrise")
        sunset = entry.get("sunset")
        moonrise = entry.get("moonrise")
        moonset = entry.get("moonset")

        # Convert timestamps to human time
        def fmt_time(ts): return datetime.utcfromtimestamp(ts).strftime("%H:%M UTC") if ts else "N/A"

        sunrise_str = fmt_time(sunrise)
        sunset_str = fmt_time(sunset)
        moonrise_str = fmt_time(moonrise)
        moonset_str = fmt_time(moonset)

        # Unit symbol
        unit_symbol = self._get_unit_symbol(unit)

        # Weather description
        weather_list = entry.get("weather", [])
        description = weather_list[0].get("description", "").capitalize() if weather_list else "Unknown"

        # Temperature
        temp = entry.get("temp", {})
        feels_like = entry.get("feels_like", {})

        parts = [f"{date_str}", ""]

        parts.append(f"- Summary: {entry.get('summary', description)}")
        parts.append(f"- Sunrise: {sunrise_str} | Sunset: {sunset_str}")
        parts.append(f"- Moonrise: {moonrise_str} | Moonset: {moonset_str}")

        parts.append(f"- Temp: Day {temp.get('day', 'N/A')}{unit_symbol} (Feels like {feels_like.get('day', 'N/A')}{unit_symbol})")
        parts.append(f"  - Morning: {temp.get('morn', 'N/A')}{unit_symbol} / Feels like {feels_like.get('morn', 'N/A')}{unit_symbol}")
        parts.append(f"  - Evening: {temp.get('eve', 'N/A')}{unit_symbol} / Feels like {feels_like.get('eve', 'N/A')}{unit_symbol}")
        parts.append(f"  - Night: {temp.get('night', 'N/A')}{unit_symbol} / Feels like {feels_like.get('night', 'N/A')}{unit_symbol}")
        parts.append(f"  - Min / Max: {temp.get('min', 'N/A')}{unit_symbol} / {temp.get('max', 'N/A')}{unit_symbol}")

        parts.append(f"- Humidity: {entry.get('humidity', 'N/A')}%")
        parts.append(f"- Dew Point: {entry.get('dew_point', 'N/A')}{unit_symbol}")
        parts.append(f"- Pressure: {entry.get('pressure', 'N/A')} hPa")
        parts.append(f"- Cloud Cover: {entry.get('clouds', 'N/A')}%")
        parts.append(f"- UV Index: {entry.get('uvi', 'N/A')}")
        parts.append(f"- Precipitation Probability: {entry.get('pop', 0) * 100:.0f}%")

        # Wind
        wind_speed = entry.get("wind_speed")
        wind_deg = entry.get("wind_deg")
        wind_gust = entry.get("wind_gust")

        if wind_speed is not None:
            wind_str = f"- Wind: {wind_speed:.1f} m/s"
            if wind_deg is not None:
                wind_str += f" from {wind_deg}°"
            if wind_gust is not None:
                wind_str += f" (gusts up to {wind_gust:.1f} m/s)"
            parts.append(wind_str)

        return "\n".join(parts)



if __name__ == "__main__":

    w_client = Weather_Info()

    # status, output = w_client.get_current_weather(city_name="Walnut Creek")
    # status, output = w_client.get_current_weather(city_id=5406990)
    # status, output = w_client.get_current_weather(zip_code=94596)

    # status, output = w_client.get_forecast_5day_3hour(city_name="Walnut Creek")

    # status, output = w_client.get_forecast_hourly("Walnut Creek")

    # status, output = w_client.get_forecast_daily("Walnut Creek")

    bla = 0
