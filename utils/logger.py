import logging
import os
import sys
import time
import functools
import streamlit as st
from functools import wraps

# Allow dynamic control of log level via environment variable or a default
# to change via terminal: export LOG_LEVEL=DEBUG (linux),
# set LOG_LEVEL=DEBUG (Windows)
# or alter in config.py
# Use DEBUG for detailed logs
# Can be DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = os.getenv("LOG_LEVEL", "ERROR").upper()

# Configure logging correctly,  # Defaults to INFO if invalid
# Ensure timestamps use local time with offset and seconds for clarity
logging.Formatter.converter = time.localtime
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s %(levelname)s:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %z",
    encoding="utf-8",
    handlers=[
        # Logs to a file
        logging.FileHandler("logs/app_log.log", encoding="utf-8"),
        # Logs to console
        logging.StreamHandler(sys.stdout)
    ]
)

# Get a logger instance
logger = logging.getLogger("StreamlitApp")


def log_function_call(func):
    """Decorator to log function calls, arguments, and return values.
    Improved to reduce duplicate logs"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.debug(f"Calling {func.__name__} with"
                         " args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} executed successfully")
            return result
        except Exception as e:
            # check if error is already logged at a higher level
            if not hasattr(st.session_state, "error_logged"):
                logger.error(f"Error in {func.__name__}:"
                             f" {e}", exc_info=True)
                st.session_state.error_logged = True
                st.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper


logger.info(f"Logging is set up correctly! Current log level: {LOG_LEVEL}")


def init_state_var(var_name, config_value):
    if var_name not in st.session_state:
        st.session_state[var_name] = config_value
        return logger.debug(f"Initialised {var_name} with value: {config_value}")
    else:
        return logger.debug(f"{var_name} already exists in session state")
