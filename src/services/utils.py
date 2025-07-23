import logging
from src.config import LOG_FILE


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
