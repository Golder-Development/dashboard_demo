import pandas as pd
import streamlit as st
import os
from rapidfuzz import process, fuzz
from collections import defaultdict
from components import mappings as mp
from components import calculations as calc
from utils.logger import logger
from utils.decorators import log_function_call  # Import decorator


def load_cleaned_data(datafile=None, streamlitrun=True, output_csv=False):
    if streamlitrun:
        # Load the data
        output_dir = st.session_state.directories["output_dir"]

        orig_df = st.session_state.get("raw_data", None)
        if orig_df is None:
            st.error("No data found in session state!")
            return None
    else:
        if datafile is None:
            orig_df = orig_df
        else:
            orig_df = datafile

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
    loadclean_df[columns_to_fill] = loadclean_df[columns_to_fill].replace("", pd.NA)
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
            loadclean_df["ReceivedDate"], dayfirst=True, format="mixed", errors="coerce"
        )
        .dt.normalize()
        .fillna(st.session_state.get("PLACEHOLDER_DATE"))
    )
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
        loadclean_df["NatureOfDonation"] = loadclean_df["NatureOfDonation"].replace(
            {"Donation to nan": "Other", "Other Payment": "Other"}
        )

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
            "Session state variables filter_def must" " be initialized before use."
        )

    # Extend dubious donor criteria using session state variables
    loadclean_df["DubiousDonor"] = (
        (loadclean_df["DonorId"].eq(st.session_state.get("PLACEHOLDER_ID")).astype(int))
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
    DubiousDonationTypes = st.session_state["filter_def"].get("DubiousDonationType_ftr")
    loadclean_df["DubiousData"] = (
        loadclean_df["DubiousDonor"]
        + (loadclean_df["DonationType"].isin(DubiousDonationTypes).astype(int))
        + loadclean_df["DonationAction"].ne("Accepted").astype(int)
        + loadclean_df["IsAggregation"].eq("True").astype(int)
        + (loadclean_df["NatureOfDonation"].eq("Aggregated Donation").astype(int))
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
        + (loadclean_df["RegulatedEntityName"].eq("Unidentified Entity").astype(int))
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

    # Ensure all columns that are in data are also in data_clean
    for col in orig_df.columns:
        if col not in loadclean_df.columns:
            loadclean_df[col] = orig_df[col]

    # change IsBequest, IsAggregation, IsSponsorship to boolean
    loadclean_df["IsBequest"] = loadclean_df["IsBequest"].astype(bool)
    loadclean_df["IsAggregation"] = loadclean_df["IsAggregation"].astype(bool)
    loadclean_df["IsSponsorship"] = loadclean_df["IsSponsorship"].astype(bool)

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
    # # Calculate the number of days to the next election
    # df["DaysTillNextElection"] = df["ReceivedDate"].map(
    #     lambda x: ger.GenElectionRelation2(x,
    #           direction="DaysTill",
    #           date_format='%Y/%m/%d %H:%M:%S')
    # )

    # # Calculate the number of days since the last election
    # df["DaysSinceLastElection"] = df["ReceivedDate"].map(
    #     lambda x: ger.GenElectionRelation2(x,
    #           direction="DaysSince",
    #           date_format='%Y/%m/%d %H:%M:%S')
    # )

    # # Apply the function to calculate weeks till the next election
    # df['WeeksTillNextElection'] = df['ReceivedDate'].apply(
    #     lambda x: GenElectionRelation2(x, divisor=7, direction="DaysTill")
    # )

    # # Apply the function to calculate weeks since the last election
    # df['WeeksSinceLastElection'] = df['ReceivedDate'].apply(
    #     lambda x: GenElectionRelation2(x, divisor=7, direction="DaysSince")
    # )

    # # Apply the function to calculate qtrs till the next election
    # df['WeeksTillNextElection'] = df['ReceivedDate'].apply(
    #     lambda x: GenElectionRelation2(x, divisor=91, direction="DaysTill")
    # )

    # # Apply the function to calculate qtrs since the last election
    # df['WeeksSinceLastElection'] = df['ReceivedDate'].apply(
    #     lambda x: GenElectionRelation2(x, divisor=91, direction="DaysSince")
    # )
    # Save cleaned data
    if output_csv:
        output_dir = st.session_state.directories["output_dir"]
        cleaned_data_filename = st.session_state.cleaned_data_fname
        cleaned_data_filename = os.path.join(output_dir, cleaned_data_filename)
        # Save the cleaned data to a CSV file for further analysis or reporting
        loadclean_df.to_csv(cleaned_data_filename)
    logger.info(f"Cleaned Data completed, shape: {loadclean_df.shape}")
    return loadclean_df
