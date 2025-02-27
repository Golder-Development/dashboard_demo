# all globel variables and constants are defined here  #

import streamlit as st
import logging
import config  # Import the config file
import os

"""
 To use the session_state object, you need to define the global variables
 and constants in a separate file. This is because the session_state object
 is not available at the time the global variables are defined. The global
 variables are defined in a separate file, and the session_state object is
 imported into the file where the global variables are defined.
 The session_state object is then used to define the global variables.
 The global variables are then imported into the file where the
 session_state object is defined. This way, the global variables are
 available to the session_state object.
"""


def initialize_session_state():
    """Load global variables into session_state if they are not already set."""
    # Define a helper function to initialize values from config
    def init_state_var(var_name, config_value):
        if var_name not in st.session_state:
            st.session_state[var_name] = config_value

    # Initialize simple configuration values
    init_state_var("BASE_DIR", config.BASE_DIR)
    init_state_var("filenames", config.FILENAMES)
    init_state_var("PLACEHOLDER_DATE", config.PLACEHOLDER_DATE)
    init_state_var("PLACEHOLDER_ID", config.PLACEHOLDER_ID)
    init_state_var("thresholds", config.THRESHOLDS)
    init_state_var("data_remappings", config.DATA_REMAPPINGS)
    init_state_var("filter_def", config.FILTER_DEF)
    init_state_var("security", config.SECURITY)
    # Initialize directories
    init_state_var("directories", config.DIRECTORIES)

    # Ensure directories exist
    for key, path in st.session_state.directories.items():
        os.makedirs(path, exist_ok=True)  # Creates if not exists

    # Initialize directory references
    for dir_key in [
        "reference_dir",
        "data_dir",
        "output_dir",
        "logs_dir",
        "components_dir",
        "app_pages_dir",
        "utils_dir"
        ]:
        init_state_var(dir_key, st.session_state["directories"].get(dir_key))


    # Initialize directories
    init_state_var("directories", config.DIRECTORIES)

    # Ensure directories exist
    for key, path in st.session_state.directories.items():
        os.makedirs(path, exist_ok=True)  # Create directory

    # Initialize filenames using correct directory mapping
    for dir_key, filenames in config.FILENAMES.items():
        if isinstance(filenames, dict):  # process dictionary entries
            for fname_key, filename in filenames.items():
                file_path = (
                    os.path.join(st.session_state["directories"].get(dir_key, ""), filename)
                )
                init_state_var(fname_key, file_path)

    # Handle `base_data` separately (since it's stored as a tuple)
    base_data_key, base_data_filename = config.FILENAMES["BASE_DIR"]
    base_data_path = os.path.join(st.session_state["BASE_DIR"],
                                  base_data_filename)
    init_state_var(base_data_key, base_data_path)

    # write to log
    logger = logging.getLogger(__name__)    
    logger.info(st.session_state)
