# MailParser: Network Maintenance Email Extraction & Automation

## Overview

**MailParser** is a Python-based system for parsing and extracting structured data from network maintenance emails using LLMs, storing results in PostgreSQL, and automating email file processing with systemd.  

This project enables:
- Automated detection and movement of incoming sample `.eml` emails using systemd jobs and timers.
- Extraction of key vendor/maintenance data using an LLM (Cohere) with robust logging.
- Organized storage, config separation, and easy further integration with database backends.

## Directory Structure

```
mailparser/
├── database_schema.sql              # SQL schema for PostgreSQL JSON tables
├── emails/                         # Incoming and processed .eml files
│   ├── sample_eml/                 # Drop new .eml samples here
│   └── processed_emails/           # .eml files moved here by systemd job
├── jobs/                           # All job scripts, configs, systemd units
│   ├── jobs_config.py
│   └── move_sample_to_processed/
│       ├── move_emails.py
│       ├── move_emails.service
│       └── move_emails.timer
├── logs/                           # Log output (e.g. parser.log)
├── prompts/                        # Prompt engineering for LLM email extraction
│   └── llm_prompt.txt
├── src/                            # Core app/services code
│   ├── config.py
│   └── services/
│       ├── llm_service.py
│       └── ...
└── tests/
    └── test_email.txt
```

## Quickstart

### 1. Python Environment

- Python 3.8+ recommended.
- `pip install -r requirements.txt`  
    *(requirements.txt should list: cohere, python-dotenv, psycopg2-binary, etc.)*

### 2. Configuration

- Set your `.env` with the required API keys, e.g.:
    ```
    COHERE_API_KEY=...
    ```
- Review `src/config.py` and `jobs/jobs_config.py` to tailor project paths, model names, etc.

### 3. Database Setup

```bash
# As postgres user
psql
CREATE DATABASE mailparser;
\q

# In your shell/project root
psql -U postgres -d mailparser -f database_schema.sql
```
Creates three JSON tables: `json_site_details`, `json_maintenance_details`, `json_vendor_details`.

### 4. Systemd Automation

- To automate moving new `.eml` files from `emails/sample_eml/` to `emails/processed_emails/` every 15 minutes:
    1. Copy the service/timer files to `/etc/systemd/system/`:
        ```bash
        sudo cp jobs/move_sample_to_processed/move_emails.{service,timer} /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable --now move_emails.timer
        ```
    2. Check logs and status:
        ```bash
        sudo systemctl status move_emails.timer
        sudo systemctl status move_emails.service
        sudo journalctl -u move_emails.service --no-pager -n 30
        ```

### 5. LLM Extraction

- To manually extract key JSON data from a sample email:
    ```bash
    python -m src.services.llm_service
    ```
- Output is printed and logged, using the template in `prompts/llm_prompt.txt`.

## Systemd Common Issues

- **If you move/rename scripts or service files**, update `/etc/systemd/system/move_emails.service` accordingly, then run `sudo systemctl daemon-reload`.
- **Permissions:** Systemd jobs typically run as root; to change, add `User=YOURUSER` in your service file.
- **Old log errors are preserved:** Always confirm fixes by reviewing only the latest lines of `journalctl`.

## Extending The Pipeline

- **To parse and insert results into PostgreSQL**:  
  Write a parser to read from `processed_emails/`, use LLM extraction, and insert into the appropriate `json_maintenance_details` etc. table.
- **To automate further:**  
  Create new jobs (in `jobs/`), register them as systemd services/timers, and document their paths/working directories for maintainability.

## License
Specify your license here (MIT, Apache, Proprietary, etc.).

## Author & Contributions

Primary maintainer: Deepak  
Contributions welcome—see [CONTRIBUTING.md] if available.

## FAQ

- **How do I add a new systemd job?**  
  Place your script and unit files under `jobs/`, copy to `/etc/systemd/system/`, `daemon-reload`, then enable/start as needed.

- **Why won’t my systemd job see my Python imports?**  
  Check that the sys.path includes the project root in your script, or always set the correct `WorkingDirectory` in your .service file.

**For bug reports or questions, open an issue or contact the maintainer.**

Let me know if you'd like this customized further for team setup, database connect details, LLM configuration, or anything else!