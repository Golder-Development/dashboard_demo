import streamlit as st
import os
import pandas as pd
from utils.logger import log_function_call, logger


@st.cache_data
@log_function_call
def try_to_use_preprocessed_data(originalfilepath,
                                 savedfilepath,
                                 timestamp_key):
    """
    Checks if the original file has been updated and if not,
    loads the preprocessed data
    """
    logger.info(f"Original file path: {originalfilepath}")
    logger.info(f"Saved file path: {savedfilepath}")

    if originalfilepath is None:
        logger.error("Error: originalfilepath is None!")
        return None

    if not is_file_updated(originalfilepath,
                           timestamp_key) and os.path.exists(savedfilepath):
        logger.info(f"Loading preprocessed data. Using {savedfilepath}"
                    f" dated {timestamp_key} instead of {originalfilepath}")
        return pd.read_csv(savedfilepath)
    return None


@st.cache_data
@log_function_call
def initialise_data():
    """
    initialises data for the app
    """

    # import the firstload function
    from data.data_loader import firstload
    # Load the data
    logger.info("Running first load function.")
    firstload()
    # check that the all data has been loaded into the session state
    if "data_clean" not in st.session_state or \
            st.session_state.data_clean is None:
        logger.error("Data loading failed.")
        st.error("Data loading failed. Please check logs.")
        raise SystemExit("Data loading failed. Exiting.")
    else:
        logger.info("Data first load completed successfully.")
    return None


@log_function_call
def get_file_modification_time(filepath):
    """Returns the last modification time of the given file."""
    logger.info(f"Getting modification time for {filepath}")
    if os.path.exists(filepath):
        return os.path.getmtime(filepath)
    else:
        logger.warning(f"File {filepath} does not exist.")
        return None


@log_function_call
def is_file_updated(main_file, timestamp_key):
    """Checks if the main file has been updated
    since the last recorded timestamp."""
    logger.info(f"Checking if {main_file} has been updated.")
    current_mod_time = get_file_modification_time(main_file)
    logger.info(f"Current modification time: {current_mod_time}")
    last_mod_time = st.session_state.get(timestamp_key, None)
    logger.info(f"Last modification time: {last_mod_time}")
    if last_mod_time is None or (current_mod_time and
                                 current_mod_time > last_mod_time):
        # Update the session state with the new timestamp
        st.session_state[timestamp_key] = current_mod_time
        return True  # File has changed
    return False  # File is unchanged
