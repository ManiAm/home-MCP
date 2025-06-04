
# Author: Mani Amoozadeh
# Email: mani.amoozadeh2@gmail.com

import os
import sys
import getpass
import logging

from apis.rest_client import REST_API_Client

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


class TZ_DB_REST_API_Client(REST_API_Client):

    def __init__(self,
                 url=None,
                 api_ver=None,
                 base=None,
                 user=getpass.getuser()):

        super().__init__(url, api_ver, base, user)

        self.TimeZoneDB_API_KEY = os.getenv('TimeZoneDB_API_KEY', None)
        if not self.TimeZoneDB_API_KEY:
            log.error("TimeZoneDB_API_KEY environment variable is missing!")
            sys.exit(1)


    def list_timezone(self, country_code=None, zone_name=None):

        url = f"{self.baseurl}/list-time-zone"

        params = {
            "key": self.TimeZoneDB_API_KEY,
            "format": "json",
            "country": country_code,
            "zone": zone_name
        }

        status, output = self.request("GET", url, params=params)
        if not status:
            return False, output

        if not isinstance(output, dict):
            return False, f"Unexpected output type: {type(output)}"

        status = output.get("status", "")
        message = output.get("message", "")

        if status and status == "FAILED":
            return False, message

        zones = output.get("zones", [])

        return True, zones


    def get_timezone(self,
                     lookup_by="city",
                     city_name=None,
                     country_code=None,
                     region_code=None,
                     zone_name=None,
                     lat=None,
                     lng=None):

        if lookup_by == "city":
            if not city_name or not country_code:
                return False, "city_name and country_code are both required in lookup by city."
        elif lookup_by == "zone":
            if not zone_name:
                return False, "zone_name is required in lookup by zone."
        elif lookup_by == "position":
            if not lat or not lng:
                return False, "lat and lng are both required in lookup by position."
        else:
            return False, f"invalid lookup_by method: {lookup_by}"

        url = f"{self.baseurl}/get-time-zone"

        params = {
            "key": self.TimeZoneDB_API_KEY,
            "format": "json",
            "by": lookup_by,
            "zone": zone_name,
            "lat": lat,
            "lng": lng,
            "country": country_code,
            "region": region_code,
            "city": city_name
        }

        status, output = self.request("GET", url, params=params)
        if not status:
            return False, output

        if not isinstance(output, dict):
            return False, f"Unexpected output type: {type(output)}"

        status = output.get("status", "")
        message = output.get("message", "")

        if status and status == "FAILED":
            return False, message

        zones = output.get("zones", [])

        return True, zones
