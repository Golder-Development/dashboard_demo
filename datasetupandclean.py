import pandas as pd
import datetime as dt
import streamlit as st
from rapidfuzz import process, fuzz
from collections import defaultdict


def load_data(output_csv=False):
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
    # Fill missing text fields with empty strings
    df["PurposeOfVisit"] = df["PurposeOfVisit"].fillna("").astype(str)
    df["DonorName"] = df["Donor Name"].fillna("").astype(str)
    df["CampaigningName"] = df["CampaigningName"].fillna("").astype(str)
    df["AccountingUnitName"] = df["AccountingUnitName"].fillna("").astype(str)
    df["ReportingPeriodName"] = (
        df["ReportingPeriodName"].fillna("").astype(str)
        )
    df["RegulatedEntityName"] = (
        df["RegulatedEntityName"].fillna("").astype(str)
        )
    df["DonationAction"] = df["DonationAction"].fillna("").astype(str)
    df["DonationType"] = df["DonationType"].fillna("").astype(str)
    df["NatureOfDonation"] = df["NatureOfDonation"].fillna("").astype(str)
    df["IsBequest"] = df["IsBequest"].fillna("").astype(str)
    df["IsAggregation"] = df["IsAggregation"].fillna("").astype(str)
    df["IsSponsorship"] = df["IsSponsorship"].fillna("").astype(str)
    df["RegulatedDoneeType"] = df["RegulatedDoneeType"].fillna("").astype(str)
    df["DonorStatus"] = df["DonorStatus"].fillna("").astype(str)
    df["CompanyRegistrationNumber"] = (
        df["CompanyRegistrationNumber"].fillna("").astype(str)
        )
    df["Postcode"] = df["Postcode"].fillna("").astype(str)
    df["RegisterName"] = df["RegisterName"].fillna("").astype(str)
    df["IsIrishSource"] = df["IsIrishSource"].fillna("").astype(str)
    df["DonorId"] = df["DonorId"].fillna("").astype(str)
    df["RegulatedEntityId"] = df["RegulatedEntityId"].fillna("").astype(str)
    df["AccountingUnitId"] = df["AccountingUnitId"].fillna("").astype(str)
    df["ECRef"] = df["ECRef"].fillna("").astype(str)

    # remove leading and trailing spaces from DonorName, RegulatedEntityName
    # remove leading and trailing spaces from DonorID and RegulatedEntityID
    # remove leading and trailing spaces from CampaignName and PurposeOfVisit
    # remove leading and trailing spaces from AccountingUnitName and
    # ReportingPeriodName
    df['DonorName'] = df['DonorName'].str.strip()
    df['RegulatedEntityName'] = df['RegulatedEntityName'].str.strip()
    df['DonorId'] = df['DonorId'].str.strip()
    df['RegulatedEntityId'] = df['RegulatedEntityId'].str.strip()
    df['CampaigningName'] = df['CampaigningName'].str.strip()
    df['PurposeOfVisit'] = df['PurposeOfVisit'].str.strip()
    df['AccountingUnitName'] = df['AccountingUnitName'].str.strip()
    df['ReportingPeriodName'] = df['ReportingPeriodName'].str.strip()

    # remove line returns and commas from DonorName, RegulatedEntityName,
    # CampaignName,
    # AccountingUnitName, ReportingPeriodName and PurposeOfVisit
    df['DonorName'] = df['DonorName'].replace({',': '', '\n': ' '}, regex=True)
    df['RegulatedEntityName'] = (
        df['RegulatedEntityName'].replace({',': '', '\n': ' '}, regex=True)
    )
    df['PurposeOfVisit'] = (
        df['PurposeOfVisit'].replace({',': '', '\n': ' '}, regex=True)
    )
    df['CampaigningName'] = (
        df['CampaigningName'].replace({',': '', '\n': ' '}, regex=True)
    )
    df['AccountingUnitName'] = (
        df['AccountingUnitName'].replace({',': '', '\n': ' '}, regex=True)
    )
    df['ReportingPeriodName'] = (
        df['ReportingPeriodName'].replace({',': '', '\n': ' '}, regex=True)
    )

    # standardise capitalisation of DonorName, RegulatedEntityName,
    # CampaignName,
    # AccountingUnitName, ReportingPeriodName and PurposeOfVisit
    df['DonorName'] = df['DonorName'].str.title()
    df['RegulatedEntityName'] = df['RegulatedEntityName'].str.title()
    df['PurposeOfVisit'] = df['PurposeOfVisit'].str.title()
    df['CampaigningName'] = df['CampaigningName'].str.title()
    df['AccountingUnitName'] = df['AccountingUnitName'].str.title()
    df['ReportingPeriodName'] = df['ReportingPeriodName'].str.title()

    # rename "Total value of donations not reported individually"
    # to "Aggregated Donation" in DonationType
    df['DonationType'] = df['DonationType'].replace(
        {"Total value of donations not reported individually": "Aggregated Donation",
         "Permissible Donor Exempt Trust": "P.D. Exempt Trust"}
    )
    # make donorid and regulatedentityid numeric
    df['DonorId'] = pd.to_numeric(df['DonorId'], errors='coerce')
    df['RegulatedEntityId'] = pd.to_numeric(df['RegulatedEntityId'],
                                            errors='coerce')

    # update Blank DonorName to "Anonymous Donor"
    df['DonorName'] = df['DonorName'].replace("", "Anonymous Donor")
    # update Blank DonorId to "1000001"
    df['DonorId'] = df['DonorId'].replace("", "1000001")
    # update Blank RegulatedEntityName to "Anonymous Entity"
    df['RegulatedEntityName'] = (
        df['RegulatedEntityName'].replace("", "Anonymous Entity")
        )
    # update Blank RegulatedEntityId to "1000001"
    df['RegulatedEntityId'] = df['RegulatedEntityId'].replace("", "1000001")

    # Load the dataset
    # file_path = "cleaned_donations.csv"  # Adjust path as needed
    # df = pd.read_csv(file_path)

    # Extract donor names and IDs
    donor_names = df[['DonorId', 'DonorName']].drop_duplicates()

    # Preprocess donor names (lowercase and remove special characters)
    donor_names["Cleaned Name"] = (
        donor_names["DonorName"]
        .str.lower()
        .str.replace(r"[^a-z0-9\s]", "", regex=True)
        )

    # Create a mapping of donor names to IDs
    name_to_id = donor_names.set_index("Cleaned Name")["DonorId"].to_dict()

    # Dictionary to store potential duplicates
    potential_duplicates = defaultdict(set)
    threshold = 85  # Adjust similarity threshold as needed

    # Apply fuzzy matching
    for cleaned_name, donor_id in name_to_id.items():
        matches = process.extract(cleaned_name,
                                  name_to_id.keys(),
                                  scorer=fuzz.ratio,
                                  limit=5)
        for match_name, score, _ in matches:
            if score >= threshold and match_name != cleaned_name:
                match_id = name_to_id[match_name]
                potential_duplicates[donor_id].add(match_id)
                potential_duplicates[match_id].add(donor_id)

    # Convert sets to lists
    potential_duplicates = {k: list(v) for k,
                            v in potential_duplicates.items()}

    # Save results or display
    print(list(potential_duplicates.items())[:10])  # Show sample of results

    # Save results to a CSV file
    output_df = (
        pd.DataFrame(potential_duplicates.items(),
                     columns=["DonorId",
                              "Potential Duplicates"])
        )
    output_df.to_csv("potential_duplicates.csv", index=False)

    # using potential_duplicates to merge the data
    # potential_duplicates = pd.read_csv("potential_duplicates.csv")

    # Create mappings for cleansed ID and Name
    id_to_cleansed = {}
    name_to_cleansed = {}

    for main_id, duplicate_ids in potential_duplicates.items():
        all_ids = [main_id] + duplicate_ids
        cleansed_id = min(all_ids)  # Choose the smallest DonorId

        # Get all names corresponding to these IDs
        matching_names = df[df["DonorId"].isin(all_ids)]["DonorName"]

        # Choose the most frequent name
        cleansed_name = matching_names.value_counts().idxmax()

        # Store mappings
        for donor_id in all_ids:
            id_to_cleansed[donor_id] = cleansed_id
            name_to_cleansed[donor_id] = cleansed_name

    # Apply mappings to the dataset
    df["Cleansed Donor ID"] = (
        df["DonorId"].map(id_to_cleansed).fillna(df["DonorId"])
        )
    df["Cleansed Donor Name"] = (
        df["DonorId"].map(name_to_cleansed).fillna(df["DonorName"])
        )
    # rename DonorId to Original DonorId and DonorName to Original DonorName
    df.rename(columns={"DonorId": "Original DonorId",
                       "DonorName": "Original DonorName"}, inplace=True)
    # rema,e Cleansed Donor ID to DonorId and Cleansed Donor Name to DonorName
    df.rename(columns={"Cleansed Donor ID": "DonorId",
                       "Cleansed Donor Name": "DonorName"}, inplace=True)

    # Remove Northern Ireland register data
    # df = df[df["RegisterName"] != "Northern Ireland"]
    # Remove Public Funds
    # df = df[df["DonationType"] != "Public Funds"]

    # generate CSV file of original data
    if output_csv:
        df.to_csv('original_donations.csv')

    return df


