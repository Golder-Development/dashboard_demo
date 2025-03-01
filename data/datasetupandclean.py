import pandas as pd
import streamlit as st
import os
from data.data_utils import is_file_updated
from data.raw_data_clean import raw_data_cleanup
from utils.global_variables import initialize_session_state
from utils.logger import logger, log_function_call  # Import decorator


@log_function_call
@st.cache_data
def load_raw_data(output_csv=False,
                  dedupe_donors=False,
                  dedupe_regentity=False):
    # Ensure session state variables are initialized
    if (
        "BASE_DIR" not in st.session_state
        or "directories" not in st.session_state
        or "filenames" not in st.session_state
        or "ec_donations_fname" not in st.session_state
    ):
        initialize_session_state()

    originaldatafilepath = st.session_state.ec_donations_fname
    cleaned_donations_file = st.session_state.cleaned_donations_fname

    # Check if we can use cached cleaned data
    if not is_file_updated(originaldatafilepath, "raw_data_last_modified") and os.path.exists(cleaned_donations_file):
        logger.info("Loading pre-cleaned raw data.")
        return pd.read_csv(cleaned_donations_file, index_col="index")

    # Load and clean the raw data
    loaddata_df = pd.read_csv(
        originaldatafilepath,
        dtype={
            "index": "int64",
            "ECRef": "object",
            "RegulatedEntityName": "object",
            "RegulatedEntityType": "object",
            "Value": "object",
            "AcceptedDate": "object",
            "AccountingUnitName": "object",
            "DonorName": "object",
            "AccountingUnitsAsCentralParty": "object",
            "IsSponsorship": "string",
            "DonorStatus": "object",
            "RegulatedDoneeType": "object",
            "CompanyRegistrationNumber": "object",
            "Postcode": "object",
            "DonationType": "object",
            "NatureOfDonation": "object",
            "PurposeOfVisit": "object",
            "DonationAction": "object",
            "ReceivedDate": "object",
            "ReportedDate": "object",
            "IsReportedPrePoll": "string",
            "ReportingPeriodName": "object",
            "IsBequest": "string",
            "IsAggregation": "string",
            "RegulatedEntityId": "object",
            "AccountingUnitId": "object",
            "DonorId": "object",
            "CampaigningName": "object",
            "RegisterName": "object",
            "IsIrishSource": "string",
        },
        index_col="index",
    )

    # Print progress message
    st.write("Base Data loaded successfully")
    st.write(f"Data has {loaddata_df.shape[0]} rows and {loaddata_df.shape[1]} columns")

    # Cleanse the raw data
    loaddata_df = raw_data_cleanup(loaddata_df,
                                   dedupe_donors=dedupe_donors,
                                   dedupe_regentity=dedupe_regentity)

    # Save cleaned data if required
    if output_csv:
        loaddata_df.to_csv(cleaned_donations_file)

    return loaddata_df
