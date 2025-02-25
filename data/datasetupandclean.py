import pandas as pd
import streamlit as st
import os
from data.data_dedupe import dedupe_entity_file


def load_raw_data(output_csv=False,
                  dedupe_donors=False,
                  dedupe_regentity=False):
    # Load the data
    base_dir = st.session_state.base_dir
    output_dir = st.session_state.directories["output_dir"]

    originaldatafilename = st.session_state.filenames["ec_donations_fname"]
    originaldatafilepath = os.path.join(base_dir,
                                        originaldatafilename)

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

    # Remove Currency sign of Value and convert to Float
    loaddata_df['Value'] = (
        loaddata_df['Value'].replace({'£': '', ',': ''},
                                     regex=True).astype(float)
    )
    # Fill missing text fields with empty strings
    columns_to_fill = [
        "PurposeOfVisit", "DonorName", "CampaigningName", "AccountingUnitName",
        "ReportingPeriodName", "RegulatedEntityName", "DonationAction",
        "DonationType", "NatureOfDonation", "IsBequest", "IsAggregation",
        "IsSponsorship", "RegulatedDoneeType", "DonorStatus",
        "CompanyRegistrationNumber", "Postcode", "RegisterName",
        "IsIrishSource", "DonorId", "RegulatedEntityId", "AccountingUnitId",
        "ECRef"
    ]
    loaddata_df[columns_to_fill] = (
        loaddata_df[columns_to_fill].fillna("").astype(str)
    )
    # remove leading and trailing spaces from DonorName, RegulatedEntityName
    # remove leading and trailing spaces from DonorID and RegulatedEntityID
    # remove leading and trailing spaces from CampaignName and PurposeOfVisit
    # remove leading and trailing spaces from AccountingUnitName and
    # ReportingPeriodName
    columns_to_strip = [
        'DonorName',
        'RegulatedEntityName',
        'DonorId',
        'RegulatedEntityId',
        'CampaigningName',
        'PurposeOfVisit',
        'AccountingUnitName',
        'ReportingPeriodName'
    ]
    loaddata_df[columns_to_strip] = (
        loaddata_df[columns_to_strip].apply(lambda x: x.str.strip())
    )
    # remove line returns and commas from DonorName, RegulatedEntityName,
    # CampaignName,
    # AccountingUnitName, ReportingPeriodName and PurposeOfVisit
    columns_to_clean = [
        'DonorName',
        'RegulatedEntityName',
        'PurposeOfVisit',
        'CampaigningName',
        'AccountingUnitName',
        'ReportingPeriodName'
    ]
    loaddata_df[columns_to_clean] = (
        loaddata_df[columns_to_clean].replace({',': '', '\n': ' '}, regex=True)
        )

    # standardise capitalisation of DonorName, RegulatedEntityName,
    # CampaignName,
    # AccountingUnitName, ReportingPeriodName and PurposeOfVisit
    columns_to_title = [
        'DonorName',
        'RegulatedEntityName',
        'PurposeOfVisit',
        'CampaigningName',
        'AccountingUnitName',
        'ReportingPeriodName'
    ]
    loaddata_df[columns_to_title] = (
        loaddata_df[columns_to_title].apply(lambda x: x.str.title())
    )
    # rename "Total value of donations not reported individually"
    # to "Aggregated Donation" in DonationType
    loaddata_df['DonationType'] = (
        loaddata_df['DonationType'].replace(
            {"Total value of donations not reported individually":
                "Aggregated Donation",
             "Permissible Donor Exempt Trust": "P.D. Exempt Trust"}
            )
        )
    # update Blank DonorName to "Anonymous Donor"
    loaddata_df['DonorName'] = (
        loaddata_df['DonorName'].replace("", "Unidentified Donor")
    )
    # update Blank DonorId to "1000001"
    loaddata_df['DonorId'] = (
        loaddata_df['DonorId'].replace("", "1000001")
    )
    # make donorid and regulatedentityid numeric
    loaddata_df['DonorId'] = (
        pd.to_numeric(loaddata_df['DonorId'], errors='coerce')
    )
    loaddata_df['RegulatedEntityId'] = (
        pd.to_numeric(loaddata_df['RegulatedEntityId'], errors='coerce')
    )
    # update Blank RegulatedEntityName to "Unidentified Entity"
    loaddata_df['RegulatedEntityName'] = (
        loaddata_df['RegulatedEntityName'].replace("", "Unidentified Entity")
        )
    # update Blank RegulatedEntityId to "1000001"
    loaddata_df['RegulatedEntityId'] = (
        loaddata_df['RegulatedEntityId'].replace("", "1000001")
    )
    # update Blank RegisterName to "Other"
    loaddata_df['RegisterName'] = (
        loaddata_df['RegisterName'].replace("", "Other")
    )
    # update Blank DonationAction to "Accepted"
    loaddata_df['DonationAction'] = (
        loaddata_df['DonationAction'].replace("", "Accepted")
    )
    # update DonorStatus to Unidentified Donor if blank
    loaddata_df['DonorStatus'] = (
        loaddata_df['DonorStatus'].replace("", "Unidentified Donor")
    )
    if dedupe_regentity:
        loaddata_df = dedupe_entity_file(loaddata_df,
                                         "RegulatedEntity",
                                         "regentity_map_fname",
                                         output_csv=True)
    else:
        st.write("Deduping of Regulated Entities not selected")

    if dedupe_donors:
        loaddata_df = dedupe_entity_file(loaddata_df,
                                         "Donor",
                                         "donor_map_fname",
                                         output_csv=True)
    else:
        st.write("Deduping of Donors Entities not selected")

    # Remove Northern Ireland register data
    loaddata_df = (
         loaddata_df[loaddata_df["RegisterName"] != "Northern Ireland"])
    # Remove Public Funds
    loaddata_df = (
        loaddata_df[loaddata_df["DonationType"] != "Public Funds"])

    # generate CSV file of original data
    if output_csv:
        cleaned_donations = (
            st.session_state.filenames["cleaned_donations_fname"]
        )
        cleaned_donations = os.path.join(output_dir,
                                         cleaned_donations)
        loaddata_df.to_csv(cleaned_donations)
    return loaddata_df
