import logging
import os
import sys
import time
import functools
import streamlit as st
from functools import wraps

# Allow dynamic control of log level
LOG_LEVEL_STR = os.getenv("LOG_LEVEL", "ERROR").upper()
LOG_LEVEL = getattr(logging, LOG_LEVEL_STR, logging.INFO)

# 1. Ensure the logs directory exists
os.makedirs("logs", exist_ok=True)

# 2. Get the root logger
root_logger = logging.getLogger()
root_logger.setLevel(LOG_LEVEL)

# 3. Safely configure handlers so they persist and don't duplicate across Streamlit runs
# Clear existing handlers first to prevent duplicate log entries on hot-reloads
if root_logger.hasHandlers():
    root_logger.handlers.clear()

# Create formatters and handlers manually
log_formatter = logging.Formatter(
    fmt="%(asctime)s %(levelname)s:%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %z"
)
logging.Formatter.converter = time.localtime

# File Handler
file_handler = logging.FileHandler("logs/app_log.log", encoding="utf-8")
file_handler.setFormatter(log_formatter)
root_logger.addHandler(file_handler)

# Console Handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
root_logger.addHandler(console_handler)

# Get your named logger instance
logger = logging.getLogger("StreamlitApp")


def log_function_call(func):
    """Decorator to log function calls, arguments, and return values."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Fixed a minor bug: you used f"args={args}" inside a string, 
            # which printed literal "{args}" because of double bracing in python f-strings.
            logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} executed successfully")
            return result
        except Exception as e:
            # Check if error is already logged in this rerun cycle
            if not st.session_state.get("error_logged", False):
                logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
                st.session_state.error_logged = True
                st.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper


logger.info(f"Logging is set up correctly! Current log level: {LOG_LEVEL_STR}")


def init_state_var(var_name, config_value):
    if var_name not in st.session_state:
        st.session_state[var_name] = config_value
        logger.debug(f"Initialised {var_name} with value: {config_value}")
    else:
        logger.debug(f"{var_name} already exists in session state")
