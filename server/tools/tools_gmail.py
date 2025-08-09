
import sys
import logging
from apis.google_mail import Email_loader_Gmail
from tools.decorator import include_as_tool

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)


class Gmail_tool():

    @include_as_tool
    def get_emails_today(self):
        """
        Retrieve emails received today.

        Returns:
        For each email we print subject, sender, date and gmail id:

        Subject: Ordered: "Boka Fluoride Free..."
        Sender: "Amazon.com" <auto-confirm@amazon.com>
        Date: 2025-08-07 17:22:37 UTC
        Gmail ID: 198858e6599fe48e
        """

        gmail = Email_loader_Gmail()

        status, output = gmail.get_emails_today()
        if not status:
            return False, f"failed to fetch email: {output}"

        string = self._format_email_list(output)

        return True, string


    @include_as_tool
    def get_emails_yesterday(self):
        """
        Retrieve emails received yesterday.

        Returns:
        For each email we print subject, sender, date and gmail id:

        Subject: Ordered: "Boka Fluoride Free..."
        Sender: "Amazon.com" <auto-confirm@amazon.com>
        Date: 2025-08-07 17:22:37 UTC
        Gmail ID: 198858e6599fe48e
        """

        gmail = Email_loader_Gmail()

        status, output = gmail.get_emails_yesterday()
        if not status:
            return False, f"failed to fetch email: {output}"

        string = self._format_email_list(output)

        return True, string


    @include_as_tool
    def get_email_details(self, gmail_id):
        """
        Retrieve and print details of an email using its Gmail ID.

        Returns:
        It prints the email details including the eamil body:

        Subject: Ordered: "Boka Fluoride Free..."
        Sender: "Amazon.com" <auto-confirm@amazon.com>
        Date: 2025-08-07 17:22:37 UTC
        Gmail ID: 198858e6599fe48e
        Body: xxxxxx
        """

        gmail = Email_loader_Gmail()

        status, output = gmail.get_email_details(gmail_id)
        if not status:
            return False, f"failed to fetch email: {output}"

        string = self._format_email_list([output])

        return True, string


    def _format_email_list(self, emails):

        email_strings = []

        for email in emails:

            email_str = ""

            if 'subject' in email:
                email_str += f"Subject: {email['subject']}\n"

            if 'sender' in email:
                email_str += f"Sender: {email['sender']}\n"

            if 'date' in email:
                email_str += f"Date: {email['date'].strftime('%Y-%m-%d %H:%M:%S %Z')}\n"

            if 'gmail_id' in email:
                email_str += f"Gmail ID: {email['gmail_id']}\n"

            if 'body' in email:
                email_str += f"Body: {email['body']}\n"

            email_strings.append(email_str)

        return "\n".join(email_strings)


if __name__ == "__main__":

    gmail_tool = Gmail_tool()

    status, output = gmail_tool.get_emails_today()
    if not status:
        log.error(output)
        sys.exit(1)

    status, output = gmail_tool.get_email_details("19885b476515c896")
    if not status:
        log.error(output)
        sys.exit(1)
