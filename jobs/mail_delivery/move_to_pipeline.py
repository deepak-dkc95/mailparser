#!/usr/bin/env python3

import sys
from pathlib import Path

# Ensure project root is in sys.path for jobs.* imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import subprocess
import time
import shutil
from jobs.jobs_config import SRC_PROCESSED, DEST_OK, DEST_FAIL, PROCMAILRC

def process_eml(eml_path):
    with eml_path.open("rb") as f:
        try:
            result = subprocess.run(
                ["procmail", str(PROCMAILRC)],
                stdin=f,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=90
            )
            if result.returncode == 0:
                print(f"PROCM SUCCESS: {eml_path.name}")
                return True
            else:
                print(f"PROCM FAIL: {eml_path.name}, code {result.returncode}")
        except Exception as ex:
            print(f"PROCM EXCEPTION: {eml_path.name}: {ex}")
    return False

def main():
    for eml in sorted(SRC_PROCESSED.glob("*.eml")):
        # First attempt
        success = process_eml(eml)
        if not success:
            time.sleep(5)  # short pause before retry
            # Retry once
            success2 = process_eml(eml)
            if not success2:
                # Move to failed_emails
                shutil.move(str(eml), DEST_FAIL / eml.name)
                print(f"MOVED TO FAILED: {eml.name}")
                time.sleep(3)  # tiny pause
                continue
        # If success, move to procmail_sent
        shutil.move(str(eml), DEST_OK / eml.name)
        print(f"MOVED TO SENT: {eml.name}")
        time.sleep(180)  # 3 minutes before next email!

if __name__ == "__main__":
    DEST_OK.mkdir(exist_ok=True)
    DEST_FAIL.mkdir(exist_ok=True)
    main()
