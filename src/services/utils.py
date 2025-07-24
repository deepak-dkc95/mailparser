import logging
from src.config import (
    LOG_FILE, IMPORTANT_KEYWORDS, CANCELLATION_KEYWORDS
)

def setup_logger(name="Network-MailParser"):
    log_dir = LOG_FILE.parent
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Lowest log level

    # Avoid adding duplicate handlers if setup_logger is called multiple times
    if not logger.hasHandlers():
        formatter = logging.Formatter(
            fmt="%(name)s %(asctime)s [%(levelname)s] : %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

logger = setup_logger()

def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def is_important(subject):
    """Check if subject contains any important keywords."""
    return any(keyword.lower() in subject.lower() for keyword in IMPORTANT_KEYWORDS)

def is_maintenance(subject):
    """Check if subject contains 'maintenance' keyword."""
    return "maintenance" in subject.lower()

def check_cancelled(subject):
    """Check if subject contains any cancellation keywords."""
    return any(keyword.lower() in subject.lower() for keyword in CANCELLATION_KEYWORDS)