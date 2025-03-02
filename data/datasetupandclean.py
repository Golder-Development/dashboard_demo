import pandas as pd
import streamlit as st
from data.data_utils import try_to_use_preprocessed_data
from data.raw_data_clean import raw_data_cleanup
from utils.logger import (log_function_call,
                          logger,
                          )


@log_function_call
@st.cache_data
def load_raw_data(main_file="raw_data",
                  cleaned_file="raw_data_clean",
                  output_csv=True,
                  dedupe_donors=False,
                  dedupe_regentity=False,
                  originaldatafilepath="source_data_fname",
                  processeddatafilepath="imported_raw_fname"):
    # Ensure session state variables are initialized
    if (
        "BASE_DIR" not in st.session_state
    ):
        logger.critical("Base Dir Session state variables not initialized!")
        return None

    if (
        "directories" not in st.session_state
    ):        # Set the original data file path
        logger.critical("Directories Session state variables not initialized!")
        return None

    if (
        "filenames" not in st.session_state
        or st.session_state.get(originaldatafilepath) is None
        or st.session_state.get(processeddatafilepath) is None
    ):
        logger.critical(f"{originaldatafilepath} or {processeddatafilepath} "
                        "Session state variables not initialized!")
        return None

    logger.debug(f"Original data file path pre"
                 " raw data load: {originaldatafilepath}")
    logger.debug(f"Processed data file path pre"
                 " raw data load: {processeddatafilepath}")

    originaldatafilepath = st.session_state.get(originaldatafilepath)
    processeddatafilepath = st.session_state.get(processeddatafilepath)
    # Use function to check if file has been updated and if not,
    # load preprocessed data
    loaddata_df = try_to_use_preprocessed_data(
        originalfilepath=originaldatafilepath,
        savedfilepath=processeddatafilepath,
        timestamp_key="load_raw_data_last_modified")
    # Check if cached data loaded successfully and return it
    if loaddata_df is not None:
        return loaddata_df
    logger.info("Loading raw data...")
    logger.debug(f"Original data file path post"
                 " raw data load: {originaldatafilepath}")
    logger.debug(f"Processed data file path post"
                 " raw data load: {processeddatafilepath}")
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
    # set data min and max dates formatted as datetime format
    st.session_state.min_datetime = pd.to_datetime(loaddata_df["ReceivedDate"]).min()
    st.session_state.max_datetime = pd.to_datetime(loaddata_df["ReceivedDate"]).max()
    # set data min and max formatted dates - formatted to date only   
    st.session_state.min_date = st.session_state.min_datetime.date()
    st.session_state.max_date = st.session_state.max_datetime.date()
    
    # Print progress message
    if logger.level <= 20:
        st.info("Base Data loaded successfully")
        st.info(f"Data has {loaddata_df.shape[0]} rows "
                f"and {loaddata_df.shape[1]} columns")

    logger.info(f"Data loaded successfully. Data has {loaddata_df.shape[0]} rows "
                f"and {loaddata_df.shape[1]} columns")
    # Save the raw data to session state
    st.session_state.raw_data = loaddata_df
    if output_csv:
        loaddata_df.to_csv(processeddatafilepath)
        logger.info(f"Data saved to {processeddatafilepath}")
    # Save the raw data to session state
    st.session_state.raw_data_clean = loaddata_df
    
    # Cleanse the raw data
    loaddata_df = raw_data_cleanup(
        loaddata_df=loaddata_df,
        dedupe_donors=dedupe_donors,
        dedupe_regentity=dedupe_regentity,
        output_csv=output_csv,
        originaldatafilepath=processeddatafilepath,
        processeddatafilepath="cleaned_donations_fname")

    return loaddata_df
