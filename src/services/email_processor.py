import sys
from email import policy
from email.parser import BytesParser
from src.services.utils import logger

class EmailProcessor:
    @staticmethod
    def parse_eml():
        """
        Reads raw email bytes from stdin, parses using BytesParser, returns EmailMessage obj.
        """
        try:
            raw_email_bytes = sys.stdin.buffer.read()
            parser = BytesParser(policy=policy.default)
            email_msg = parser.parsebytes(raw_email_bytes)
            logger.info("Successfully parsed email from stdin.")
            return email_msg
        except Exception as e:
            logger.error(f"Failed to parse email from stdin: {e}")
            raise

    @staticmethod
    def get_msg_string(email_msg):
        """
        Returns: Subject:"..."\n\nBody:"..."
        """
        subject = (email_msg.get('Subject', '') or '').strip().replace('\n', ' ').replace('\r', '')
        body = ""
        if email_msg.is_multipart():
            for part in email_msg.walk():
                ctype = part.get_content_type()
                disposition = part.get_content_disposition()
                if ctype == "text/plain" and not disposition:
                    body = part.get_content().strip()
                    break
        else:
            body = email_msg.get_content().strip()
        return f'Subject:"{subject}"\n\nBody:"{body}"'
