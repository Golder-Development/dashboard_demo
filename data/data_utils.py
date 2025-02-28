import streamlit as st
import os
from components import calculations as calc
from utils.logger import logger, log_function_call


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
def load_entity_summary_data(datafile=None, streamlitrun=True, output_csv=False):
    # Load the data
    output_dir = st.session_state.directories["output_dir"]

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
