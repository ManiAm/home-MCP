
# Author: Mani Amoozadeh
# Email: mani.amoozadeh2@gmail.com

import os
import sys
import getpass
import logging

from apis.rest_client import REST_API_Client

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


class Open_Weather_REST_API_Client(REST_API_Client):

    def __init__(self,
                 url=None,
                 api_ver=None,
                 base=None,
                 user=getpass.getuser()):

        super().__init__(url, api_ver, base, user)

        self.OpenWeather_API_KEY = os.getenv('OpenWeather_API_KEY', None)
        if not self.OpenWeather_API_KEY:
            log.error("OpenWeather_API_KEY environment variable is missing!")
            sys.exit(1)


    #############################
    ######### Free-Plan #########
    #############################

    def get_current_weather(self, city_name=None, city_id=None, zip_code=None, unit="imperial"):
        """
        Get current weather data by city_name or city_id or zip_code
        """

        identifiers = [city_name, city_id, zip_code]
        if sum(x is not None for x in identifiers) != 1:
            return False, "You must provide exactly one of: city_name, city_id, or zip_code."

        url = f"{self.baseurl}/data/2.5/weather"

        params = {
            "appid": self.OpenWeather_API_KEY,
            "units": unit
        }

        if city_name:
            params["q"] = city_name
        elif city_id:
            params["id"] = city_id
        elif zip_code:
            params["zip"] = zip_code

        status, output = self.request("GET", url, params=params)
        if not status:
            return False, output

        return True, output


    def get_forecast_5day_3hour(self, city_name, unit="imperial"):
        """
        Get 5-day forecast in 3-hour intervals
        """

        url = f"{self.baseurl}/data/2.5/forecast"

        params = {
            "appid": self.OpenWeather_API_KEY,
            "q": city_name,
            "units": unit
        }

        status, output = self.request("GET", url, params=params)
        if not status:
            return False, output

        return True, output


    def get_city_coordinates(self, city_name, limit=1):
        """
        Get lat/lon for a city name
        """

        url = f"{self.baseurl}/geo/1.0/direct"

        params = {
            "appid": self.OpenWeather_API_KEY,
            "q": city_name,
            "limit": limit
        }

        return self.request("GET", url, params=params)


    #############################
    ######### Paid-Plan #########
    #############################

    def get_onecall_forecast(self, city_name, unit="imperial", exclude="alerts"):
        """
        Get current, minutely, hourly, and daily forecast using One Call 3.0.
        exclude: current, minutely, hourly, daily, alerts
        """

        status, output = self.get_city_coordinates(city_name)
        if not status or not output:
            return False, f"cannot get coordinates of '{city_name}': {output}"

        if len(output) > 1:
            print(f"More than one coordinates found for '{city_name}'")

        lat = output[0].get("lat", None)
        lon = output[0].get("lon", None)
        if not lat or not lon:
            return False, f"lat or lon is missing for city {city_name}"

        url = f"{self.baseurl}/data/3.0/onecall"

        params = {
            "appid": self.OpenWeather_API_KEY,
            "lat": lat,
            "lon": lon,
            "units": unit,
            "exclude": exclude
        }

        return self.request("GET", url, params=params)


    def get_forecast_hourly(self, city_name=None, unit="imperial"):

        status, output = self.get_onecall_forecast(city_name, unit=unit, exclude="current,minutely,daily,alerts")
        if not status:
            return False, output

        result = output.get("hourly", [])
        return True, result


    def get_forecast_daily(self, city_name=None, unit="imperial"):

        status, output = self.get_onecall_forecast(city_name, unit=unit, exclude="current,minutely,hourly,alerts")
        if not status:
            return False, output

        result = output.get("daily", [])
        return True, result
