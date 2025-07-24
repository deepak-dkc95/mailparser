from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EMAILS_DIR = PROJECT_ROOT / "emails"

SRC_SAMPLE = EMAILS_DIR / "sample_eml"
SRC_PROCESSED = EMAILS_DIR / "processed_emails"
DEST_OK = EMAILS_DIR / "procmail_sent"
DEST_FAIL = EMAILS_DIR / "failed_emails"

PROCM_EMAIL_RC = PROJECT_ROOT / ".procmailrc"
