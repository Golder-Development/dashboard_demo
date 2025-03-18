import logging
import os
import sys
import functools
import streamlit as st
# from functools import wraps

# Allow dynamic control of log level via environment variable or a default
# to change via terminal: export LOG_LEVEL=DEBUG (linux),
# set LOG_LEVEL=DEBUG (Windows)
# or alter in config.py
# Use DEBUG for detailed logs
# Can be DEBUG, INFO, WARNING, ERROR, CRITICAL


# Allow dynamic control of log level via environment variable or config file
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()
# LOG_LEVEL = os.getenv("LOG_LEVEL", "ERROR").upper()
# Ensure logs directory exists

os.makedirs("logs", exist_ok=True)

# Streamlit App Logger
streamlit_logger = logging.getLogger("StreamlitApp")
streamlit_logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

streamlit_file_handler = logging.FileHandler("logs/Streamlit_log.log",
                                             encoding="utf-8")
streamlit_console_handler = logging.StreamHandler(sys.stdout)

formatter = logging.Formatter("%(asctime)s %(levelname)s:%(message)s",
                              datefmt="%Y/%m/%d %I:%M")

streamlit_file_handler.setFormatter(formatter)
streamlit_console_handler.setFormatter(formatter)

streamlit_logger.addHandler(streamlit_file_handler)
streamlit_logger.addHandler(streamlit_console_handler)

# Data Pipeline Logger
datapipeline_logger = logging.getLogger("DataPipeline")
datapipeline_logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

datapipeline_file_handler = logging.FileHandler("logs/data_pipeline.log",
                                                encoding="utf-8")
datapipeline_console_handler = logging.StreamHandler(sys.stdout)

datapipeline_file_handler.setFormatter(formatter)
datapipeline_console_handler.setFormatter(formatter)

datapipeline_logger.addHandler(datapipeline_file_handler)
datapipeline_logger.addHandler(datapipeline_console_handler)


def log_function_call(logger):
    """Decorator to log function calls, arguments, and return
       values using the correct logger."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                logger.debug(f"Calling {func.__name__} with"
                             f" args={args}, kwargs={kwargs}")
                result = func(*args, **kwargs)
                logger.info(f"{func.__name__} executed successfully")
                return result
            except Exception as e:
                if not hasattr(st.session_state, "error_logged"):
                    logger.error(f"Error in {func.__name__}: {e}",
                                 exc_info=True)
                    st.session_state.error_logged = True
                    st.error(f"Error in {func.__name__}: {e}")
                raise
        return wrapper
    return decorator


def init_state_var(var_name, config_value):
    # set logger for init state var
    logger = datapipeline_logger
    if var_name not in st.session_state:
        st.session_state[var_name] = config_value
        return logger.debug(f"Initialised {var_name} with"
                            f" value: {config_value}")
    else:
        return logger.debug(f"{var_name} already exists in session state")