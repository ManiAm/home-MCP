
import logging

from apis.google_calendar import Google_Calendar
from tools.decorator import include_as_tool

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


class Tool_Calendar():

    def __init__(self):

        self.cal = Google_Calendar()


    @include_as_tool
    def get_upcoming_events(self, calendarId='primary', max_results:int=50, exclude_birthdays:bool=True):
        """
        Retrieves a list of upcoming events from the specified Google Calendar.

        Parameters:
        - calendarId (str): The ID of the calendar to retrieve events from (default: 'primary').
        - max_results (int): The maximum number of events to return (default: 50).
        - exclude_birthdays (bool): Whether to exclude birthday events from the results (default: True).

        Sample output:
            Summary: Home Mortgage
            Description:
            Location:
            Event ID: cdi3acpl64o6abb670s30b9k65h64b9p6go6ab9n6ssjge35cgsjgc1n6s_20251201T190000Z
            Status: confirmed
            Start: 2025-12-01 11:00:00-08:00
            End: 2025-12-01 12:00:00-08:00
        """

        status, output = self.cal.get_upcoming_events(calendarId, max_results, exclude_birthdays)
        if not status:
            return False, output

        formatted_output = self._parse_event(output)

        return True, formatted_output


    @include_as_tool
    def get_events_today(self, calendarId='primary', max_results:int=50, exclude_birthdays:bool=True):
        """
        Retrieves a list of events scheduled for today from the specified Google Calendar.

        Parameters:
        - calendarId (str): The ID of the calendar to retrieve events from (default: 'primary').
        - max_results (int): The maximum number of events to return (default: 50).
        - exclude_birthdays (bool): Whether to exclude birthday events from the results (default: True).

        Sample output:
            Summary: Home Mortgage
            Description:
            Location:
            Event ID: cdi3acpl64o6abb670s30b9k65h64b9p6go6ab9n6ssjge35cgsjgc1n6s_20251201T190000Z
            Status: confirmed
            Start: 2025-12-01 11:00:00-08:00
            End: 2025-12-01 12:00:00-08:00
        """

        status, output = self.cal.get_events_today(calendarId, max_results, exclude_birthdays)
        if not status:
            return False, output

        formatted_output = self._parse_event(output)

        return True, formatted_output


    @include_as_tool
    def get_events_yesterday(self, calendarId='primary', max_results:int=50, exclude_birthdays:bool=True):
        """
        Retrieves a list of events that occurred yesterday from the specified Google Calendar.

        Parameters:
        - calendarId (str): The ID of the calendar to retrieve events from (default: 'primary').
        - max_results (int): The maximum number of events to return (default: 50).
        - exclude_birthdays (bool): Whether to exclude birthday events from the results (default: True).

        Sample output:
            Summary: Home Mortgage
            Description:
            Location:
            Event ID: cdi3acpl64o6abb670s30b9k65h64b9p6go6ab9n6ssjge35cgsjgc1n6s_20251201T190000Z
            Status: confirmed
            Start: 2025-12-01 11:00:00-08:00
            End: 2025-12-01 12:00:00-08:00
        """

        status, output = self.cal.get_events_yesterday(calendarId, max_results, exclude_birthdays)
        if not status:
            return False, output

        formatted_output = self._parse_event(output)

        return True, formatted_output


    @include_as_tool
    def get_events_n_days_ago(self, n=7, calendarId='primary', max_results:int=50, exclude_birthdays:bool=True):
        """
        Retrieves a list of events that occurred 'n' days ago from the specified Google Calendar.

        Parameters:
        - n (int): The number of days ago to retrieve events for (default: 7).
        - calendarId (str): The ID of the calendar to retrieve events from (default: 'primary').
        - max_results (int): The maximum number of events to return (default: 50).
        - exclude_birthdays (bool): Whether to exclude birthday events from the results (default: True).

        Sample output:
            Summary: Home Mortgage
            Description:
            Location:
            Event ID: cdi3acpl64o6abb670s30b9k65h64b9p6go6ab9n6ssjge35cgsjgc1n6s_20251201T190000Z
            Status: confirmed
            Start: 2025-12-01 11:00:00-08:00
            End: 2025-12-01 12:00:00-08:00
        """

        status, output = self.cal.get_events_n_days_ago(n, calendarId, max_results, exclude_birthdays)
        if not status:
            return False, output

        formatted_output = self._parse_event(output)

        return True, formatted_output


    @include_as_tool
    def get_events_tomorrow(self, calendarId='primary', max_results:int=50, exclude_birthdays:bool=True):
        """
        Retrieves a list of events scheduled for tomorrow from the specified Google Calendar.

        Parameters:
        - calendarId (str): The ID of the calendar to retrieve events from (default: 'primary').
        - max_results (int): The maximum number of events to return (default: 50).
        - exclude_birthdays (bool): Whether to exclude birthday events from the results (default: True).

        Sample output:
            Summary: Home Mortgage
            Description:
            Location:
            Event ID: cdi3acpl64o6abb670s30b9k65h64b9p6go6ab9n6ssjge35cgsjgc1n6s_20251201T190000Z
            Status: confirmed
            Start: 2025-12-01 11:00:00-08:00
            End: 2025-12-01 12:00:00-08:00
        """

        status, output = self.cal.get_events_tomorrow(calendarId, max_results, exclude_birthdays)
        if not status:
            return False, output

        formatted_output = self._parse_event(output)

        return True, formatted_output


    @include_as_tool
    def get_events_n_days_later(self, n=7, calendarId='primary', max_results:int=50, exclude_birthdays:bool=True):
        """
        Retrieves a list of events scheduled 'n' days later from the specified Google Calendar.

        Parameters:
        - n (int): The number of days later to retrieve events for (default: 7).
        - calendarId (str): The ID of the calendar to retrieve events from (default: 'primary').
        - max_results (int): The maximum number of events to return (default: 50).
        - exclude_birthdays (bool): Whether to exclude birthday events from the results (default: True).

        Sample output:
            Summary: Home Mortgage
            Description:
            Location:
            Event ID: cdi3acpl64o6abb670s30b9k65h64b9p6go6ab9n6ssjge35cgsjgc1n6s_20251201T190000Z
            Status: confirmed
            Start: 2025-12-01 11:00:00-08:00
            End: 2025-12-01 12:00:00-08:00
        """

        status, output = self.cal.get_events_n_days_later(n, calendarId, max_results, exclude_birthdays)
        if not status:
            return False, output

        formatted_output = self._parse_event(output)

        return True, formatted_output


    @include_as_tool
    def get_events_in_time_range(self, start_time, end_time, calendarId='primary', max_results:int=50, exclude_birthdays:bool=True):
        """
        Retrieves a list of events that fall within a specific time range from the specified Google Calendar.

        Parameters:
        - start_time (str): The start time of the range in ISO 8601 format.
        - end_time (str): The end time of the range in ISO 8601 format.
        - calendarId (str): The ID of the calendar to retrieve events from (default: 'primary').
        - max_results (int): The maximum number of events to return (default: 50).
        - exclude_birthdays (bool): Whether to exclude birthday events from the results (default: True).

        Sample output:
            Summary: Home Mortgage
            Description:
            Location:
            Event ID: cdi3acpl64o6abb670s30b9k65h64b9p6go6ab9n6ssjge35cgsjgc1n6s_20251201T190000Z
            Status: confirmed
            Start: 2025-12-01 11:00:00-08:00
            End: 2025-12-01 12:00:00-08:00
        """

        status, output = self.cal.get_events_in_time_range(start_time, end_time, calendarId, max_results, exclude_birthdays)
        if not status:
            return False, output

        formatted_output = self._parse_event(output)

        return True, formatted_output


    def _parse_event(self, events):

        formatted_output = ""

        for event in events:

            event_str = (
                f"Summary: {event['summary']}\n"
                f"Description: {event['description']}\n"
                f"Location: {event['location']}\n"
                f"Event ID: {event['id']}\n"
                f"Status: {event['status']}\n"
                f"Start: {event['start_datetime']}\n"
                f"End: {event['end_datetime']}\n"
                "----------------------\n"
            )

            formatted_output += event_str

        return formatted_output


if __name__ == "__main__":

    cal = Tool_Calendar()

    status, output1 = cal.get_upcoming_events()
    status, output2 = cal.get_events_today()
    status, output3 = cal.get_events_yesterday()
    status, output4 = cal.get_events_n_days_ago(n=6)

    bla = 0
