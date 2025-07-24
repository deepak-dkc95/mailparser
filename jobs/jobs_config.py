from pathlib import Path

# Set the paths (use absolute paths for reliability in systemd jobs)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC = PROJECT_ROOT / "emails" / "sample_eml"
DST = PROJECT_ROOT / "emails" / "processed_emails"