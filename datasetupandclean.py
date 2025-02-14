import pandas as pd


def load_data():
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
    # # Fill blank ReceivedDate with ReportedDate
    df['ReceivedDate'] = df['ReceivedDate'].fillna(df['ReportedDate'])
    # # Fill blank ReceivedDate with AcceptedDate
    df['ReceivedDate'] = df['ReceivedDate'].fillna(df['AcceptedDate'])
    # # convert Received date to Date Format
    df['ReceivedDate'] = pd.to_datetime(df['ReceivedDate'],
                                        format='%d/%m/%Y', errors='coerce')
    # # Convert 'ReportingPeriodName' to datetime if it contains dates at the e
    df['ReportingPeriodName_Date'] = pd.to_datetime(
         df['ReportingPeriodName'].str.strip().str[-10:],
         dayfirst=True,
         format='mixed',
         errors='coerce'
    )
    # # Fill missing 'ReceivedDate' with dates from 'ReportingPeriodName'
    df['ReceivedDate'] = df['ReceivedDate'].fillna(
        df['ReportingPeriodName_Date'])
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
    return df
