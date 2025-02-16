import pandas as pd
import datetime as dt
import streamlit as st


def load_data():
    import pandas as pd
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
    df.to_csv('original_donations.csv')
    return df


# create summary data
def load_party_summary_data():
    df = st.session_state.get("data", None)
    # Create a DataFrame with the sum, count and mean of the donations for each RegulatedEntityName
    RegulatedEntity_df = df.groupby('RegulatedEntityName').agg({'Value': ['sum', 'count', 'mean']})
    # Rename columns
    RegulatedEntity_df.columns = ['DonationsValue', 'DonationEvents', 'DonationMean']
    # generate CSV file of summary data
    RegulatedEntity_df.to_csv('party_summary.csv')
    return df


# create cleaned data
def load_cleaned_data():
    orig_df = st.session_state.get("data", None)
    df = orig_df.copy()
    # # Fill blank ReceivedDate with ReportedDate
    df['ReceivedDate'] = df['ReceivedDate'].fillna(df['ReportedDate'])
    # # Fill blank ReceivedDate with AcceptedDate
    df['ReceivedDate'] = df['ReceivedDate'].fillna(df['AcceptedDate'])
    # # Convert 'ReportingPeriodName' to datetime if it contains dates at the e
    df['ReportingPeriodName_Date'] = pd.to_datetime(
         df['ReportingPeriodName'].str.strip().str[-10:],
         dayfirst=True,
         format='mixed',
         errors='coerce'
    ).dt.normalize()
    # # convert Received date to Date Format
    df['ReceivedDate'] = pd.to_datetime(df['ReceivedDate'],
                                        errors='coerce').dt.normalize()
    # # Fill missing 'ReceivedDate' with dates from 'ReportingPeriodName'
    df['ReceivedDate'] = df['ReceivedDate'].fillna(
        df['ReportingPeriodName_Date'])
    # # Fill errors in ReceivedDate with 01/01/1900 00:00:00
    df['ReceivedDate'] = df['ReceivedDate'].fillna(dt.datetime(1900, 1, 1))
    # # Append YearReceived column
    df['YearReceived'] = round(df['ReceivedDate'].dt.year)
    # # Append MonthReceived column
    df['MonthReceived'] = round(df['ReceivedDate'].dt.month)
    # # Create YearMonthReceived Column
    df['YearMonthReceived'] = round(df['YearReceived']*100 +
                                    df['MonthReceived'])
    # Replace Nulls in NatureOfDonation
    # Fill missing 'NatureOfDonation' with dates from 'ReportingPeriodName'
    # if IsBequest is true then set Blank Nature of Donations to Is A Bequest
    df['NatureOfDonation'] = df['NatureOfDonation'].fillna(df['IsBequest'].
                                                           apply(lambda x: 'Is A Bequest' if x else None))
    # # if isAggregation is true then set Blank Nature of Donations to Aggregated Donation
    df['NatureOfDonation'] = df['NatureOfDonation'].fillna(df['IsAggregation'].
                                                           apply(lambda x: 'Aggregated Donation' if x else None))
    # # if IsSponsorship true the set Blank Nature of Donations to SponsorShip
    df['NatureOfDonation'] = df['NatureOfDonation'].fillna(df['IsSponsorship'].
                                                           apply(lambda x: 'Sponsorship' if x else None))
    # # Update NatureOfDonation to donation to doneetype
    df['NatureOfDonation'] = df['NatureOfDonation'].fillna(df['RegulatedDoneeType'].
                                                           apply(lambda x: f'Donation to {x}' if x else None))
    # # Replace Donationm to nan in NatureOfDonation with Other
    df['NatureOfDonation'] = df['NatureOfDonation'].replace({'Donation to nan': 'Other',
                                                             'Other Payment': 'Other'}, regex=True)
    # # Add flag to mark 1 when received date - 01/01/1900 00:00:00
    df['DubiousData'] = df['ReceivedDate'].apply(lambda x: 1 if x == dt.datetime(1900, 1, 1) else 0)
    # # Add flag to mark 1 when RegulatedEntityId is null
    df['DubiousData'] = df['DubiousData'] + df['RegulatedEntityId'].apply(lambda x: 1 if pd.isnull(x) else 0)
    # # Add flag to mark 1 when DonorId is null
    df['DubiousData'] = df['DubiousData'] + df['DonorId'].apply(lambda x: 1 if pd.isnull(x) else 0)
    # # Add flag to mark 1 when DonationAction is not null
    df['DubiousData'] = df['DubiousData'] + df['DonationAction'].apply(lambda x: 1 if pd.notnull(x) else 0)
    # Apply the function to create a new column

    def RegulatedEntityGroup(RegulatedEntityNameVar):
        RegulatedEntity_df = st.session_state.get("data_party_sum", None)
        # Use the global dictionary g_thresholds
        RegEntityGrouping = st.session_state.g_thresholds
        # Select all relevant donation events for specified Entity Name
        RE_Events = RegulatedEntity_df[RegulatedEntity_df.index == RegulatedEntityNameVar]
        # Compare Count of events to rangelimits in Dictionary and return Category
        for rangeLimit, category in RegEntityGrouping.items():
            if RE_Events.DonationEvents.agg(sum) <= rangeLimit:
                return category
    # Apply the function to create a new column
    df['RegEntity_Group'] = df.RegulatedEntityName.apply(RegulatedEntityGroup)
    # generate CSV file of cleaned data
    df.to_csv('cleaned_donations.csv')
    return df
