import logging
import os
from functools import wraps

# Allow dynamic control of log level via environment variable or a default
# to change via terminal: export LOG_LEVEL=DEBUG (linux), set LOG_LEVEL=DEBUG (Windows)
# or alter in config.py
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()  # Can be DEBUG, INFO, WARNING, ERROR, CRITICAL

# Configure logging correctly
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),  # Defaults to INFO if invalid
    format="%(asctime)s %(levelname)s:%(message)s",
    datefmt="%Y/%m/%d %I:%M:%S %p",
    encoding="utf-8",
    handlers=[
        logging.FileHandler("logs/app_log.log"),  # Logs to a file
        logging.StreamHandler()  # Logs to console
    ]
)

# Get a logger instance
logger = logging.getLogger("StreamlitApp")


def log_function_call(func):
    """Decorator to log function calls, arguments, and return values."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")  # Use DEBUG for detailed logs
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} executed successfully")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            raise e
    return wrapper


logger.info(f"Logging is set up correctly! Current log level: {LOG_LEVEL}")
