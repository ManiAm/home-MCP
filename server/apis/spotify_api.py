
import os
import sys
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

load_dotenv()


class Spotify_API():

    def __init__(self):

        SPOTIFY_Client_ID = os.getenv('SPOTIFY_Client_ID', None)
        if not SPOTIFY_Client_ID:
            log.error("SPOTIFY_Client_ID environment variable is missing!")
            sys.exit(1)

        SPOTIFY_Client_SECRET = os.getenv('SPOTIFY_Client_SECRET', None)
        if not SPOTIFY_Client_SECRET:
            log.error("SPOTIFY_Client_SECRET environment variable is missing!")
            sys.exit(1)

        SPOTIFY_Redirect_URL = os.getenv('SPOTIFY_Redirect_URL', None)
        if not SPOTIFY_Redirect_URL:
            log.error("SPOTIFY_Redirect_URL environment variable is missing!")
            sys.exit(1)

        # https://developer.spotify.com/documentation/web-api/concepts/scopes
        scope = "user-library-read"

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_Client_ID,
                                                            client_secret=SPOTIFY_Client_SECRET,
                                                            redirect_uri=SPOTIFY_Redirect_URL,
                                                            scope=scope))

    #########################

    def search_song(self, query, limit=10):
        """
        Search for songs by name
        :param query: The song name
        :param limit: The number of results to fetch
        :return: List of song details
        """

        try:

            songs = []

            results = self.sp.search(q=query, type='track', limit=limit)

            items = results.get("tracks", {}).get("items", {})

            items_filtered = [
                item for item in items if item['is_playable']
            ]

            items_sorted = sorted(items_filtered, key=lambda x: x['popularity'], reverse=True)

            for item in items_sorted:

                entry = {
                    "Type"        : item['type'],
                    "Song Name"   : item['name'],
                    "Artist Name" : item['artists'][0]['name'],
                    "Explicit"    : item['explicit'],
                    "Popularity"  : item['popularity'],
                    "uri"         : item['uri'],
                    "id"          : item['id']
                }

                songs.append(entry)

            return True, songs

        except Exception as e:

            return False, str(e)


    def search_artist(self, query, limit=10):
        """
        Search for artists by name
        :param query: The artist name
        :param limit: The number of results to fetch
        :return: List of artist details
        """

        try:

            artists = []

            results = self.sp.search(q=query, type='artist', limit=limit)

            items = results.get("artists", {}).get("items", {})

            items_sorted = sorted(items, key=lambda x: x['popularity'], reverse=True)

            for item in items_sorted:

                entry = {
                    "Type"        : item['type'],
                    "Artist Name" : item['name'],
                    "Popularity"  : item['popularity'],
                    "uri"         : item['uri'],
                    "id"          : item['id']
                }

                artists.append(entry)

            return True, artists

        except Exception as e:

            return False, str(e)


    def search_album(self, query, limit=10):
        """
        Search for albums by name
        :param query: The album name
        :param limit: The number of results to fetch
        :return: List of album details
        """

        try:

            albums = []

            results = self.sp.search(q=query, type='album', limit=limit)

            items = results.get("albums", {}).get("items", {})

            for item in items:

                entry = {
                    "Type"         : item['type'],
                    "Album Name"   : item['name'],
                    "Tracks"       : item['total_tracks'],
                    "Artists"      : item['artists'][0]['name'],
                    "Release Date" : item['release_date'],
                    "uri"          : item['uri'],
                    "id"           : item['id']
                }

                albums.append(entry)

            return True, albums

        except Exception as e:

            return False, str(e)

    #########################

    def get_saved_playlists(self, limit=50):
        """
        Get the saved playlists in your library
        :param limit: The number of results to fetch
        :return: List of saved playlists in your library
        """

        try:

            saved_playlists = []

            results = self.sp.current_user_playlists(limit=limit)

            items = results.get("items", {})

            for item in items:

                entry = {
                    "Type"    : item['type'],
                    "Name"    : item['name'],
                    "Tracks"  : item['tracks']['total'],
                    "uri"     : item['uri'],
                    "id"      : item['id']
                }

                saved_playlists.append(entry)

            return True, saved_playlists

        except Exception as e:

            return False, str(e)


    def get_saved_tracks(self, max_tracks=200):
        """
        Get the saved tracks (songs) in your library
        :param max_tracks: Maximum number of tracks to fetch
        :return: List of saved songs in your library
        """

        try:

            saved_tracks = []
            offset = 0
            limit = 50

            while True:

                results = self.sp.current_user_saved_tracks(limit=limit, offset=offset)

                items = results.get("items", {})

                for item in items:

                    track = item['track']

                    entry = {
                        "Type"        : track['type'],
                        "Song Name"   : track['name'],
                        "Artist Name" : track['artists'][0]['name'],
                        "Explicit"    : track['explicit'],
                        "Popularity"  : track['popularity'],
                        "uri"         : track['uri'],
                        "id"          : track['id']
                    }

                    saved_tracks.append(entry)

                if len(items) < limit or len(saved_tracks) >= max_tracks:
                    break

                offset += limit

            return True, saved_tracks

        except Exception as e:

            return False, str(e)


    def get_saved_track_details(self, track_id):
        """
        Get detailed information about a saved track
        :param track_id: The track ID
        :return: Detailed information about the track
        """

        try:

            track = self.sp.track(track_id)

            track_info = {
                "Type"        : track['type'],
                "Song Name"   : track['name'],
                "Artist Name" : track['artists'][0]['name'],
                "Explicit"    : track['explicit'],
                "Popularity"  : track['popularity'],
                "uri"         : track['uri'],
                "id"          : track['id']
            }

            return True, track_info

        except Exception as e:

            return False, str(e)
