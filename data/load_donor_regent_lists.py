import pandas as pd
import streamlit as st
from components.calculations import determine_groups_optimized
from utils.logger import (log_function_call,
                          logger,
                          )
from data.data_utils import try_to_use_preprocessed_data


@log_function_call
def load_donorList_data(main_file="data_clear",
                        cleaned_file="data_donor",
                        streamlitrun=True,
                        output_csv=False,
                        originaldatafilepath="cleaned_data_fname",
                        cleaneddatafilepath="cleaned_donorlist_fname"):
    if (
        st.session_state.get(originaldatafilepath) is None
        or st.session_state.get(cleaneddatafilepath) is None
        or st.session_state.get(main_file) is None
    ):
        st.error(f"Session state variables not initialized! {__name__}")
        logger.error(f"Session state variables not initialized! {__name__}")
        return None

    # Check if we can use cached cleaned data
    originaldatafilepath = st.session_state.get(originaldatafilepath)
    cleaneddatafilepath = st.session_state.get(cleaneddatafilepath)
    # Use function to check if file has been updated and if not,
    # load preprocessed data
    loaddata_df = try_to_use_preprocessed_data(
        originalfilepath=originaldatafilepath,
        savedfilepath=cleaneddatafilepath,
        timestamp_key="load_donorlist_data_last_modified")
    # Check if cached data loaded successfully and return it
    if loaddata_df is not None:
        return loaddata_df

    # Load and clean the data
    if streamlitrun:
        donorlist_df = st.session_state.get(main_file)
        if donorlist_df is None:
            st.error(f"No data found in session state! {__name__}")
            logger.error(f"No data found in session state! {__name__}")
            return None
    else:
        donorlist_df = (
            pd.read_csv(cleaneddatafilepath) if cleaneddatafilepath else None
        )
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
        donorlist_df.to_csv(cleaneddatafilepath, index=False)
        logger.info(f"Donor data saved to {cleaneddatafilepath}")
    if logger.level <= 20:
        st.info("Donor data summary successfully")
        st.info(f"Data has {donorlist_df.shape[0]} rows "
                f"and {donorlist_df.shape[1]} columns")

    logger.info("Donor Data summary completed")
    logger.info(f"Data shape: {donorlist_df.shape}")
    return donorlist_df


@log_function_call
def load_regulated_entity_data(
    main_file="data_clean",
    cleaned_file="data_regentity",
    streamlitrun=True,
    output_csv=False,
    originaldatafilepath="cleaned_data_fname",
    cleaneddatafilepath="cleaned_regentity_fname",
        ):
    if (
        st.session_state.get(main_file) is None
        or st.session_state.get(originaldatafilepath) is None
        or st.session_state.get(cleaneddatafilepath) is None
    ):
        st.error(f"Session state variables not initialized! {__name__}")
        logger.error(f"Session state variables not initialized! {__name__}")
        return None

    # Check if we can use cached cleaned data
    originaldatafilepath = st.session_state.get(originaldatafilepath)
    cleaneddatafilepath = st.session_state.get(cleaneddatafilepath)
    # Use function to check if file has been updated and if not,
    # load preprocessed data
    loaddata_df = try_to_use_preprocessed_data(
        originalfilepath=originaldatafilepath,
        savedfilepath=cleaneddatafilepath,
        timestamp_key="load_donorlist_data_last_modified")
    # Check if cached data loaded successfully and return it
    if loaddata_df is not None:
        return loaddata_df

    # Load and clean the data
    if streamlitrun:
        try:
            regent_df = st.session_state.get(main_file)
        except Exception as e:
            logger.error(f"Error loading {main_file} from session state: {e}")
            return None
    else:
        regent_df = (
            pd.read_csv(cleaneddatafilepath) if cleaneddatafilepath else None
        )
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
        regent_df.to_csv(cleaneddatafilepath, index=False)
        logger.info(f"Regulated entity data saved to {cleaneddatafilepath}")
    if logger.level <= 20:
        st.info("Regulated entity data successfully")
        st.info(f"Data has {regent_df.shape[0]} rows "
                f"and {regent_df.shape[1]} columns")

    logger.info("Raw Data cleanup completed")
    logger.info(f"Data shape: {regent_df.shape}")

    return regent_df


# @st.cache_data
# @log_function_call
# def load_entity_summary_data(
#         main_file="raw_data",
#         cleaned_file="party_summary_fname",
#         datafile=None,
#         output_csv=False,
#         streamlitrun=True,
#         originaldatafilepath="cleaned_data_fname",
#         cleaneddatafilepath="party_summary_fname"
#         ):
#     if (
#         st.session_state.get(main_file) is None
#         or st.session_state.get(originaldatafilepath) is None
#         or st.session_state.get(cleaneddatafilepath) is None
#     ):
#         st.error(f"Session state variables not initialized! {__name__}")
#         logger.error(f"Session state variables not initialized! {__name__}")
#         return None
#     # Check if we can use cached cleaned data
#     originaldatafilepath = st.session_state.get(originaldatafilepath)
#     cleaned_data_file = st.session_state.get(cleaneddatafilepath)
#     # Use function to check if file has been updated and if not,
#     # load preprocessed data
#     loaddata_df = try_to_use_preprocessed_data(originaldatafilepath,
#                                                cleaned_data_file,
#                                                "entity_summary_last_modified")
#     # Check if cached data loaded successfully and return it
#     if loaddata_df is not None:
#         return loaddata_df

#     if streamlitrun:
#         entitysummary_df = st.session_state.get(main_file)
#         if entitysummary_df is None:
#             st.error(f"No data found in session state! {__name__}")
#             logger.error(f"No data found in session state! {__name__}")
#             return None
#     else:
#         if datafile is None:
#             st.error("No datafile passed for entity summary creation!")
#             logger.error("No datafile passed for entity summary creation!")
#         else:
#             entitysummary_df = datafile
#             if logger.level <= 20:
#                 st.info("Data loaded from datafile passed to function")
#             logger.error("Data loaded from datafile passed to function")

#     # Create a DataFrame with the sum, count and mean of the donations
#     # for each RegulatedEntityName
#     RegulatedEntity_df = (
#         entitysummary_df.groupby(["RegulatedEntityName"])
#         .agg({"Value": ["sum", "count", "mean"]})
#         .reset_index()
#     )
#     # Rename columns
#     RegulatedEntity_df.columns = [
#         "RegulatedEntityName",
#         "DonationsValue",
#         "DonationEvents",
#         "DonationMean",
#     ]

#     # Add RegEntity_Group column based on thresholds
#     thresholds = st.session_state.thresholds
#     RegulatedEntity_df["RegEntity_Group"] = determine_groups_optimized(
#         RegulatedEntity_df,
#         "RegulatedEntityName",
#         "DonationEvents",
#         thresholds
#     )

#     # generate CSV file of summary data
#     if output_csv:
#         RegulatedEntity_df.to_csv(cleaned_data_file)
#         logger.info(f"Regulated entity summary saved to {cleaned_data_file}")
#     if logger.level <= 20:
#         st.info("Regulated entity summary successfully")
#         st.info(f"Data has {RegulatedEntity_df.shape[0]} rows "
#                 f"and {RegulatedEntity_df.shape[1]} columns")

#     logger.info("Raw Data cleanup completed")
#     logger.info(f"Data shape: {RegulatedEntity_df.shape}")

#     return RegulatedEntity_df
