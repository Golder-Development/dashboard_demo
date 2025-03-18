# all globel variables and constants are defined here  #
import streamlit as st
from pathlib import Path
from utils.logger import (log_function_call,
                          logger,
                          init_state_var)
import config as config  # Import the config file
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


@log_function_call("StreamlitApp")
def initialize_session_state():
    BASE_DIR = Path(os.getcwd())
    logger.info(f"BASE_DIR: {BASE_DIR}")

    # log current file and path
    """Load global variables into session_state if they are not already set."""
    # Initialize simple configuration values
    init_state_var("BASE_DIR", BASE_DIR)
    init_state_var("filenames", config.FILENAMES)
    init_state_var("PLACEHOLDER_DATE", config.PLACEHOLDER_DATE)
    init_state_var("PLACEHOLDER_ID", config.PLACEHOLDER_ID)
    init_state_var("thresholds", config.THRESHOLDS)
    init_state_var("data_remappings", config.DATA_REMAPPINGS)
    init_state_var("filter_def", config.FILTER_DEF)
    init_state_var("security", config.SECURITY)
    init_state_var("perc_target", config.perc_target)
    init_state_var("RERUN_MP_PARTY_MEMBERSHIP", config.RERUN_MP_PARTY_MEMBERSHIP)
    # Initialize directories
    init_state_var("directories", config.DIRECTORIES)

    # Ensure directories exist
    for key, path in config.DIRECTORIES.items():
        os.makedirs(path, exist_ok=True)  # Creates if not exists

    # Initialize directory references
    for dir_key in [
        "reference_dir",
        "data_dir",
        "output_dir",
        "logs_dir",
        "components_dir",
        "app_pages_dir",
        "utils_dir",
            ]:
        init_state_var(dir_key, config.DIRECTORIES.get(dir_key))

    # Initialize filenames using correct directory mapping
    for dir_key, filenames in config.FILENAMES.items():
        if isinstance(filenames, dict):  # process dictionary entries
            for fname_key, filename in filenames.items():
                file_path = (
                    os.path.join(config.DIRECTORIES.get(dir_key, ""), filename)
                )
                init_state_var(fname_key, file_path)

    # Initialize Cash_ftr filter
    init_state_var("Cash_ftr", config.FILTER_DEF.get("Cash_ftr"))

    # write session state as list to log
    logger.info("Session_state variables initialized")
    for key, value in st.session_state.items():
        logger.debug(f"{key}: {value}")

    return logger.info("Session state Setup complete")
# End of function initialize_session_state
# End of file