def create_thresholds():
    if 'g_thresholds' not in st.session_state:
        st.session_state.g_thresholds = {
            0: "No Relevant Donations",
            1: "Single Donation Entity",
            50: "Very Small Entity",
            100: "Small Entity",
            1000: "Medium Entity",
            float('inf'): "Large Entity"
        }


def calculate_reg_entity_group(donation_events, entity_name):
    if 'g_thresholds' not in st.session_state:
        create_thresholds()
    # Copy g_thresholds and add the new entity_name to the thresholds
    # dictionary
    # Make a copy to avoid modifying the global dictionary
    thresholds = st.session_state.g_thresholds.copy()
    # Add the new threshold with entity_name
    thresholds[float("inf")] = entity_name
    # Loop through the thresholds to find the corresponding category
    for limit, category in thresholds.items():
        if donation_events <= limit:
            return category


def load_party_summary_data(output_csv=False):
    df = st.session_state.get("data", None)
    if df is None:
        st.error("No data found in session state!")
        return None
    # Create a DataFrame with the sum, count and mean of the donations
    # for each RegulatedEntityName
    RegulatedEntity_df = (
        df.groupby(['RegulatedEntityName'])
        .agg({'Value': ['sum', 'count', 'mean']}).reset_index()
    )
    # Rename columns
    RegulatedEntity_df.columns = ['RegulatedEntityName',
                                  'DonationsValue',
                                  'DonationEvents',
                                  'DonationMean']

    # Add RegEntity_Group column
    RegulatedEntity_df['RegEntity_Group'] = (
        RegulatedEntity_df.apply(
            lambda row: calculate_reg_entity_group(row['DonationEvents'],
                                                   row['RegulatedEntityName']),
            axis=1
                                ))
    # generate CSV file of summary data
    if output_csv:
        RegulatedEntity_df.to_csv('party_summary.csv')

    return RegulatedEntity_df


