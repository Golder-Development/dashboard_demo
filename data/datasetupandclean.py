import pandas as pd
import streamlit as st
from data.raw_data_clean import raw_data_cleanup
from components.global_variables import initialize_session_state

def load_raw_data(output_csv=False,
                  dedupe_donors=False,
                  dedupe_regentity=False):
    # Load the data
    if ('BASE_DIR' not in st.session_state
            or 'directories' not in st.session_state
            or 'filenames' not in st.session_state
            or "ec_donations_fname" not in st.session_state):
        initialize_session_state()

    originaldatafilepath = st.session_state["ec_donations_fname"]
    loaddata_df = pd.read_csv(originaldatafilepath, dtype={
        'index': 'int64',
        'ECRef': 'object',
        'RegulatedEntityName': 'object',
        'RegulatedEntityType': 'object',
        'Value': 'object',
        "AcceptedDate": 'object',
        "AccountingUnitName": 'object',
        "DonorName": 'object',
        "AccountingUnitsAsCentralParty": 'object',
        'IsSponsorship': 'object',
        'DonorStatus': 'object',
        'RegulatedDoneeType': 'object',
        'CompanyRegistrationNumber': 'object',
        'Postcode': 'object',
        'DonationType': 'object',
        'NatureOfDonation': 'object',
        'PurposeOfVisit': 'object',
        'DonationAction': 'object',
        'ReceivedDate': 'object',
        'ReportedDate': 'object',
        'IsReportedPrePoll': 'object',
        'ReportingPeriodName': 'object',
        'IsBequest': 'object',
        'IsAggregation': 'object',
        'RegulatedEntityId': 'object',
        'AccountingUnitId': 'object',
        'DonorId': 'object',
        'CampaigningName': 'object',
        'RegisterName': 'object',
        'IsIrishSource': 'object'
        }, index_col="index")  # Load the data

    # Print progress message
    st.write("Base Data loaded successfully")
    st.write(f"Data has {loaddata_df.shape[0]} rows "
             f"and {loaddata_df.shape[1]} columns")

    # cleanse the raw data
    loaddata_df = raw_data_cleanup(loaddata_df,
                                   dedupe_donors=dedupe_donors,
                                   dedupe_regentity=dedupe_regentity)

    # generate CSV file of original data
    if output_csv:
        cleaned_donations = (
            st.session_state.filenames["cleaned_donations_fname"]
        )
        loaddata_df.to_csv(cleaned_donations)
    return loaddata_df
