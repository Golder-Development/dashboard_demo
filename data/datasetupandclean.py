import pandas as pd
import streamlit as st
from data.data_utils import try_to_use_preprocessed_data
from data.raw_data_clean import raw_data_cleanup
from utils.logger import (log_function_call,
                          logger,
                          )


@log_function_call
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

    logger.debug("Original data file path pre"
                 f" raw data load: {originaldatafilepath}")
    logger.debug("Processed data file path pre"
                 f" raw data load: {processeddatafilepath}")

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
        logger.info("Preprocessed data loaded successfully.")
    else:
        logger.info("Loading raw data...")
        logger.debug("Original data file path post"
                     f" raw data load: {originaldatafilepath}")
        logger.debug("Processed data file path post"
                     f" raw data load: {processeddatafilepath}")
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
        logger.info(f"Data loaded successfully."
                    f" Data has {loaddata_df.shape[0]} rows "
                    f"and {loaddata_df.shape[1]} columns")
        # Save the raw data to session state
        st.session_state.raw_data = loaddata_df
        if output_csv:
            from data.data_file_defs import save_dataframe_to_zip, normalize_string_columns_for_streamlit
            loaddata_df = normalize_string_columns_for_streamlit(loaddata_df)
            save_dataframe_to_zip(loaddata_df, processeddatafilepath, index=True)
            logger.info(f"Data saved to {processeddatafilepath.replace('.csv', '.zip')}")
        logger.info("Data saved to sessionstate as 'raw_data'")

    # Cleanse the raw data
    def imported_raw_data(loaddata_df):
        loaddata_df = raw_data_cleanup(
            loaddata_df=loaddata_df,
            dedupe_donors=dedupe_donors,
            dedupe_regentity=dedupe_regentity,
            output_csv=output_csv,
            originaldatafilepath=processeddatafilepath,
            processeddatafilepath="cleaned_donations_fname")
        return loaddata_df

    return imported_raw_data(loaddata_df)