def load_cleaned_data(output_csv=False):
    orig_df = st.session_state.get("data", None)
    if orig_df is None:
        st.error("No data found in session state!")
        return None

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
                                        dayfirst=True,
                                        format='mixed',
                                        errors='coerce').dt.normalize()
    # # Fill missing 'ReceivedDate' with dates from 'ReportingPeriodName'
    df['ReceivedDate'] = df['ReceivedDate'].fillna(
        df['ReportingPeriodName_Date'])
    # Set any remaining missing dates to 1900-01-01
    # df["ReceivedDate"] = df["ReceivedDate"].fillna(dt.datetime(1900, 1, 1))
    # Create Year and Month columns
    df["YearReceived"] = df["ReceivedDate"].dt.year
    df["MonthReceived"] = df["ReceivedDate"].dt.month
    df["YearMonthReceived"] = df["YearReceived"] * 100 + df["MonthReceived"]

    # Handle NatureOfDonation based on other fields
    if "NatureOfDonation" in df.columns:
        df["NatureOfDonation"] = (
            df["NatureOfDonation"].fillna(
                df["IsBequest"].map(lambda x: "Is A Bequest"
                                    if str(x).lower() == "true" else None)
                                   ))
        df["NatureOfDonation"] = (
            df["NatureOfDonation"].fillna(
                df["IsAggregation"].map(lambda x: "Aggregated Donation"
                                        if str(x).lower() == "true" else None)
                                    ))
        df["NatureOfDonation"] = (
            df["NatureOfDonation"].fillna(
                df["IsSponsorship"].map(lambda x: "Sponsorship"
                                        if str(x).lower() == "true" else None)
            ))
        df["NatureOfDonation"] = (
            df["NatureOfDonation"].fillna(
                df["RegulatedDoneeType"].map(lambda x: f"Donation to {x}"
                                             if pd.notna(x) else None)
            ))
        df["NatureOfDonation"] = df["NatureOfDonation"].replace(
            {"Donation to nan": "Other", "Other Payment": "Other"}
        )
        df["NatureOfDonation"] = df["NatureOfDonation"].fillna(
            df["DonationAction"].map(lambda x: f"{x}" if pd.notna(x) else None)
        )
        df["NatureOfDonation"] = df["NatureOfDonation"].fillna(
            df["DonationType"].map(lambda x: f"{x}" if pd.notna(x) else None)
        )

    # Create a DubiousData flag for problematic records
    df["DubiousData"] = (
        (df["DonationType"] == "Impermissible Donor").astype(int) +
        (df["DonationType"] == "Unidentified Donor").astype(int) +
        (df["DonationType"] == "Aggregated Donation").astype(int) +
        (df['IsAggregation'] == "True").astype(int) +
        (df["DonationType"] == "Visit").astype(int) +
        (df['NatureOfDonation'] == "Other").astype(int) +
        (df["DonationAction"].notnull()).astype(int) +
        (df["ReceivedDate"] == dt.datetime(1900, 1, 1)).astype(int) +
        df["RegulatedEntityId"].isna().astype(int) +
        df["DonorId"].isna().astype(int) +
        (df["DonorName"].isnull()).astype(int)
        )

    # Create simple column to enable count of events using sum
    df["EventCount"] = 1

    # Load party summary data to get RegEntity_Group
    RegulatedEntity_df = st.session_state.get("data_party_sum", None)
    if RegulatedEntity_df is None:
        RegulatedEntity_df = load_party_summary_data()
        st.session_state["data_party_sum"] = RegulatedEntity_df

    # Create a dictionary to map RegulatedEntityName to RegEntity_Group
    reg_entity_dict = (
        RegulatedEntity_df
        .set_index("RegulatedEntityName")[["RegEntity_Group"]]
        .to_dict(orient="index")
        )

    # Apply dictionary to populate RegEntity_Group
    if "RegulatedEntityName" in df.columns:
        df["RegEntity_Group"] = (
            df["RegulatedEntityName"]
            .map(lambda x: reg_entity_dict.get(x, {})
                 .get("RegEntity_Group", "Unknown"))
        )
    # Ensure all columns that are in data are also in data_clean
    for col in orig_df.columns:
        if col not in df.columns:
            df[col] = orig_df[col]

    # Drop Columns that are not needed
    df = df.drop(['ReportingPeriodName_Date',
                  'IsIrishSource',
                  'AccountingUnitsAsCentralParty',
                  'AccountingUnitName',
                  'AcceptedDate',
                  'ReportedDate',
                  'IsReportedPrePoll',
                  'AccountingUnitId',
                  'Postcode',
                  'CompanyRegistrationNumber',
                  'CampaigningName'
                  ],
                 axis=1)

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
        df.to_csv('cleaned_donations.csv')

    return df


