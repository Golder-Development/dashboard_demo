# all globel variables and constants are defined here  #

import streamlit as st
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
    if "base_dir" not in st.session_state:
        st.session_state.base_dir = config.BASE_DIR

    # Initialize filenames
    if "filenames" not in st.session_state:
        st.session_state.filenames = config.FILENAMES

    # Initialize safe donors & dubious donation types
    if "safe_donor_types" not in st.session_state:
        st.session_state.safe_donor_types = config.SAFE_DONORS

    if "dubious_donation_types" not in st.session_state:
        st.session_state.dubious_donation_types = config.DUBIOUS_DONATION_TYPES

    # Initialize placeholders
    if "PLACEHOLDER_DATE" not in st.session_state:
        st.session_state.PLACEHOLDER_DATE = config.PLACEHOLDER_DATE

    if "PLACEHOLDER_ID" not in st.session_state:
        st.session_state.PLACEHOLDER_ID = config.PLACEHOLDER_ID

    # Initialize thresholds
    if "thresholds" not in st.session_state:
        st.session_state.thresholds = config.THRESHOLDS

    # Initialize partyparents
    if "partyparents" not in st.session_state:
        st.session_state.partyparents = config.PARTYPARENTS

    # Initialize directories
    if "directories" not in st.session_state:
        st.session_state.directories = config.DIRECTORIES

    # ensure directories exist
    for key, value in st.session_state.directories.items():
        if not os.path.exists(value):
            os.makedirs(value)  # create the directory if it does not exist