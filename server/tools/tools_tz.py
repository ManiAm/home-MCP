
import logging
from apis.tz_db_client import TZ_DB_REST_API_Client
from tools.decorator import include_as_tool

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


class TZ_Info():

    def __init__(self):

        self.tz_client = TZ_DB_REST_API_Client(url="http://vip.timezonedb.com", api_ver="v2.1")


    @include_as_tool
    def list_timezone(self, country_code=None, zone_name=None, max_entries: int=10):
        """
        List available time zones.

        Parameters:
        - country_code (optional): A valid ISO 3166-1 alpha-2 country code (e.g., "US", "IN", "AU").
        - zone_name (optional): Specific time zone name (e.g., "America/Los_Angeles", "Asia/Kolkata").

        Returns:
        A list of time zone records. Each record contains:

        - countryCode (str): ISO 3166-1 alpha-2 country code representing the country. Example: 'US'
        - countryName (str): Full name of the country associated with the time zone. Example: 'United States'
        - zoneName (str): IANA time zone identifier. Example: 'America/Adak'
        - gmtOffset (int): The number of seconds the time zone is offset from GMT/UTC. Example: -32400  (which is UTC-9:00)
        - timestamp (int): The current local Unix timestamp (seconds since epoch) in that time zone. Example: 1749913379
        """

        status, output = self.tz_client.list_timezone(country_code=country_code, zone_name=zone_name)
        if not status:
            return False, f"Failed to fetch timezones: {output}"

        if not output:
            return False, "No time zones found for the given parameters."

        if not isinstance(output, list):
            return False, "Unexpected output format"

        lines = []
        for r in output[:max_entries]:
            line = (
                f"countryCode = '{r.get('countryCode', 'N/A')}', "
                f"countryName = '{r.get('countryName', 'N/A')}', "
                f"zoneName = '{r.get('zoneName', 'N/A')}', "
                f"gmtOffset = {r.get('gmtOffset', 'N/A')}, "
                f"timestamp = {r.get('timestamp', 'N/A')}"
            )
            lines.append(line)

        output = "\n\n".join(lines)

        return True, output


    @include_as_tool
    def get_timezone(self,
                     lookup_by="city",
                     city_name=None,
                     country_code=None,
                     region_code=None,
                     zone_name=None,
                     lat=None,
                     lng=None,
                     max_entries: int=10):
        """
        Retrieve the current local time, GMT offset, zone name, DST, etc. for a given location.

        Parameters:
        - lookup_by: Required. One of "city", "zone", or "position".
            - "city": Lookup by city name and country code.
            - "zone": Lookup by full time zone name (e.g., "Asia/Tokyo").
            - "position": Lookup by geographic coordinates (latitude and longitude).

        Required Fields (based on lookup_by):
        - If lookup_by == "city":
            - city_name: The city (e.g., "Paris")
            - country_code: ISO 3166 country code (e.g., "FR")
        - If lookup_by == "zone":
            - zone_name: Full zone name (e.g., "Europe/Paris")
        - If lookup_by == "position":
            - lat: Latitude (e.g., 48.8566)
            - lng: Longitude (e.g., 2.3522)

        Returns:
        A list of time zone records. Each record contains:

        - countryCode: ISO 3166-1 alpha-2 country code. Example: "US"
        - countryName: Full name of the country. Example: "United States"
        - regionName: Administrative region or state name. Example: "California"
        - cityName: Name of the city or locality. Example: "Walnut Creek"
        - zoneName: IANA time zone identifier. Example: "America/Los_Angeles"
        - abbreviation: Time zone abbreviation. Example: "PDT"
        - gmtOffset: Offset from GMT/UTC in seconds. Example: -25200
        - dst: Indicates if Daylight Saving Time is active ("1") or not ("0"). Example: "1"
        - zoneStart: Unix timestamp when current DST period began. Example: 1741514400
        - zoneEnd: Unix timestamp when next DST change will occur. Example: 1762074000
        - timestamp: Current local time as Unix timestamp. Example: 1749914980
        - formatted: Human-readable local time. Example: "2025-06-14 15:29:40"
        - nextAbbreviation: Time zone abbreviation after the next DST change. Example: "PST"
        """

        status, output = self.tz_client.get_timezone(lookup_by=lookup_by,
                                                     city_name=city_name,
                                                     country_code=country_code,
                                                     region_code=region_code,
                                                     zone_name=zone_name,
                                                     lat=lat,
                                                     lng=lng)

        if not status:
            return False, output

        if not output:
            return False, "No time zones found for the given parameters."

        if not isinstance(output, list):
            return False, "Unexpected output format"

        lines = []
        for r in output[:max_entries]:
            line = (
                f"countryCode = '{r.get('countryCode', 'N/A')}', "
                f"countryName = '{r.get('countryName', 'N/A')}', "
                f"regionName = '{r.get('regionName', 'N/A')}', "
                f"cityName = '{r.get('cityName', 'N/A')}', "
                f"zoneName = '{r.get('zoneName', 'N/A')}', "
                f"abbreviation = '{r.get('abbreviation', 'N/A')}', "
                f"gmtOffset = {r.get('gmtOffset', 'N/A')}, "
                f"dst = '{r.get('dst', 'N/A')}', "
                f"zoneStart = {r.get('zoneStart', 'N/A')}, "
                f"zoneEnd = {r.get('zoneEnd', 'N/A')}, "
                f"timestamp = {r.get('timestamp', 'N/A')}, "
                f"formatted = '{r.get('formatted', 'N/A')}', "
                f"nextAbbreviation = '{r.get('nextAbbreviation', 'N/A')}'"
            )
            lines.append(line)

        output = "\n\n".join(lines)

        return True, output


if __name__ == "__main__":

    tz_client = TZ_Info()

    status, output = tz_client.list_timezone(country_code="US")
    status, output = tz_client.get_timezone(city_name="Walnut creek", country_code="US")

    bla = 0
