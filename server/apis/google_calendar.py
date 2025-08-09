
import logging
from datetime import datetime, timedelta

from apis.google_cloud import Google_Cloud

log = logging.getLogger(__name__)


class Google_Calendar(Google_Cloud):

    def __init__(self):

        self.token_file = "token_calendar.pickle"
        self.credential_file = "credentials.json"

        self.service = self.get_google_service(api_name='calendar', api_version='v3')


    def get_upcoming_events(self, calendarId='primary', max_results=50, exclude_birthdays=True):
        """List upcoming events from the user's primary calendar."""

        now = datetime.now()
        time_min = now.replace(hour=0, minute=0, second=0, microsecond=0)
        time_min_iso = time_min.isoformat() + "Z"

        return self.get_events_in_time_range(
            start_time=time_min_iso,
            end_time=None,
            calendarId=calendarId,
            max_results=max_results,
            exclude_birthdays=exclude_birthdays)


    def get_events_today(self, calendarId='primary', max_results=50, exclude_birthdays=True):
        """List todays events from the user's primary calendar."""

        # Get today's date at midnight
        now = datetime.now()
        time_min = now.replace(hour=0, minute=0, second=0, microsecond=0)
        time_max = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Convert both times to ISO format
        time_min_iso = time_min.isoformat() + "Z"
        time_max_iso = time_max.isoformat() + "Z"

        return self.get_events_in_time_range(
            start_time=time_min_iso,
            end_time=time_max_iso,
            calendarId=calendarId,
            max_results=max_results,
            exclude_birthdays=exclude_birthdays)


    def get_events_yesterday(self, calendarId='primary', max_results=50, exclude_birthdays=True):
        """List yesterdays events from the user's primary calendar."""

        # Get yesterday's date at midnight
        yesterday = datetime.now() - timedelta(days=1)
        time_min = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        time_max = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Convert both times to ISO format
        time_min_iso = time_min.isoformat() + "Z"
        time_max_iso = time_max.isoformat() + "Z"

        return self.get_events_in_time_range(
            start_time=time_min_iso,
            end_time=time_max_iso,
            calendarId=calendarId,
            max_results=max_results,
            exclude_birthdays=exclude_birthdays)


    def get_events_n_days_ago(self, n=7, calendarId='primary', max_results=50, exclude_birthdays=True):
        """List events from n days ago from the user's primary calendar."""

        # Calculate the date n days ago
        n_days_ago = datetime.now() - timedelta(days=n)
        time_min = n_days_ago.replace(hour=0, minute=0, second=0, microsecond=0)
        time_max = n_days_ago.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Convert both times to ISO format
        time_min_iso = time_min.isoformat() + "Z"
        time_max_iso = time_max.isoformat() + "Z"

        return self.get_events_in_time_range(
            start_time=time_min_iso,
            end_time=time_max_iso,
            calendarId=calendarId,
            max_results=max_results,
            exclude_birthdays=exclude_birthdays)


    def get_events_tomorrow(self, calendarId='primary', max_results=50, exclude_birthdays=True):
        """List events for tomorrow from the user's primary calendar."""

        # Calculate tomorrow's date
        tomorrow = datetime.now() + timedelta(days=1)
        time_min = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        time_max = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Convert both times to ISO format
        time_min_iso = time_min.isoformat() + "Z"
        time_max_iso = time_max.isoformat() + "Z"

        return self.get_events_in_time_range(
            start_time=time_min_iso,
            end_time=time_max_iso,
            calendarId=calendarId,
            max_results=max_results,
            exclude_birthdays=exclude_birthdays)


    def get_events_n_days_later(self, n=7, calendarId='primary', max_results=50, exclude_birthdays=True):
        """List events from n days later from the user's primary calendar."""

        # Calculate the date n days later
        n_days_later = datetime.now() + timedelta(days=n)
        time_min = n_days_later.replace(hour=0, minute=0, second=0, microsecond=0)
        time_max = n_days_later.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Convert both times to ISO format
        time_min_iso = time_min.isoformat() + "Z"
        time_max_iso = time_max.isoformat() + "Z"

        return self.get_events_in_time_range(
            start_time=time_min_iso,
            end_time=time_max_iso,
            calendarId=calendarId,
            max_results=max_results,
            exclude_birthdays=exclude_birthdays)


    def get_events_in_time_range(self, start_time, end_time, calendarId='primary', max_results=50, exclude_birthdays=True):
        """Get events in a specific time range."""

        events_result = self.service.events().list(
            calendarId=calendarId,
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            maxResults=max_results,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        # No events found in the given time range.
        if not events:
            return True, []

        output = self._parse_events(events, exclude_birthdays)

        return True, output

    ######################

    def _parse_events(self, events, exclude_birthdays):

        output = []

        for event in events:

            event_summary = event["summary"]

            if exclude_birthdays and "birthday" in event_summary.lower():
                continue

            entry = {
                "summary"        : event_summary,
                "description"    : event.get("description", ""),
                "location"       : event.get("location", ""),
                "id"             : event["id"],
                "status"         : event["status"],
                "start_datetime" : self._to_datetime(event["start"]),
                "end_datetime"   : self._to_datetime(event["end"])
            }

            output.append(entry)

        return output


    def _to_datetime(self, event_datetime):

        if 'dateTime' in event_datetime:
            return datetime.fromisoformat(event_datetime['dateTime'])

        elif 'date' in event_datetime:
            return datetime.strptime(event_datetime['date'], '%Y-%m-%d')

        raise ValueError("Event data is missing 'dateTime' or 'date'")
