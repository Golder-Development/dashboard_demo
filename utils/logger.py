import logging
from functools import wraps

# Configure logging correctly
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for detailed logs
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
        logger.info(f"Calling {func.__name__} with args={args}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} executed successfully")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            raise e
    return wrapper


logger.info("Logging is set up correctly!")
