
import os
import sys
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class Google_Cloud():

    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/calendar.readonly'
    ]

    def __init__(self):

        self.token_file = None
        self.credential_file = None


    def get_google_service(self, api_name, api_version):

        creds = None

        if os.path.exists(self.token_file):

            with open(self.token_file, 'rb') as tf:
                creds = pickle.load(tf)
                print("Expired           :", creds.expired)
                print("Has refresh token :", bool(creds.refresh_token))
                print("Valid             :", creds.valid)

                # Refresh if possible
                if creds.expired and creds.refresh_token:
                    try:
                        creds.refresh(Request())
                        print("Token refreshed successfully.")
                        # Save updated token
                        with open(self.token_file, 'wb') as tfu:
                            pickle.dump(creds, tfu)
                    except Exception as e:
                        print(f"Failed to refresh token: {e}")
                        creds = None  # fallback to re-auth

        if not creds or not creds.valid:

            if not os.path.exists(self.credential_file):
                print("Credential JSON file cannot be accessed!")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                self.credential_file,
                Google_Cloud.SCOPES
            )

            creds = flow.run_local_server(
                port=5008,
                open_browser=False,
                access_type='offline',
                include_granted_scopes='true'
            )

            with open(self.token_file, 'wb') as tf:
                pickle.dump(creds, tf)

        return build(api_name, api_version, credentials=creds)
