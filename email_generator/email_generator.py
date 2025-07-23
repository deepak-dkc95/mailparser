import random
import string
from email.message import EmailMessage
from email.utils import make_msgid, formatdate
from pathlib import Path
from generator_llm import VendorEmailGenerator
from generator_config import (
    VENDORS, LOREM_WORDS, KEYWORDS, MODIFIERS, SAMPLE_EML_PATH
)

class SampleEmailGenerator:
    def __init__(self, output_dir=SAMPLE_EML_PATH):
        self.vendor_llm_generator = VendorEmailGenerator()
        self.output_dir = Path(output_dir)

    @staticmethod
    def random_lorem_words(n):
        return ' '.join(random.choices(LOREM_WORDS, k=n)).capitalize()

    @staticmethod
    def random_lorem_sentence(n=15):
        return SampleEmailGenerator.random_lorem_words(n) + '.'

    @staticmethod
    def random_signature(vendor):
        return f"{SampleEmailGenerator.random_lorem_words(2).title()}\n{vendor}"

    @staticmethod
    def random_from(vendor):
        prefixes = ["somebody", "alerts", "info", "notifications", "support"]
        return f"{random.choice(prefixes)}@{vendor.lower()}.com"

    @staticmethod
    def random_email_filename():
        chars = string.ascii_lowercase + string.digits
        return 'email_' + ''.join(random.choices(chars, k=12)) + '.eml'

    def noise_email(self, vendor=None):
        if not vendor:
            vendor = random.choice(list(VENDORS.keys()))
        from_addr = self.random_from(vendor)
        to_addr = "noc@customer.com"
        noise_keywords = [k for k in KEYWORDS if k.lower() != "maintenance"]
        keyword = random.choice(noise_keywords)
        subject = f"{self.random_lorem_words(5).title()} {keyword}"
        body = self.random_lorem_sentence(35)
        signature = self.random_signature(vendor)
        return {
            "from": from_addr,
            "to": to_addr,
            "subject": subject,
            "body": body + f"\n\nBest regards,\n{signature}"
        }

    def random_email(self, vendor=None):
        if not vendor:
            vendor = random.choice(list(VENDORS.keys()))
        from_addr = self.random_from(vendor)
        to_addr = "noc@customer.com"
        subject = self.random_lorem_words(5).title()
        body = self.random_lorem_sentence(35)
        signature = self.random_signature(vendor)
        return {
            "from": from_addr,
            "to": to_addr,
            "subject": subject,
            "body": body + f"\n\nBest regards,\n{signature}"
        }

    @staticmethod
    def build_eml(email_obj):
        msg = EmailMessage()
        msg['From'] = email_obj['from']
        msg['To'] = email_obj['to']
        msg['Subject'] = email_obj['subject']
        msg['Date'] = formatdate(localtime=True)  # RFC2822
        msg['Message-ID'] = make_msgid()
        msg['MIME-Version'] = '1.0'
        msg.set_content(email_obj['body'])
        return msg

    @staticmethod
    def save_eml(email_obj, path):
        msg = SampleEmailGenerator.build_eml(email_obj)
        with open(path, 'wb') as f:
            f.write(msg.as_bytes())

    def generate_sample_emails(self):
        emails = []
        # 1. Maintenance (3)
        maint_emails = [self.vendor_llm_generator.generate_email() for _ in range(3)]
        idx = random.randint(0, 2)
        modifier = random.choice(MODIFIERS)
        maint_emails[idx]["subject"] = maint_emails[idx]["subject"].strip() + f" {modifier.capitalize()}"
        emails.extend(maint_emails)
        # 2. Keyword noise (2)
        for _ in range(2):
            emails.append(self.noise_email())
        # 3. Fully random (2)
        for _ in range(2):
            emails.append(self.random_email())
        return emails

    def write_emails_to_sample_eml_dir(self, emails):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        for email in emails:
            filename = self.random_email_filename()
            filepath = self.output_dir / filename
            self.save_eml(email, filepath)

    def generate_and_save(self, batch_size=7):
        emails = self.generate_sample_emails()
        self.write_emails_to_sample_eml_dir(emails)
        print(f"Generated & saved {len(emails)} .eml emails in {self.output_dir}")

# --- Usage/entry point ---

if __name__ == "__main__": 
    generator = SampleEmailGenerator()
    generator.generate_and_save()