def load_donorList_data(output_csv=False):
    orig_df = st.session_state.get("data_clean", None)
    if orig_df is None:
        st.error("No data found in session state!")
        return None
    else:
        orig_df = (
            orig_df.groupby(['DonorId',
                             'DonorName'])
                   .agg({'Value': ['sum',
                                   'count',
                                   'mean']}).reset_index()
        )
        orig_df.columns = ['DonorId',
                           'Donor Name',
                           'Donations Value',
                           'Donation Events',
                           'Donation Mean']
        if output_csv:
            orig_df.to_csv('cleaned_donations.csv')
        return orig_df


def load_regulated_entity_data(output_csv=False):
    orig_df = st.session_state.get("data_clean", None)
    if orig_df is None:
        st.error("No data found in session state!")
        return None
    else:
        orig_df = (
            orig_df.groupby(['RegulatedEntityId',
                             'RegulatedEntityName',
                             'RegEntity_Group'])
                   .agg({'Value': ['sum',
                                   'count',
                                   'mean']}).reset_index()
        )
        orig_df.columns = ['RegulatedEntityId',
                           'Regulated Entity Name',
                           'Regulated Entity Group',
                           'Donations Value',
                           'Donation Events',
                           'Donation Mean']
        if output_csv:
            orig_df.to_csv('cleaned_regentity.csv')
        return orig_df
