import streamlit as st
import os
import json
import pandas as pd
from utils.logger import log_function_call, logger
from data.data_file_defs import (load_source_data,
                                load_improved_raw_data,
                                load_cleaned_data,
                                load_cleaned_donations,
                                 )

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
        # Load last modified dates from the JSON file
        last_modified_dates = load_last_modified_dates()
        last_mod_time = last_modified_dates.get(timestamp_key, None)
        logger.info(f"Loading preprocessed data. Using {savedfilepath}"
                    f" dated {last_mod_time} instead of {originalfilepath}")
        return importfile(timestamp_key, savedfilepath)
    return None



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


def load_last_modified_dates():
    """Load the last modified dates from the JSON file."""
    try:
        with open('reference_files/last_modified_dates.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_last_modified_dates(last_modified_dates):
    """Save the updated last modified dates to the JSON file."""
    # Create the folder if it doesn't exist
    os.makedirs('reference_files', exist_ok=True)
    with open('reference_files/last_modified_dates.json', 'w') as f:
        json.dump(last_modified_dates, f, indent=4)


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

    # Load last modified dates from the JSON file
    last_modified_dates = load_last_modified_dates()

    # Get the current modification time of the file
    current_mod_time = get_file_modification_time(main_file)
    logger.info(f"Current modification time: {current_mod_time}")

    # Retrieve the last modification time from the loaded data
    last_mod_time = last_modified_dates.get(timestamp_key, None)
    logger.info(f"Last modification time: {last_mod_time}")

    # Check if the file has been updated
    if last_mod_time is None or (current_mod_time > last_mod_time):
        # Update the session state and the JSON file with the new timestamp
        last_modified_dates[timestamp_key] = current_mod_time
        st.session_state[timestamp_key] = current_mod_time

        # Save the updated modification times back to the JSON file
        save_last_modified_dates(last_modified_dates)

        return True # File has changed

    return False  # File is unchanged


def importfile(timestamp_key, savedfilepath):
    """
    Imports a file from the given path.
    Using a specified file definition
    """
    logger.info(f"Importing file from {savedfilepath}")

    if not os.path.exists(savedfilepath):
        logger.error(f"File {savedfilepath} does not exist.")
        return None
    elif os.path.getsize(savedfilepath) == 0:
        logger.error(f"File {savedfilepath} is empty.")
        return None
    elif timestamp_key == "load_raw_data_last_modified":
        loaddata_df = load_source_data(savedfilepath)
    elif timestamp_key == "cleaned_raw_data_last_modified":
        loaddata_df = load_improved_raw_data(savedfilepath)
    elif timestamp_key == "cleaned_data_last_modified":
        loaddata_df = load_cleaned_data(savedfilepath)
    elif timestamp_key == "cleaned_donations_last_modified":
        loaddata_df = load_cleaned_donations(savedfilepath)
    else:
        logger.error(f"Timestamp key {timestamp_key} not recognised.")
        return
    
    return loaddata_df
