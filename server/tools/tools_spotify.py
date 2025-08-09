
import logging

from apis.spotify_api import Spotify_API
from tools.decorator import include_as_tool

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


class Tool_Spotify():

    def __init__(self):

        self.sp = Spotify_API()


    @include_as_tool
    def search_song(self, query):
        """
        Searches for songs based on a given query.

        Parameters:
        - query (str): The search query for the song (e.g., song title, artist name).
        """

        status, output = self.sp.search_song(query)
        if not status:
            return False, output

        formatted_output = ""

        for entry in output:
            formatted_output += f"Song Name: {entry['Song Name']}\n"
            formatted_output += f"Artist Name: {entry['Artist Name']}\n"
            formatted_output += f"Explicit: {entry['Explicit']}\n"
            formatted_output += f"Popularity: {entry['Popularity']}\n"
            formatted_output += f"URI: {entry['uri']}\n"
            formatted_output += f"ID: {entry['id']}\n"
            formatted_output += "\n"

        return True, formatted_output


    @include_as_tool
    def search_artist(self, query):
        """
        Searches for artists based on a given query.

        Parameters:
        - query (str): The search query for the artist (e.g., artist name).
        """

        status, output = self.sp.search_artist(query)
        if not status:
            return False, output

        formatted_output = ""

        for entry in output:
            formatted_output += f"Artist Name: {entry['Artist Name']}\n"
            formatted_output += f"Popularity: {entry['Popularity']}\n"
            formatted_output += f"URI: {entry['uri']}\n"
            formatted_output += f"ID: {entry['id']}\n"
            formatted_output += "\n"

        return True, formatted_output


    @include_as_tool
    def search_album(self, query):
        """
        Searches for albums based on a given query.

        Parameters:
        - query (str): The search query for the album (e.g., album name).
        """

        status, output = self.sp.search_album(query)
        if not status:
            return False, output

        formatted_output = ""

        for entry in output:
            formatted_output += f"Album Name: {entry['Album Name']}\n"
            formatted_output += f"Tracks: {entry['Tracks']}\n"
            formatted_output += f"Artists: {entry['Artists']}\n"
            formatted_output += f"Release Date: {entry['Release Date']}\n"
            formatted_output += f"URI: {entry['uri']}\n"
            formatted_output += f"ID: {entry['id']}\n"
            formatted_output += "\n"

        return True, formatted_output


    @include_as_tool
    def get_saved_playlists(self, query):
        """
        Retrieves saved playlists based on a given query.

        Parameters:
        - query (str): The search query for playlists (e.g., playlist name).
        """

        status, output = self.sp.get_saved_playlists(query)
        if not status:
            return False, output

        formatted_output = ""

        for entry in output:
            formatted_output += f"Name: {entry['Name']}\n"
            formatted_output += f"Tracks: {entry['Tracks']}\n"
            formatted_output += f"URI: {entry['uri']}\n"
            formatted_output += f"ID: {entry['id']}\n"
            formatted_output += "\n"

        return True, formatted_output


    @include_as_tool
    def get_saved_tracks(self, query):
        """
        Retrieves saved tracks based on a given query.

        Parameters:
        - query (str): The search query for tracks (e.g., song name, artist name).
        """

        status, output = self.sp.get_saved_tracks(query)
        if not status:
            return False, output

        formatted_output = ""

        for entry in output:
            formatted_output += f"Song Name: {entry['Song Name']}\n"
            formatted_output += f"Artist Name: {entry['Artist Name']}\n"
            formatted_output += f"Type: {entry['Type']}\n"
            formatted_output += f"Explicit: {entry['Explicit']}\n"
            formatted_output += f"Popularity: {entry['Popularity']}\n"
            formatted_output += f"URI: {entry['uri']}\n"
            formatted_output += f"ID: {entry['id']}\n"
            formatted_output += "\n"

        return True, formatted_output


    @include_as_tool
    def get_saved_track_details(self, query):
        """
        Retrieves details for saved tracks based on a given query.

        Parameters:
        - query (str): The search query for tracks (e.g., song name, artist name).
        """

        status, output = self.sp.get_saved_track_details(query)
        if not status:
            return False, output

        formatted_output = ""

        for track_info in output:
            formatted_output += f"Song Name: {track_info['Song Name']}\n"
            formatted_output += f"Artist Name: {track_info['Artist Name']}\n"
            formatted_output += f"Explicit: {track_info['Explicit']}\n"
            formatted_output += f"Popularity: {track_info['Popularity']}\n"
            formatted_output += f"URI: {track_info['uri']}\n"
            formatted_output += f"ID: {track_info['id']}\n"
            formatted_output += "\n"

        return True, formatted_output


if __name__ == "__main__":

    tool = Tool_Spotify()

    status, output1 = tool.search_song(query="Shape of You Ed Sheeran")
    # status, output2 = tool.search_artist(query="Taylor Swift")
    # status, output3 = tool.search_album(query="1989")

    # status, output4 = tool.get_saved_playlists()
    # status, output5 = tool.get_saved_tracks()
    # status, output6 = tool.get_saved_track_details("spotify:track:5iyZwawawLjHYpX4MxUKVF")

    bla = 0
