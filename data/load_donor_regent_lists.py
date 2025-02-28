import pandas as pd
import streamlit as st
import os
from components import mappings as mp
from components import calculations as calc
from utils.logger import logger, log_function_call


@log_function_call
def load_donorList_data(datafile=None, streamlitrun=True, output_csv=False):
    if streamlitrun:
        # Load the data
        output_dir = st.session_state.directories["output_dir"]

        donorlist_df = st.session_state.get("data_clean", None)
        if donorlist_df is None:
            st.error("No data found in session state!")
            return None
    else:
        if datafile is None:
            donorlist_df = donorlist_df
        else:
            donorlist_df = datafile
    donorlist_df = (
        donorlist_df.groupby(["DonorId", "DonorName"])
        .agg({"Value": ["sum", "count", "mean"]})
        .reset_index()
    )
    donorlist_df.columns = [
        "DonorId",
        "Donor Name",
        "Donations Value",
        "Donation Events",
        "Donation Mean",
    ]
    if output_csv:
        output_dir = st.session_state.directories["output_dir"]
        cleaned_donor_filename = st.session_state.cleaned_donorlist_fname
        cleaned_donor_filename = os.path.join(output_dir, cleaned_donor_filename)
        donorlist_df.to_csv(cleaned_donor_filename)

    return donorlist_df


@log_function_call
def load_regulated_entity_data(datafile=None, streamlitrun=True, output_csv=False):
    # Load the data
    output_dir = st.session_state.directories["output_dir"]
    if streamlitrun:
        regent_df = st.session_state.get("data_clean", None)
        if regent_df is None:
            st.error("No data found in session state!")
            return None
    else:
        if datafile is None:
            regent_df = regent_df
        else:
            regent_df = datafile
    regent_df = (
        regent_df.groupby(
            ["RegulatedEntityId", "RegulatedEntityName", "RegEntity_Group"],
            observed=True,
        )
        .agg({"Value": ["sum", "count", "mean"]})
        .reset_index()
    )
    regent_df.columns = [
        "RegulatedEntityId",
        "Regulated Entity Name",
        "Regulated Entity Group",
        "Donations Value",
        "Donation Events",
        "Donation Mean",
    ]
    if output_csv:
        output_dir = st.session_state.directories["output_dir"]
        cleaned_regentity_filename = st.session_state.cleaned_regentity_fname
        cleaned_regentity_filename = os.path.join(
            output_dir, cleaned_regentity_filename
        )
        regent_df.to_csv(cleaned_regentity_filename)

    return regent_df
