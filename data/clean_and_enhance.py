import pandas as pd
import streamlit as st
import os
from data.politicalperson import map_mp_to_party
from components import mappings as mp
from components import calculations as calc
from utils.logger import logger, log_function_call
from components.GenElectionRelationship import GenElectionRelation2

@log_function_call
@st.cache_data
def load_cleaned_data(datafile=None, streamlitrun=True, output_csv=False):
    if streamlitrun:
        # Load the data
        output_dir = st.session_state.directories["output_dir"]
        orig_df = st.session_state.raw_data
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
        .fillna(st.session_state.PLACEHOLDER_DATE)
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

    # apply mapping of MPs to party membership
    if "RegulatedEntityName" in loadclean_df.columns:
        loadclean_df = map_mp_to_party(loadclean_df)

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

    # Column encoding DonationType, RegulatedEntityName, DonorName, DonationAction, DonorStatus,
    # CampaigningName, PurposeOfVisit, AccountingUnitName, ReportingPeriodName, RegulatedDoneeType,
    # IsIrishSource, IsBequest, IsAggregation, IsSponsorship, NatureOfDonation, RegisterName
    loadclean_df["DonationTypeInt"] = loadclean_df["DonationType"].astype("category").cat.codes
    loadclean_df["RegulatedEntityNameInt"] = loadclean_df["RegulatedEntityName"].astype("category").cat.codes
    loadclean_df["DonorNameInt"] = loadclean_df["DonorName"].astype("category").cat.codes
    loadclean_df["DonationActionInt"] = loadclean_df["DonationAction"].astype("category").cat.codes
    loadclean_df["DonorStatusInt"] = loadclean_df["DonorStatus"].astype("category").cat.codes
    # loadclean_df["CampaigningNameInt"] = loadclean_df["CampaigningName"].astype("category").cat.codes
    loadclean_df["PurposeOfVisitInt"] = loadclean_df["PurposeOfVisit"].astype("category").cat.codes
    # loadclean_df["AccountingUnitNameInt"] = loadclean_df["AccountingUnitName"].astype("category").cat.codes
    # loadclean_df["ReportingPeriodNameInt"] = loadclean_df["ReportingPeriodName"].astype("category").cat.codes
    loadclean_df["RegulatedDoneeTypeInt"] = loadclean_df["RegulatedDoneeType"].astype("category").cat.codes
    # loadclean_df["IsIrishSourceInt"] = loadclean_df["IsIrishSource"].astype("category").cat.codes
    loadclean_df["IsBequestInt"] = loadclean_df["IsBequest"].astype("category").cat.codes
    loadclean_df["IsAggregationInt"] = loadclean_df["IsAggregation"].astype("category").cat.codes
    loadclean_df["IsSponsorshipInt"] = loadclean_df["IsSponsorship"].astype("category").cat.codes
    loadclean_df["NatureOfDonationInt"] = loadclean_df["NatureOfDonation"].astype("category").cat.codes
    loadclean_df["RegisterNameInt"] = loadclean_df["RegisterName"].astype("category").cat.codes

    # Column encoding PublicFundsInt
    loadclean_df["PublicFundsInt"] = loadclean_df["DonationType"].apply(lambda x: 0 if x != "Public Funds" else 1)
    # Calculate the number of days to the next election and since the last election
    loadclean_df["DaysTillNextElection"] = loadclean_df["ReceivedDate"].apply(
        lambda x: GenElectionRelation2(x.strftime('%Y/%m/%d %H:%M:%S'), direction="DaysTill")
    )
    loadclean_df["DaysSinceLastElection"] = loadclean_df["ReceivedDate"].apply(
        lambda x: GenElectionRelation2(x.strftime('%Y/%m/%d %H:%M:%S'), direction="DaysSince")
    )

    # Calculate weeks and quarters till the next election and since the last election
    for period, divisor in [("Weeks", 7), ("Quarters", 91)]:
        loadclean_df[f'{period}TillNextElection'] = loadclean_df["ReceivedDate"].apply(
            lambda x: GenElectionRelation2(x.strftime('%Y/%m/%d %H:%M:%S'), divisor=divisor, direction="DaysTill")
        )
        loadclean_df[f'{period}SinceLastElection'] = loadclean_df["ReceivedDate"].apply(
            lambda x: GenElectionRelation2(x.strftime('%Y/%m/%d %H:%M:%S'), divisor=divisor, direction="DaysSince")
        )
    # Save cleaned data
    if output_csv:
        output_dir = st.session_state.directories["output_dir"]
        cleaned_data_filename = st.session_state.cleaned_data_fname
        cleaned_data_filename = os.path.join(output_dir, cleaned_data_filename)
        # Save the cleaned data to a CSV file for further analysis or reporting
        loadclean_df.to_csv(cleaned_data_filename)
    logger.info(f"Cleaned Data completed, shape: {loadclean_df.shape}")

    # apply political party mappings to MPs
    if st.session_state.RERUN_MP_PARTY_MEMBERSHIP:
        MP_Party = mp.map_mps_to_party_membership(loadclean_df)
    return loadclean_df
