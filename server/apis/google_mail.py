
import re
import logging
import uuid
import html2text
from datetime import datetime, timezone, timedelta
from base64 import urlsafe_b64decode

from email.utils import parsedate_to_datetime
from email.utils import getaddresses

from apis.google_cloud import Google_Cloud

log = logging.getLogger(__name__)


class Email_loader_Gmail(Google_Cloud):

    def __init__(self):

        self.token_file = "token_gmail.pickle"
        self.credential_file = "credentials.json"

        self.service = self.get_google_service(api_name='gmail', api_version='v1')


    def get_emails_today(self):
        """Get emails received today."""

        today = datetime.now().date()
        query = f"after:{today} before:{today + timedelta(days=1)}"
        return self._get_emails(query)


    def get_emails_yesterday(self):
        """Get emails received yesterday."""

        yesterday = datetime.now().date() - timedelta(days=1)
        query = f"after:{yesterday} before:{yesterday + timedelta(days=1)}"
        return self._get_emails(query)


    def get_emails_n_days_ago(self, n):
        """Get emails received n days ago."""

        target_date = datetime.now().date() - timedelta(days=n)
        query = f"after:{target_date} before:{target_date + timedelta(days=1)}"
        return self._get_emails(query)


    def get_emails_between_dates(self, start_date, end_date):
        """Get emails between two dates."""

        start_date = parsedate_to_datetime(start_date).strftime("%Y/%m/%d")
        end_date = parsedate_to_datetime(end_date).strftime("%Y/%m/%d")
        query = f"after:{start_date} before:{end_date}"
        return self._get_emails(query)


    def get_all_emails(self):
        """Get all emails (no date restriction)."""

        query = ""
        return self._get_emails(query)


    def get_email_details(self, gmail_id):

        full = self.service.users().messages().get(userId='me', id=gmail_id, format='full').execute()

        status, output = self._extract_emails_meta(emails=[full])
        if not status:
            return False, output

        email_meta = output[0]

        payload = full.get('payload', {})
        email_meta["body"] = self._extract_body(payload)

        return True, email_meta

    ##############################################################

    def _get_emails(self, query, maxResults=40):
        """Retrieve emails matching a specific query."""

        status, output = self._get_emails_meta(query, maxResults)
        if not status:
            return False, output

        return self._extract_emails_meta(output)


    def _get_emails_meta(self, query, maxResults):

        try:

            email_data = []

            results = self.service.users().messages().list(
                userId='me',
                q=query,
                labelIds=['INBOX'],
                maxResults=maxResults).execute()

            messages = results.get('messages', [])

            if not messages:
                return True, email_data

            for msg in messages:
                # no body or attachments
                msg_data = self.service.users().messages().get(userId='me', id=msg['id'], format='metadata').execute()
                email_data.append(msg_data)

            return True, email_data

        except Exception as error:
            return False, f"_get_emails_meta: An error occurred: {error}"


    def _extract_emails_meta(self, emails):

        msg_dict = []

        for metadata in emails:

            gmail_id = metadata['id']

            headers = metadata.get('payload', {}).get('headers', [])

            message_header = {
                h['name'].lower(): h['value'] for h in headers
            }

            references_raw = message_header.get('references', '')
            references_list = references_raw.split() if references_raw else []

            recipients_raw = message_header.get('to', '')
            recipients = [email for _, email in getaddresses([recipients_raw])]

            # Date in UTC
            date_str = message_header.get('date')
            date_obj = None
            if date_str:
                try:
                    date_obj = parsedate_to_datetime(date_str).astimezone(timezone.utc)
                except Exception:
                    print(f"Error: parsing email date: {date_str}")

            msg_data = {
                "gmail_id"     : gmail_id,   # Unique to Gmail for API interactions
                "message_id"   : message_header.get('message-id', str(uuid.uuid4())),   # Unique to the email itself, used for threading,
                                                                                        # replies, and cross-system tracking of messages.
                "thread_id"    : message_header.get('threadId'),
                "references"   : references_list,
                "in_reply_to"  : message_header.get('in-reply-to'),
                "sender"       : message_header.get('from', ''),
                "recipients"   : recipients,
                "date"         : date_obj,
                "subject"      : message_header.get('subject', ''),
                "internalDate" : int(message_header.get('internalDate', 0))
            }

            msg_dict.append(msg_data)

        return True, msg_dict


    def _extract_body(self, payload):

        def decode(data):
            if not data:
                return ""
            try:
                data += '=' * (-len(data) % 4)
                return urlsafe_b64decode(data).decode(errors="ignore")
            except Exception:
                return ""

        text_plain = ""
        text_html = ""

        def recurse_parts(parts):

            nonlocal text_plain, text_html

            for part in parts:

                mime = part.get('mimeType')
                body_data = part.get('body', {}).get('data')

                if body_data:
                    decoded = decode(body_data)
                    if mime == 'text/plain':
                        text_plain += "\n" + decoded
                    elif mime == 'text/html':
                        text_html += "\n" + decoded

                if 'parts' in part:
                    recurse_parts(part['parts'])

        if 'parts' in payload:
            recurse_parts(payload['parts'])
        else:
            # Single-part message
            mime = payload.get('mimeType')
            body_data = payload.get('body', {}).get('data')
            decoded = decode(body_data)
            if mime == 'text/plain':
                text_plain = decoded
            elif mime == 'text/html':
                text_html = decoded

        if text_html:
            status, output = self._html_to_text(text_html)
            if status and output:
                text_plain = output

        return text_plain.replace('\x00', '').strip()


    def _html_to_text(self, html_text):

        try:

            h = html2text.HTML2Text()

            h.ignore_links = True           # Do not include hyperlinks
            h.ignore_images = True          # Skip image tags
            h.body_width = 0                # Do not wrap text
            h.ignore_emphasis = True        # Remove **bold** and _italics_
            h.skip_internal_links = True    # Avoid internal anchors
            h.ignore_tables = True          # Do not include tables
            h.protect_links = True

            text = h.handle(html_text)

            # Remove invisible or formatting Unicode characters
            text = re.sub(r"[\u200c\u200d\u200e\u200f\u202a-\u202e\u2060-\u206f\u00ad\xa0]", " ", text)

            # Replace multiple consecutive spaces or tabs with a single space
            text = re.sub(r"[ \t]+", " ", text)

            # Normalize newlines (remove lines that are empty or have only whitespace)
            text = re.sub(r"\n\s*\n+", "\n\n", text)

            return True, text.strip()

        except Exception as E:

            return False, f"Error in parsing html: {str(E)}"


if __name__ == "__main__":

    gmail = Email_loader_Gmail()
    gmail.get_emails_today()
