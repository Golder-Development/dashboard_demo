import pandas as pd
import streamlit as st
import os
from utils.logger import logger, log_function_call
from data.data_utils import is_file_updated


@log_function_call
def load_donorList_data(main_file,
                        cleaned_file,
                        streamlitrun=True,
                        output_csv=False):
    output_dir = st.session_state.directories["output_dir"]
    cleaned_file_path = os.path.join(output_dir, cleaned_file)

    # Check if we can use cached cleaned data
    if not is_file_updated(main_file, "donorlist_last_modified") and os.path.exists(cleaned_file_path):
        logger.info("Loading pre-cleaned donor list data.")
        return pd.read_csv(cleaned_file_path)

    # Load and clean the data
    if streamlitrun:
        donorlist_df = st.session_state.get("data_clean", None)
        if donorlist_df is None:
            st.error("No data found in session state!")
            return None
    else:
        donorlist_df = pd.read_csv(main_file) if main_file else None
        if donorlist_df is None:
            return None

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
        donorlist_df.to_csv(cleaned_file_path, index=False)

    return donorlist_df


@log_function_call
def load_regulated_entity_data(main_file,
                               cleaned_file,
                               streamlitrun=True,
                               output_csv=False):
    output_dir = st.session_state.directories["output_dir"]
    cleaned_file_path = os.path.join(output_dir, cleaned_file)

    # Check if we can use cached cleaned data
    if not is_file_updated(main_file, "regentity_last_modified") and os.path.exists(cleaned_file_path):
        logger.info("Loading pre-cleaned regulated entity data.")
        return pd.read_csv(cleaned_file_path)

    # Load and clean the data
    if streamlitrun:
        regent_df = st.session_state.get("data_clean", None)
        if regent_df is None:
            st.error("No data found in session state!")
            return None
    else:
        regent_df = pd.read_csv(main_file) if main_file else None
        if regent_df is None:
            return None

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
        regent_df.to_csv(cleaned_file_path, index=False)

    return regent_df
