import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv('Donations_accepted_by_political_parties.csv', dtype={
        'index': 'int64',
        'ECRef' : 'object',
        'RegulatedEntityName': 'object',
        'RegulatedEntityType': 'object',
        'Value': 'string',
        "AcceptedDate": 'string',
        "AccountingUnitName": 'string',
        "DonorName": 'object',
        "AccountingUnitsAsCentralParty": 'bool',
        'IsSponsorship': 'bool',
        'DonorStatus': 'object',
        'RegulatedDoneeType': 'object',
        'CompanyRegistrationNumber': 'string',
        'Postcode': 'string',
        'DonationType': 'object',
        'NatureOfDonation': 'object',
        'PurposeOfVisit': 'string',
        'DonationAction': 'string',
        'ReceivedDate': 'string',
        'ReportedDate': 'string',
        'IsReportedPrePoll': 'string',
        'ReportingPeriodName': 'string',
        'IsBequest': 'bool',
        'IsAggregation': 'bool',
        'RegulatedEntityId': 'object',
        'AccountingUnitId': 'string',
        'DonorId': 'object',
        'CampaigningName': 'string',
        'RegisterName': 'string',
        'IsIrishSource': 'string'
        },index_col="index")  # Load the data
    return df