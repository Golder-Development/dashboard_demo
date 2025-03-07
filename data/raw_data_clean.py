import streamlit as st
import pandas as pd
from data.data_utils import try_to_use_preprocessed_data
from data.data_dedupe import dedupe_entity_file
from utils.logger import (
    logger,
    log_function_call,  # Import decorator
    )


@log_function_call
def raw_data_cleanup(
    loaddata_df,
    output_csv=True,
    dedupe_donors=True,
    dedupe_regentity=True,
    originaldatafilepath="imported_raw_fname",
    processeddatafilepath="cleaned_donations_fname",
        ):
    """
    Clean up the raw data file - this is only run if the data has been updated
    since the last run.

    Args:
        loaddata_df (_type_): raw data as pandas dataframe
        output_csv (bool, optional): trigger for csv export.
        dedupe_donors (bool, optional): trigger to dedupe donors.
        dedupe_regentity (bool, optional): trigger to dedupe regentity.
        originaldatafilepath (_type_): path to the original data file
        processeddatafilepath (_type_): path to the processed data file

    Returns:
        loaddata_df: cleaned data file
    """
    logger.info("Cleaning up raw data")
    # Ensure session state variables are initialized
    if (
        st.session_state.get(originaldatafilepath) is None
        or st.session_state.get(processeddatafilepath) is None
    ):
        logger.error("Session state variables not initialized!")

    # check if processed data file exists and is relevant to original data file
    # if it does, load the processed data file, if not undertake data cleanup
    originaldatafilepath = st.session_state.get(originaldatafilepath)
    processeddatafilepath = st.session_state.get(processeddatafilepath)
    # Use function to check if file has been updated and if not,
    # load preprocessed data
    preloaddata_df = try_to_use_preprocessed_data(
        originalfilepath=originaldatafilepath,
        savedfilepath=processeddatafilepath,
        timestamp_key="cleaned_raw_data_last_modified")
    # Check if cached data loaded successfully and return it
    if preloaddata_df is not None:
        return preloaddata_df

    # Load and clean the raw data
    loaddata_df
    logger.info(f"Data loaded, shape: {loaddata_df.shape}")
    # Remove Currency sign of Value and convert to Float
    loaddata_df["Value"] = (
        loaddata_df["Value"]
        .replace({"£": "", ",": ""}, regex=True)
        .astype(float)
    )
    # Fill missing text fields with empty strings
    columns_to_fill = [
        "PurposeOfVisit",
        "DonorName",
        "CampaigningName",
        "AccountingUnitName",
        "ReportingPeriodName",
        "RegulatedEntityName",
        "DonationAction",
        "DonationType",
        "NatureOfDonation",
        "IsBequest",
        "IsAggregation",
        "IsSponsorship",
        "RegulatedDoneeType",
        "DonorStatus",
        "CompanyRegistrationNumber",
        "Postcode",
        "RegisterName",
        "IsIrishSource",
        "DonorId",
        "RegulatedEntityId",
        "AccountingUnitId",
        "ECRef",
    ]
    # label index to index
    loaddata_df.index.name = "index"
    # bulk change all columns to string and replace NaN with empty string
    loaddata_df[columns_to_fill] = (
        loaddata_df[columns_to_fill].fillna("").astype(str))
    # remove leading and trailing spaces from DonorName, RegulatedEntityName
    # remove leading and trailing spaces from DonorID and RegulatedEntityID
    # remove leading and trailing spaces from CampaignName and PurposeOfVisit
    # remove leading and trailing spaces from AccountingUnitName and
    # ReportingPeriodName
    columns_to_strip = [
        "DonorName",
        "RegulatedEntityName",
        "DonorId",
        "RegulatedEntityId",
        "CampaigningName",
        "PurposeOfVisit",
        "AccountingUnitName",
        "ReportingPeriodName",
    ]
    loaddata_df[columns_to_strip] = loaddata_df[columns_to_strip].apply(
        lambda x: x.str.strip()
    )
    # remove line returns and commas from DonorName, RegulatedEntityName,
    # CampaignName,
    # AccountingUnitName, ReportingPeriodName and PurposeOfVisit
    columns_to_clean = [
        "DonorName",
        "RegulatedEntityName",
        "PurposeOfVisit",
        "CampaigningName",
        "AccountingUnitName",
        "ReportingPeriodName",
    ]
    loaddata_df[columns_to_clean] = loaddata_df[columns_to_clean].replace(
        {",": "", "\n": " "}, regex=True
    )

    # standardise capitalisation of DonorName, RegulatedEntityName,
    # CampaignName,
    # AccountingUnitName, ReportingPeriodName and PurposeOfVisit
    columns_to_title = [
        "DonorName",
        "RegulatedEntityName",
        "PurposeOfVisit",
        "CampaigningName",
        "AccountingUnitName",
        "ReportingPeriodName",
    ]
    loaddata_df[columns_to_title] = loaddata_df[columns_to_title].apply(
        lambda x: x.str.title()
    )
    # rename "Total value of donations not reported individually"
    # to "Aggregated Donation" in DonationType
    loaddata_df["DonationType"] = loaddata_df["DonationType"].replace(
        {
            "Total value of donations not reported individually": "Aggregated Donation",
            "Permissible Donor Exempt Trust": "P.D. Exempt Trust",
        }
    )
    # update Blank DonorName to "Anonymous Donor"
    loaddata_df["DonorName"] = loaddata_df["DonorName"].replace(
        "", "Unidentified Donor"
    )

    # make donorid and regulatedentityid numeric
    loaddata_df["DonorId"] = (
        pd.to_numeric(loaddata_df["DonorId"], errors="coerce"))
    loaddata_df["RegulatedEntityId"] = pd.to_numeric(
        loaddata_df["RegulatedEntityId"], errors="coerce"
    )
    # update Blank RegulatedEntityName to "Unidentified Entity"
    loaddata_df["RegulatedEntityName"] = (
        loaddata_df["RegulatedEntityName"].replace(
            "", "Unidentified Entity"
        ))
    # update null or blank RegulatedEntityName to "Unidentified Entity"
    loaddata_df["RegulatedEntityName"] = (
        loaddata_df["RegulatedEntityName"].fillna("Unidentified Entity")
        )
    # update Blank DonorId to 1000001
    loaddata_df["DonorId"] = loaddata_df["DonorId"].fillna(1000001)
    # update Blank RegulatedEntityId to "1000001"
    loaddata_df["RegulatedEntityId"] = (
        loaddata_df["RegulatedEntityId"].fillna(1000001)
    )
    # update Blank RegisterName to "Other"
    loaddata_df["RegisterName"] = (
        loaddata_df["RegisterName"].replace("", "Other")
    )
    # update Blank DonationAction to "Accepted"
    loaddata_df["DonationAction"] = loaddata_df["DonationAction"].replace(
        "", "Accepted"
    )
    # update DonorStatus to Unidentified Donor if blank
    loaddata_df["DonorStatus"] = loaddata_df["DonorStatus"].replace(
        "", "Unidentified Donor"
    )
    if dedupe_regentity:
        loaddata_df = dedupe_entity_file(
            loaddata_dd_df=loaddata_df,
            entity="RegulatedEntity",
            map_filename="regentity_map_fname",
            output_csv=True
        )
    else:
        if logger.level <= 20:
            st.info("Deduping of Regulated Entities not selected")

    if dedupe_donors:
        loaddata_df = dedupe_entity_file(
            loaddata_dd_df=loaddata_df,
            entity="Donor",
            map_filename="donor_map_fname",
            output_csv=True
        )
    else:
        if logger.level <= 20:
            st.info("Deduping of Donors Entities not selected")

    # Print progress message
    logger.info("Raw Data cleanup completed")
    logger.info(f"Data shape: {loaddata_df.shape}")

    # Save cleaned data if required
    if output_csv:
        loaddata_df.to_csv(processeddatafilepath)
        logger.info(f"Data saved to {processeddatafilepath}")
    # Save the cleaned data to session state
    logger.info(f"Data cleanup completed, shape: {loaddata_df.shape}")

    return loaddata_df
