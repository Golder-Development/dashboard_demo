import streamlit as st
import os
import pandas as pd
from components import calculations as calc
from utils.logger import log_function_call, logger


@st.cache_data
@log_function_call
def initialise_data():
    """
    initialises data for the app
    """

    loading_message = st.empty()
    loading_message.markdown(
        "<h3 style='text-align: center; color: blue;'>"
        "Please wait while the data sets are being "
        "calculated...</h3>",
        unsafe_allow_html=True,
    )
    from data.data_loader import firstload

    firstload()  # Load the data

    loading_message.empty()


@st.cache_data
@log_function_call
def load_entity_summary_data(main_file=None,
                             cleaned_file=None,
                             datafile=None,
                             streamlitrun=True,
                             output_csv=False):
    # Load the data
    output_dir = st.session_state.directories["output_dir"]
    cleaned_file_path = os.path.join(output_dir,
                                     cleaned_file)

    # Check if we can use cached cleaned data
    if not is_file_updated(main_file, "regentity_last_modified") and os.path.exists(cleaned_file_path):
        logger.info("Loading pre-cleaned regulated entity data.")
        return pd.read_csv(cleaned_file_path)

    if streamlitrun:
        entitysummary_df = st.session_state.get("raw_data", None)
        if entitysummary_df is None:
            st.error("No data found in session state!")
            return None
    else:
        if datafile is None:
            st.error("No data found in session state!")
        else:
            entitysummary_df = datafile
    # Create a DataFrame with the sum, count and mean of the donations
    # for each RegulatedEntityName
    RegulatedEntity_df = (
        entitysummary_df.groupby(["RegulatedEntityName"])
        .agg({"Value": ["sum", "count", "mean"]})
        .reset_index()
    )
    # Rename columns
    RegulatedEntity_df.columns = [
        "RegulatedEntityName",
        "DonationsValue",
        "DonationEvents",
        "DonationMean",
    ]

    # Add RegEntity_Group column based on thresholds
    thresholds = st.session_state.thresholds
    RegulatedEntity_df["RegEntity_Group"] = calc.determine_groups_optimized(
        RegulatedEntity_df, "RegulatedEntityName", "DonationEvents", thresholds
    )

    # generate CSV file of summary data
    if output_csv:
        output_dir = st.session_state.directories["output_dir"]
        party_filename = st.session_state.party_summary_fname
        party_filename = os.path.join(output_dir, party_filename)
        RegulatedEntity_df.to_csv(party_filename)

    return RegulatedEntity_df


@log_function_call
def get_file_modification_time(filepath):
    """Returns the last modification time of the given file."""
    return os.path.getmtime(filepath) if os.path.exists(filepath) else None


@log_function_call
def is_file_updated(main_file, timestamp_key):
    """Checks if the main file has been updated
    since the last recorded timestamp."""
    current_mod_time = get_file_modification_time(main_file)
    last_mod_time = st.session_state.get(timestamp_key, None)

    if last_mod_time is None or (current_mod_time and
                                 current_mod_time > last_mod_time):
        # Update the session state with the new timestamp
        st.session_state[timestamp_key] = current_mod_time
        return True  # File has changed
    return False  # File is unchanged
