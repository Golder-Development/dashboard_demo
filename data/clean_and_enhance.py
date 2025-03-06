import pandas as pd
import numpy as np
import streamlit as st
from data.data_utils import try_to_use_preprocessed_data
from data.politicalperson import map_mp_to_party
from components import mappings as mp
from components import calculations as calc
from utils.logger import logger, log_function_call
from data.GenElectionRelationship import (
    load_election_dates
    )


@log_function_call
@st.cache_data
def load_cleaned_data(
        originaldatafilepath="cleaned_donations_fname",
        processeddatafilepath="cleaned_data_fname",
        datafile="raw_data",
        streamlitrun=True,
        output_csv=False,
        main_file="raw_data",
        cleaned_file="data_clean"):

    if (
        st.session_state.get(originaldatafilepath) is None
        or st.session_state.get(processeddatafilepath) is None
        or st.session_state.get(main_file) is None
    ):
        logger.error(f"Session state variables not initialized! {__name__}")
        st.error(f"Session state variables not initialized! {__name__}")
        return None
    logger.debug(f"Rows in Raw Data: {len(st.session_state.get(main_file))}")

    originaldatafilepath = st.session_state.get(originaldatafilepath)
    processeddatafilepath = st.session_state.get(processeddatafilepath)

    # Use function to check if file has been updated and if not,
    # load preprocessed data
    loaddata_df = try_to_use_preprocessed_data(
        originalfilepath=originaldatafilepath,
        savedfilepath=processeddatafilepath,
        timestamp_key="load_raw_data_last_modified")
    if loaddata_df is None:
        logger.error(f"Failed to load data from {originaldatafilepath}")
    # Check if cached data loaded successfully and return it
    if loaddata_df is not None:
        # check that number of rows in the loaded data is the same as the
        # number of rows in the original data
        if len(loaddata_df) == len(st.session_state.get(main_file)):
            return loaddata_df
        else:
            logger.error(
                f"Number of rows in loaded data ({len(loaddata_df)}) "
                f"does not match the number of rows in the original data "
                f"({len(st.session_state.get(main_file))})! {__name__}"
            )
            st.error(
                f"Number of rows in loaded data ({len(loaddata_df)}) "
                f"does not match the number of rows in the original data "
                f"({len(st.session_state.get(main_file))})! {__name__}"
            )
            logger.error(f"Reprocessing data... {__name__}")
            st.error(f"Reprocessing data... {__name__}")
    # start final processing - load and clean data
    logger.info(f"Loading and cleaning data... {__name__}")
    if streamlitrun:
        # Load the data
        orig_df = st.session_state.get(datafile)
        if orig_df is None:
            st.error(f"No data found in session state! {__name__}")
            logger.error(f"No data found in session state! {__name__}")
            return None
    else:
        if datafile is None:
            orig_df = orig_df
        else:
            orig_df = datafile
    logger.debug(f"Clean Data Prep: streamlitdata load: {len(orig_df)}")
    # create a copy of the original data
    loadclean_df = orig_df.copy()
    # Create simple column to enable count of events using sum
    loadclean_df["EventCount"] = 1
    # convert DonorId = "" to null
    loadclean_df["DonorId"] = loadclean_df["DonorId"].replace("", pd.NA)
    # Fill missing text fields with empty strings
    columns_to_fill = [
        "ReceivedDate",
        "ReportingPeriodName",
        "NatureOfDonation",
        "DonationAction",
        "DonationType",
    ]
    loadclean_df[columns_to_fill] = (
        loadclean_df[columns_to_fill].replace("", pd.NA)
    )
    # # Fill blank ReceivedDate with ReportedDate
    # Fill blank ReceivedDate with ReportedDate, AcceptedDate,
    # or ReportingPeriodName_Date
    loadclean_df["ReceivedDate"] = (
        loadclean_df["ReceivedDate"]
        .fillna(loadclean_df["ReportedDate"])
        .fillna(loadclean_df["AcceptedDate"])
        .fillna(
            pd.to_datetime(
                loadclean_df["ReportingPeriodName"].str.strip().str[-10:],
                dayfirst=True,
                format="mixed",
                errors="coerce",
            ).dt.normalize()
        )
    )
    # Convert ReceivedDate to datetime and set any remaining missing dates
    # to 1900-01-01
    loadclean_df["ReceivedDate"] = (
        pd.to_datetime(
            loadclean_df["ReceivedDate"],
            dayfirst=True,
            format="mixed",
            errors="coerce"
        )
        .dt.normalize()
        .fillna(st.session_state.PLACEHOLDER_DATE)
    )
    # Phase 1 - line 122 - Clean data prep
    logger.debug(f"Clean Data Prep 123: streamlitdata"
                 f" load: {len(loadclean_df)}")

    # Create Year and Month columns
    loadclean_df["YearReceived"] = loadclean_df["ReceivedDate"].dt.year
    loadclean_df["MonthReceived"] = loadclean_df["ReceivedDate"].dt.month
    loadclean_df["YearMonthReceived"] = (
        loadclean_df["YearReceived"] * 100 + loadclean_df["MonthReceived"]
    )
    # Handle NatureOfDonation based on other fields
    if "NatureOfDonation" in loadclean_df.columns:
        loadclean_df["NatureOfDonation"] = loadclean_df.apply(
            mp.map_nature_of_donation, axis=1
        )
        loadclean_df["NatureOfDonation"] = (
            loadclean_df["NatureOfDonation"].replace(
                {"Donation to nan": "Other", "Other Payment": "Other"}
               ))

    # apply mapping of MPs to party membership
    if "RegulatedEntityName" in loadclean_df.columns:
        try:
            loadclean_df = map_mp_to_party(loadclean_df)
        except Exception as e:
            logger.error(f"Error mapping MPs to party membership: {e}")
            st.error(f"Error mapping MPs to party membership: {e}"
                     " Political Party Matching will not be done")
            return loadclean_df
    logger.debug(f"Clean Data Prep 150: Map Mps: {len(loadclean_df)}")

    # Create a DubiousData flag for problematic records
    if ("PLACEHOLDER_DATE" not in st.session_state) or (
        "PLACEHOLDER_ID" not in st.session_state
    ):
        raise ValueError(
            "Session state variables PLACEHOLDER_DATE "
            "and PLACEHOLDER_ID must be initialized before use."
        )

    if "filter_def" not in st.session_state:
        raise ValueError(
            "Session state variables filter_def must"
            " be initialized before use."
        )

    # Extend dubious donor criteria using session state variables
    loadclean_df["DubiousDonor"] = (
        (loadclean_df["DonorId"].eq(st.session_state
                                    .get("PLACEHOLDER_ID")).astype(int))
        + (
            loadclean_df["DonorName"]
            .isin(["Unidentified Donor", "Anonymous Donor"])
            .astype(int)
        )
        + (
            loadclean_df["DonationType"]
            .isin(["Unidentified Donor", "Impermissible Donor"])
            .astype(int)
        )
    )
    DubiousDonationTypes = (
        st.session_state["filter_def"].get("DubiousDonationType_ftr")
    )
    loadclean_df["DubiousData"] = (
        loadclean_df["DubiousDonor"]
        + (loadclean_df["DonationType"].isin(DubiousDonationTypes).astype(int))
        + loadclean_df["DonationAction"].ne("Accepted").astype(int)
        + loadclean_df["IsAggregation"].eq("True").astype(int)
        + (loadclean_df["NatureOfDonation"]
            .eq("Aggregated Donation").astype(int))
        + (
            loadclean_df["ReceivedDate"]
            .eq(st.session_state.get("PLACEHOLDER_DATE"))
            .astype(int)
        )
        + (
            loadclean_df["RegulatedEntityId"]
            .eq(st.session_state.get("PLACEHOLDER_ID"))
            .astype(int)
        )
        + (loadclean_df["RegulatedEntityName"]
           .eq("Unidentified Entity").astype(int))
        + (
            loadclean_df["DonorId"]
            .eq(st.session_state.get("PLACEHOLDER_ID"))
            .astype(int)
        )
        + loadclean_df["DonorName"].eq("Unidentified Donor").astype(int)
        - (
            loadclean_df["DonorStatus"]
            .isin(st.session_state["filter_def"].get("SafeDonors_ftr"))
            .astype(int)
        )  # Safe donors should be excluded
        - (
            (
                (loadclean_df["IsAggregation"].eq("True"))
                & (
                    loadclean_df["DonorStatus"].isin(
                        st.session_state["filter_def"].get("SafeDonors_ftr")
                    )
                )
            ).astype(int)
        )  # Fixing subtraction
    )

    # if "DubiousData" is less than 0, set it to 0
    loadclean_df["DubiousData"] = loadclean_df["DubiousData"].clip(lower=0)

    # Apply dictionary to populate RegEntity_Group
    thresholds = st.session_state.thresholds
    if "RegulatedEntityName" in loadclean_df.columns:
        loadclean_df["RegEntity_Group"] = calc.determine_groups_optimized(
            loadclean_df, "RegulatedEntityName", "EventCount", thresholds
        )
    logger.debug(f"Clean Data Prep 235: RegEntity_Map: {len(loadclean_df)}")
    # Ensure all columns that are in data are also in data_clean
    for col in orig_df.columns:
        if col not in loadclean_df.columns:
            loadclean_df[col] = orig_df[col]

    # Drop Columns that are not needed
    loadclean_df = loadclean_df.drop(
        [
            "IsIrishSource",
            "AccountingUnitsAsCentralParty",
            "AccountingUnitName",
            "AcceptedDate",
            "ReportedDate",
            "IsReportedPrePoll",
            "AccountingUnitId",
            "Postcode",
            "CompanyRegistrationNumber",
            "CampaigningName",
        ],
        axis=1,
    )

    # Column encoding DonationType, RegulatedEntityName, DonorName,
    # DonationAction, DonorStatus,
    # CampaigningName, PurposeOfVisit, AccountingUnitName, ReportingPeriodName,
    # RegulatedDoneeType,
    # IsIrishSource, IsBequest, IsAggregation, IsSponsorship, NatureOfDonation,
    # RegisterName
    loadclean_df["DonationTypeInt"] = (
        loadclean_df["DonationType"].astype("category").cat.codes)
    loadclean_df["RegulatedEntityNameInt"] = (
        loadclean_df["RegulatedEntityName"].astype("category").cat.codes)
    loadclean_df["DonorNameInt"] = (
        loadclean_df["DonorName"].astype("category").cat.codes)
    loadclean_df["DonationActionInt"] = (
        loadclean_df["DonationAction"].astype("category").cat.codes)
    loadclean_df["DonorStatusInt"] = (
        loadclean_df["DonorStatus"].astype("category").cat.codes)
    # loadclean_df["CampaigningNameInt"] = (
    #     loadclean_df["CampaigningName"].astype("category").cat.codes)
    loadclean_df["PurposeOfVisitInt"] = (
        loadclean_df["PurposeOfVisit"].astype("category").cat.codes)
    # loadclean_df["AccountingUnitNameInt"] = (
    #     loadclean_df["AccountingUnitName"].astype("category").cat.codes)
    # loadclean_df["ReportingPeriodNameInt"] = (
    #     loadclean_df["ReportingPeriodName"].astype("category").cat.codes)
    loadclean_df["RegulatedDoneeTypeInt"] = (
        loadclean_df["RegulatedDoneeType"].astype("category").cat.codes)
    # loadclean_df["IsIrishSourceInt"] = (
    #     loadclean_df["IsIrishSource"].astype("category").cat.codes)
    loadclean_df["IsBequestInt"] = (
        loadclean_df["IsBequest"].astype("category").cat.codes)
    loadclean_df["IsAggregationInt"] = (
        loadclean_df["IsAggregation"].astype("category").cat.codes)
    loadclean_df["IsSponsorshipInt"] = (
        loadclean_df["IsSponsorship"].astype("category").cat.codes)
    loadclean_df["NatureOfDonationInt"] = (
        loadclean_df["NatureOfDonation"].astype("category").cat.codes)
    loadclean_df["RegisterNameInt"] = (
        loadclean_df["RegisterName"].astype("category").cat.codes)

    # Column encoding PublicFundsInt
    loadclean_df["PublicFundsInt"] = (
        loadclean_df["DonationType"]
        .apply(lambda x: 0 if x != "Public Funds" else 1))
    # Calculate the number of days to the next election and
    # since the last election
    # Ensure election dates are loaded
    if ("ElectionDatesAscend" not in st.session_state or
            "ElectionDatesDescend" not in st.session_state):
        load_election_dates()

    if st.session_state.ElectionDatesAscend is None:
        # set [DaysTillNextElection, DaysSinceLastElection,
        # WeeksTillNextElection, WeeksSinceLastElection,QtrsTillNextElection,
        # QtrsSinceLastElection] to None
        loadclean_df["DaysTillNextElection"] = None
        loadclean_df["DaysSinceLastElection"] = None
        loadclean_df["WksTillNextElection"] = None
        loadclean_df["WksSinceLastElection"] = None
        loadclean_df["QtrsTillNextElection"] = None
        loadclean_df["QtrsSinceLastElection"] = None
        loadclean_df["YrsTillNextElection"] = None
        loadclean_df["YrsSinceLastElection"] = None
        logger.error("Election dates could not be loaded. Returning None.")
        st.error("Election dates could not be loaded. Returning None.")
        return None
    else:
        # Convert election dates into Pandas Series
        loadclean_df["ReceivedDate"] = pd.to_datetime(
            loadclean_df["ReceivedDate"])
        election_dates_asc = pd.to_datetime(
            pd.Series(st.session_state.ElectionDatesAscend))
        election_dates_desc = pd.to_datetime(
            pd.Series(st.session_state.ElectionDatesDescend))

        # Calculate days till the next election and since the last election
        def get_days_till_next_election(date_series):
            date_series = pd.to_datetime(date_series)
            idx = np.searchsorted(election_dates_asc,
                                  date_series,
                                  side="left")
            valid_idx = idx < len(election_dates_asc)
            next_election_dates = np.where(valid_idx,
                                           election_dates_asc.iloc[idx],
                                           pd.NaT)
            return (pd.to_datetime(next_election_dates) - date_series).dt.days

        # Vectorized function for days since the last election
        def get_days_since_last_election(date_series):
            date_series = pd.to_datetime(date_series)
            idx = np.searchsorted(election_dates_desc,
                                  date_series,
                                  side="right") - 1
            valid_idx = idx >= 0
            last_election_dates = np.where(valid_idx,
                                           election_dates_desc.iloc[idx],
                                           pd.NaT)
            return (date_series - pd.to_datetime(last_election_dates)).dt.days
        # Apply vectorized calculations
        loadclean_df["DaysTillNextElection"] = (
            get_days_till_next_election(loadclean_df["ReceivedDate"])
            )
        loadclean_df["DaysSinceLastElection"] = (
            get_days_since_last_election(loadclean_df["ReceivedDate"])
            )

        # Compute weeks and quarters and years
        for period, divisor in [("Wks", 7), ("Qtrs", 91), ("Yrs", 365)]:
            loadclean_df[f"{period}TillNextElection"] = (
                np.ceil(loadclean_df["DaysTillNextElection"] / divisor))
            loadclean_df[f"{period}SinceLastElection"] = (
                np.ceil(loadclean_df["DaysSinceLastElection"] / divisor))

    logger.debug(f"Clean Data Prep 353: Election dates: {len(loadclean_df)}")
    # compare count of rows in original data with cleaned data
    if len(orig_df) != len(loadclean_df):
        logger.error(
            f"Number of rows in cleaned data ({len(loadclean_df)}) "
            f"does not match the number of rows in the original data "
            f"({len(orig_df)})! {__name__}"
        )
        st.error(
            f"Number of rows in cleaned data ({len(loadclean_df)}) "
            f"does not match the number of rows in the original data "
            f"({len(orig_df)})! {__name__}"
        )
        # Dedupe the data
        loadclean_df = loadclean_df.drop_duplicates()
        logger.info(
            f"Deduplication completed, shape: {loadclean_df.shape} {__name__}"
        )
        # compare count of rows in original data with cleaned data
        if len(orig_df) != len(loadclean_df):
            logger.error(
                "Post deduplication: "
                f"Number of rows in cleaned data ({len(loadclean_df)}) "
                f"does not match the number of rows in the original data "
                f"({len(orig_df)})! {__name__}"
            )
            st.error(
                "Post deduplication: "
                f"Number of rows in cleaned data ({len(loadclean_df)}) "
                f"does not match the number of rows in the original data "
                f"({len(orig_df)})! {__name__}, deduplication failed"
            )
            return ValueError("Deduplication failed")
    logger.debug(f"Clean Data Prep 386: End of clean: {len(loadclean_df)}")
    # Save cleaned data
    if output_csv:
        # Save the cleaned data to a CSV file for further analysis or reporting
        loadclean_df.to_csv(processeddatafilepath)
    logger.info(f"Cleaned Data completed, shape: {loadclean_df.shape}")
    logger.info("Data successfully cleaned")
    logger.info(f"Data has {loadclean_df.shape[0]} rows "
                f"and {loadclean_df.shape[1]} columns")
    # return the cleaned data
    return loadclean_df
