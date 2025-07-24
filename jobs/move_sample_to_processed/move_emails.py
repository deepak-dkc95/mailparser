#!/usr/bin/env python3

import sys
from pathlib import Path

# Ensure project root is in sys.path for jobs.* imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from jobs.jobs_config import SRC_SAMPLE, SRC_PROCESSED


def move_eml_files(src=SRC_SAMPLE, dst=SRC_PROCESSED):
    src.mkdir(exist_ok=True, parents=True)
    dst.mkdir(exist_ok=True, parents=True)
    for eml_file in src.glob("*.eml"):
        target = dst / eml_file.name
        eml_file.rename(target)
        # Optional: log or print move (stdout will go to systemd journal)
        print(f"Moved {eml_file} to {target}")

if __name__ == "__main__":
    move_eml_files()
