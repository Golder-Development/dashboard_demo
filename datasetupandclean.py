import pandas as pd
import datetime as dt
import streamlit as st


def load_data():
    # Load the data
    df = pd.read_csv('Donations_accepted_by_political_parties.csv', dtype={
        'index': 'int64',
        'ECRef': 'object',
        'RegulatedEntityName': 'object',
        'RegulatedEntityType': 'object',
        'Value': 'object',
        "AcceptedDate": 'object',
        "AccountingUnitName": 'category',
        "DonorName": 'object',
        "AccountingUnitsAsCentralParty": 'object',
        'IsSponsorship': 'object',
        'DonorStatus': 'object',
        'RegulatedDoneeType': 'object',
        'CompanyRegistrationNumber': 'category',
        'Postcode': 'category',
        'DonationType': 'object',
        'NatureOfDonation': 'object',
        'PurposeOfVisit': 'category',
        'DonationAction': 'category',
        'ReceivedDate': 'object',
        'ReportedDate': 'object',
        'IsReportedPrePoll': 'object',
        'ReportingPeriodName': 'category',
        'IsBequest': 'object',
        'IsAggregation': 'object',
        'RegulatedEntityId': 'object',
        'AccountingUnitId': 'category',
        'DonorId': 'object',
        'CampaigningName': 'category',
        'RegisterName': 'category',
        'IsIrishSource': 'object'
        }, index_col="index")  # Load the data
    # Remove Currency sign of Value and convert to Float
    df['Value'] = df['Value'].replace({'£': '', ',': ''},
                                      regex=True).astype(float)
    # generate CSV file of original data
    # df.to_csv('original_donations.csv')
    return df

def calculate_reg_entity_group(donation_events, entity_name):
    thresholds = {0: "No Relevant Donations", 1: "Single Donation Entity", 50: "Very Small Entity",
                  100: "Small Entity", 1000: "Medium Entity", float("inf"): entity_name}
    for limit, category in thresholds.items():
        if donation_events <= limit:
            return category

def load_party_summary_data():
    df = st.session_state.get("data", None)
    if df is None:
        st.error("No data found in session state!")
        return None
    # Create a DataFrame with the sum, count and mean of the donations for each RegulatedEntityName
    RegulatedEntity_df = df.groupby('RegulatedEntityName').agg({'Value': ['sum', 'count', 'mean']})
    # Rename columns
    RegulatedEntity_df.columns = ['DonationsValue', 'DonationEvents', 'DonationMean']

    # Add RegEntity_Group column
    RegulatedEntity_df['RegEntity_Group'] = RegulatedEntity_df.apply(
        lambda row: calculate_reg_entity_group(row['DonationEvents'], row.name), axis=1
    )
    # generate CSV file of summary data
    # RegulatedEntity_df.to_csv('party_summary.csv')
    return RegulatedEntity_df

def load_cleaned_data():
    orig_df = st.session_state.get("data", None)
    if orig_df is None:
        st.error("No data found in session state!")
        return None

    df = orig_df.copy()

    # Ensure date columns exist and are properly formatted
    date_cols = ["ReceivedDate", "ReportedDate", "AcceptedDate"]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Fill missing ReceivedDate values in priority order
    df["ReceivedDate"] = df["ReceivedDate"].fillna(df["ReportedDate"])
    df["ReceivedDate"] = df["ReceivedDate"].fillna(df["AcceptedDate"])

    # Extract date from ReportingPeriodName
    if "ReportingPeriodName" in df.columns:
        df["ReportingPeriodName_Date"] = pd.to_datetime(
            df["ReportingPeriodName"].str.extract(r'(\d{2}/\d{2}/\d{4})', expand=False),
            dayfirst=True, errors="coerce"
        )

        # Fill missing ReceivedDate with extracted date
        df["ReceivedDate"] = df["ReceivedDate"].fillna(df["ReportingPeriodName_Date"])

    # Set any remaining missing dates to 1900-01-01
    df["ReceivedDate"] = df["ReceivedDate"].fillna(dt.datetime(1900, 1, 1))

    # Create Year and Month columns
    df["YearReceived"] = df["ReceivedDate"].dt.year
    df["MonthReceived"] = df["ReceivedDate"].dt.month
    df["YearMonthReceived"] = df["YearReceived"] * 100 + df["MonthReceived"]

    # Handle NatureOfDonation based on other fields
    if "NatureOfDonation" in df.columns:
        df["NatureOfDonation"] = df["NatureOfDonation"].fillna(
            df["IsBequest"].map(lambda x: "Is A Bequest" if str(x).lower() == "true" else None)
        )
        df["NatureOfDonation"] = df["NatureOfDonation"].fillna(
            df["IsAggregation"].map(lambda x: "Aggregated Donation" if str(x).lower() == "true" else None)
        )
        df["NatureOfDonation"] = df["NatureOfDonation"].fillna(
            df["IsSponsorship"].map(lambda x: "Sponsorship" if str(x).lower() == "true" else None)
        )
        df["NatureOfDonation"] = df["NatureOfDonation"].fillna(
            df["RegulatedDoneeType"].map(lambda x: f"Donation to {x}" if pd.notna(x) else None)
        )
        df["NatureOfDonation"] = df["NatureOfDonation"].replace(
            {"Donation to nan": "Other", "Other Payment": "Other"}
        )

    # Create a DubiousData flag for problematic records
    df["DubiousData"] = (
        (df["ReceivedDate"] == dt.datetime(1900, 1, 1)).astype(int) +
        df["RegulatedEntityId"].isna().astype(int) +
        df["DonorId"].isna().astype(int) +
        df["DonationAction"].notna().astype(int)
    )

    # Load party summary data to get RegEntity_Group
    RegulatedEntity_df = st.session_state.get("data_party_sum", None)
    if RegulatedEntity_df is None:
        RegulatedEntity_df = load_party_summary_data()
        st.session_state["data_party_sum"] = RegulatedEntity_df

    reg_entity_dict = RegulatedEntity_df["RegEntity_Group"].to_dict()

    # Apply dictionary to populate RegEntity_Group
    if "RegulatedEntityName" in df.columns:
        df["RegEntity_Group"] = df["RegulatedEntityName"].map(reg_entity_dict).fillna("Unknown")

    # Ensure all columns that are in data are also in data_clean
    for col in orig_df.columns:
        if col not in df.columns:
            df[col] = orig_df[col]

    # Save cleaned data
    # df.to_csv("cleaned_donations.csv", index=False)
    return df
