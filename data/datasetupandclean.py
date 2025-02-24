import pandas as pd
import streamlit as st
import os
from rapidfuzz import process, fuzz
from collections import defaultdict


def load_data(output_csv=False, dedupe_donors=False, dedupe_regentity=False):
    # Load the data
    base_dir = st.session_state.base_dir
    ref_dir = st.session_state.directories["reference_dir"]
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
    # update Blank RegulatedEntityId to "1000001"
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
        # check that reentity_deduped file exists using global variables
        if "regentity_map_fname" not in st.session_state.filenames:
            raise ValueError("regentity_map_fname not found"
                             " in session state filenames")
        # check that file exists at identified path from global var
        if os.path.exists(os.path.join(ref_dir,
                                       st.session_state
                                       .filenames["regentity_map_fname"])):
            # load regentity_map_fname file using global variables
            regentity_dedupedfilename = (
                st.session_state.filenames["regentity_map_fname"])
            regentity_dedupedfilepath = os.path.join(ref_dir,
                                                     regentity_dedupedfilename)
            re_dedupe_df = pd.read_csv(regentity_dedupedfilepath)
            # merge re_dedupe_df with original data
            loaddata_df = pd.merge(loaddata_df,
                                   re_dedupe_df,
                                   how='left',
                                   on='RegulatedEntityId')
            # rename RegulatedEntityName_x to RegulatedEntityName
            # and RegulatedEntityName_y to OriginalRegulatedEntityName
            loaddata_df.rename(
                columns={"RegulatedEntityName_x": "RegulatedEntityName",
                         "RegulatedEntityName_y": "OriginalRegulatedEntityName"
                         }, inplace=True)
            # use the RegulatedEntityId and RegulatedEntityName columns
            # to update the original data with new columns called
            # parententityid and parententityname - in no match exists
            # the original data will be used
            loaddata_df['ParentEntityId'] = (
                loaddata_df['CleanedRegulatedEntityId'].replace("", pd.NA)
            )
            loaddata_df['ParentEntityName'] = (
                loaddata_df['CleanedRegulatedEntityName'].replace("", pd.NA)
            )
            loaddata_df['ParentEntityId'] = (
                loaddata_df['ParentEntityId']
                .fillna(loaddata_df['RegulatedEntityId'])
            )
            loaddata_df['ParentEntityName'] = (
                loaddata_df['ParentEntityName']
                .fillna(loaddata_df['RegulatedEntityName'])
            )
            loaddata_df.rename(
                columns={"RegulatedEntityId": "OriginalRegEntityId",
                         "RegulatedEntityName": "OriginalRegEntityName",
                         "ParentEntityId": "RegulatedEntityId",
                         "ParentEntityName": "RegulatedEntityName"},
                inplace=True)
        else:
            # Run dedupe logic if PoliticalDonorsDeduped.csv file does not
            # exist

            # Extract donor names and IDs
            entity_names = (
                loaddata_df[['RegulatedEntityId',
                             'RegulatedEntityName']].drop_duplicates()
                )

            # Preprocess donor names (lowercase and remove special characters)
            entity_names["Cleaned Name"] = (
                entity_names["RegulatedEntityName"]
                .str.lower()
                .str.replace(r"[^a-z0-9\s]", "", regex=True)
                )

            # Create a mapping of donor names to IDs
            name_to_id = (
                entity_names.set_index("Cleaned Name")["RegulatedEntityId"]
                .to_dict()
            )

            # Dictionary to store potential duplicates
            potential_duplicates = defaultdict(set)
            threshold = 85  # Adjust similarity threshold as needed

            # Apply fuzzy matching
            for cleaned_name, RegulatedEntityId in name_to_id.items():
                matches = process.extract(cleaned_name,
                                          name_to_id.keys(),
                                          scorer=fuzz.ratio,
                                          limit=5)
                for match_name, score, _ in matches:
                    if score >= threshold and match_name != cleaned_name:
                        match_id = name_to_id[match_name]
                        potential_duplicates[RegulatedEntityId].add(match_id)
                        potential_duplicates[match_id].add(RegulatedEntityId)

            # Convert sets to lists
            potential_duplicates = {k: list(v) for k,
                                    v in potential_duplicates.items()}

            # Save results to a CSV file
            if output_csv:
                potential_regentity_duplicates_filemane = (
                    st.session_state
                    .filenames["potential_regentity_duplicates_fname"]
                )
                potential_regentity_duplicates_filemane = (
                    os.path.join(output_dir,
                                 potential_regentity_duplicates_filemane)
                )
                output_df = (
                    pd.DataFrame(potential_duplicates.items(),
                                 columns=["RegulatedEntityId",
                                          "Potential Duplicates"])
                    )

                output_df.to_csv(potential_regentity_duplicates_filemane,
                                 index=False)

            # Create mappings for cleansed ID and Name
            id_to_cleansed = {}
            name_to_cleansed = {}

            for main_id, duplicate_ids in potential_duplicates.items():
                all_ids = [main_id] + duplicate_ids
                # Choose the smallest RegulatedEntityId
                cleansed_id = min(all_ids)

                # Get all names corresponding to these IDs
                matching_names = (
                    loaddata_df[loaddata_df["RegulatedEntityId"]
                                .isin(all_ids)]["RegulatedEntityName"]
                )

                # Choose the most frequent name
                cleansed_name = matching_names.value_counts().idxmax()

                # Store mappings
                for RegulatedEntityId in all_ids:
                    id_to_cleansed[RegulatedEntityId] = cleansed_id
                    name_to_cleansed[RegulatedEntityId] = cleansed_name

            # convert Id = "" to null
            loaddata_df['RegulatedEntityId'] = (
                loaddata_df['RegulatedEntityId'].replace("", pd.NA)
            )
            # Apply mappings to the dataset
            loaddata_df["Cleansed RegulatedEntityID"] = (
                loaddata_df["RegulatedEntityId"]
                .map(id_to_cleansed)
                .fillna(loaddata_df["RegulatedEntityId"])
                )
            loaddata_df["Cleansed RegulatedEntityName"] = (
                loaddata_df["RegulatedEntityId"]
                .map(name_to_cleansed)
                .fillna(loaddata_df["RegulatedEntityName"])
                )

            # rename Cleansed ID to Id and Cleansed Name to Name
            loaddata_df.rename(
                columns={"Cleansed RegulatedEntityID": "ParentRegEntityId",
                         "Cleansed RegulatedEntityName":
                         "ParentRegEntityName"},
                inplace=True
                )
    # if ListOfPoliticalPeople_Final.csv file does not exist:
    #     # import ListOfPoliticalPeople_Final.csv file
    #     base_dir = st.session_state.base_dir
    #     politician_party_filename = st.session_state.filenames["politician_party_fname"]
    #     politician_party_filepath = os.path.join(base_dir, politician_party_filename)
    #     politician_party_df = pd.read_csv(politician_party_filepath)
    #     # merge ListOfPoliticalPeople_Final.csv file with original data
    #     loaddata_df = pd.merge(df, politician_party_df, how='left', on='RegulatedEntityID')
    #     # update blank PartyName to "Unidentified Party"
    #     loaddata_df['PartyName'] = loaddata_df['PartyName'].replace("", RegulatedEntityName)
    #     # update blank PartyId to "1000001"
    #     loaddata_df['PartyId'] = loaddata_df['PartyId'].replace("", RegulatedEntityId)
    #     # update blank PoliticianName to "Unidentified Politician"
    #     loaddata_df['PoliticianName'] = loaddata_df['PoliticianName'].replace("", "Unidentified Politician")
    #     # update blank PoliticianId to "1000001"
    #     loaddata_df['PoliticianId'] = loaddata_df['PoliticianId'].replace("", "1000001")

    if dedupe_donors:
        # check that politicaldonoprsdedupedfile exists using global variables
        if "donor_map_fname" not in st.session_state.filenames:
            raise ValueError("donor_map_fname not found in"
                             " session state filenames")
        # check that file exists at identified path from global var
        if os.path.exists(os.path.join(ref_dir,
                                       st.session_state
                                       .filenames["donor_map_fname"])):
            # load PoliticalDonorsDeduped.csv file using global variables
            politicaldonorsdedupedfilename = (
                st.session_state.filenames["donor_map_fname"]
            )
            politicaldonorsdedupedfilepath = (
                os.path.join(ref_dir, politicaldonorsdedupedfilename)
            )
            donors_df = pd.read_csv(politicaldonorsdedupedfilepath)
            # merge donors_df with original data
            loaddata_df = pd.merge(loaddata_df,
                                   donors_df,
                                   how='left',
                                   on='DonorId')
            # use the DonorId and DonorName columns to update the original
            # data with new columns called parentdonorid and parentdonorname
            # - in no match exists the original data will be used
            loaddata_df['ParentDonorId'] = (
                loaddata_df['ParentDonorId'].replace("", pd.NA)
            )
            loaddata_df['ParentDonorName'] = (
                loaddata_df['ParentDonorName'].replace("", pd.NA)
            )
            loaddata_df['ParentDonorId'] = (
                loaddata_df['ParentDonorId'].fillna(loaddata_df['DonorId'])
            )
            loaddata_df['ParentDonorName'] = (
                loaddata_df['ParentDonorName'].fillna(loaddata_df['DonorName'])
            )
            loaddata_df.rename(columns={"DonorId": "ChildDonorId",
                                        "DonorName": "ChildDonorName",
                                        "ParentDonorId": "DonorId",
                                        "ParentDonorName": "DonorName"},
                               inplace=True)
        else:
            # Run dedupe logic if PoliticalDonorsDeduped.csv file
            # does not exist  Extract donor names and IDs
            donor_names = (
                loaddata_df[['DonorId', 'DonorName']].drop_duplicates()
            )
            # Preprocess donor names (lowercase and remove special characters)
            donor_names["CleanedName"] = (
                donor_names["DonorName"]
                .str.lower()
                .str.replace(r"[^a-z0-9\s]", "", regex=True)
                )

            # Create a mapping of donor names to IDs
            name_to_id = (
                donor_names.set_index("CleanedName")["DonorId"].to_dict()
            )
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

            # Save results to a CSV file
            if output_csv:
                potential_donor_duplicates_filename = (
                    st.session_state
                    .filenames["potential_donor_duplicates_fname"]
                )
                potential_donor_duplicates_filename = (
                    os.path.join(output_dir,
                                 potential_donor_duplicates_filename)
                )
                output_df = (
                    pd.DataFrame(potential_duplicates.items(),
                                 columns=["DonorId",
                                          "Potential Duplicates"])
                    )
                output_df.to_csv(potential_donor_duplicates_filename,
                                 index=False)

            # Create mappings for cleansed ID and Name
            id_to_cleansed = {}
            name_to_cleansed = {}

            for main_id, duplicate_ids in potential_duplicates.items():
                all_ids = [main_id] + duplicate_ids
                cleansed_id = min(all_ids)  # Choose the smallest DonorId

                # Get all names corresponding to these IDs
                matching_names = (
                    loaddata_df[loaddata_df["DonorId"]
                                .isin(all_ids)]["DonorName"]
                )
                # Choose the most frequent name
                cleansed_name = matching_names.value_counts().idxmax()

                # Store mappings
                for donor_id in all_ids:
                    id_to_cleansed[donor_id] = cleansed_id
                    name_to_cleansed[donor_id] = cleansed_name

            # convert DonorId = "" to null
            loaddata_df['DonorId'] = loaddata_df['DonorId'].replace("", pd.NA)

            # Apply mappings to the dataset
            loaddata_df["CleansedDonorID"] = (
                loaddata_df["DonorId"]
                .map(id_to_cleansed)
                .fillna(loaddata_df["DonorId"])
                )
            loaddata_df["CleansedDonorName"] = (
                loaddata_df["DonorId"]
                .map(name_to_cleansed)
                .fillna(loaddata_df["DonorName"])
                )
            # rename DonorId to Original DonorId and DonorName
            # to Original DonorName
            loaddata_df.rename(columns={"DonorId": "OriginalDonorId",
                               "DonorName": "OriginalDonorName"},
                               inplace=True)
            # rename Cleansed Donor ID to DonorId and Cleansed Donor Name
            # to DonorName
            loaddata_df.rename(columns={"CleansedDonorID": "DonorId",
                               "CleansedDonorName": "DonorName"},
                               inplace=True)

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


def load_entity_summary_data(datafile=None,
                             streamlitrun=True,
                             output_csv=False):
    if streamlitrun:
        entitysummary_df = st.session_state.get("data", None)
        if entitysummary_df is None:
            st.error("No data found in session state!")
            return None
    else:
        if datafile is None:
            st.error("No data found in session state!")
        else:
            entitysummary_df = datafile
    # Create a DataFrame with the sum, count and mean of the donations
    # for each RegulatedEntityName
    RegulatedEntity_df = (
        entitysummary_df.groupby(['RegulatedEntityName'])
        .agg({'Value': ['sum', 'count', 'mean']}).reset_index()
    )
    # Rename columns
    RegulatedEntity_df.columns = ['RegulatedEntityName',
                                  'DonationsValue',
                                  'DonationEvents',
                                  'DonationMean']

    # Add RegEntity_Group column based on thresholds
    def determine_group(row):
        if row['DonationEvents'] > 2500:
            return row['RegulatedEntityName']
        else:
            return st.session_state.thresholds.get(row['DonationEvents'],
                                                   "Unknown")

    RegulatedEntity_df['RegEntity_Group'] = (
        RegulatedEntity_df.apply(determine_group, axis=1)
    )

    # generate CSV file of summary data
    if output_csv:
        output_dir = st.session_state.directories["output_dir"]
        party_filename = (
            st.session_state.filenames["party_summary_fname"]
        )
        party_filename = os.path.join(output_dir,
                                      party_filename)
        RegulatedEntity_df.to_csv(party_filename)

    return RegulatedEntity_df


def load_cleaned_data(datafile=None, streamlitrun=True, output_csv=False):
    if streamlitrun:
        orig_df = st.session_state.get("data", None)
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
    # convert DonorId = "" to null
    loadclean_df['DonorId'] = loadclean_df['DonorId'].replace("", pd.NA)
    # Fill missing text fields with empty strings
    columns_to_fill = [
                "ReceivedDate",
                "ReportingPeriodName",
                "NatureOfDonation",
                "DonationAction",
                "DonationType"
            ]
    loadclean_df[columns_to_fill] = (
        loadclean_df[columns_to_fill].replace("", pd.NA)
    )
    # # Fill blank ReceivedDate with ReportedDate
    loadclean_df['ReceivedDate'] = (
        loadclean_df['ReceivedDate'].fillna(loadclean_df['ReportedDate'])
    )
    # # Fill blank ReceivedDate with AcceptedDate
    loadclean_df['ReceivedDate'] = (
        loadclean_df['ReceivedDate'].fillna(loadclean_df['AcceptedDate'])
    )
    # # Convert 'ReportingPeriodName' to datetime if it contains dates at the e
    loadclean_df['ReportingPeriodName_Date'] = pd.to_datetime(
         loadclean_df['ReportingPeriodName'].str.strip().str[-10:],
         dayfirst=True,
         format='mixed',
         errors='coerce'
    ).dt.normalize()
    # # convert Received date to Date Format
    loadclean_df['ReceivedDate'] = (
        pd.to_datetime(loadclean_df['ReceivedDate'],
                       dayfirst=True,
                       format='mixed',
                       errors='coerce').dt.normalize()
    )
    # # Fill missing 'ReceivedDate' with dates from 'ReportingPeriodName'
    loadclean_df['ReceivedDate'] = (
        loadclean_df['ReceivedDate']
        .fillna(loadclean_df['ReportingPeriodName_Date'])
    )
    # Set any remaining missing dates to 1900-01-01
    filldate = st.session_state.PLACEHOLDER_DATE
    loadclean_df["ReceivedDate"] = (
        loadclean_df["ReceivedDate"].fillna(filldate))
    # Create Year and Month columns
    loadclean_df["YearReceived"] = loadclean_df["ReceivedDate"].dt.year
    loadclean_df["MonthReceived"] = loadclean_df["ReceivedDate"].dt.month
    loadclean_df["YearMonthReceived"] = (
        loadclean_df["YearReceived"] * 100 + loadclean_df["MonthReceived"]
    )
    # Handle NatureOfDonation based on other fields
    if "NatureOfDonation" in loadclean_df.columns:
        loadclean_df["NatureOfDonation"] = (
            loadclean_df["NatureOfDonation"].fillna(
                loadclean_df["IsBequest"]
                .map(lambda x: "Is A Bequest"
                     if str(x).lower() == "true" else None)
                                   ))
        loadclean_df["NatureOfDonation"] = (
            loadclean_df["NatureOfDonation"].fillna(
                loadclean_df["IsAggregation"]
                .map(lambda x: "Aggregated Donation"
                     if str(x).lower() == "true" else None)
                                    ))
        loadclean_df["NatureOfDonation"] = (
            loadclean_df["NatureOfDonation"].fillna(
                loadclean_df["IsSponsorship"]
                .map(lambda x: "Sponsorship"
                     if str(x).lower() == "true" else None)
            ))
        loadclean_df["NatureOfDonation"] = (
            loadclean_df["NatureOfDonation"].fillna(
                loadclean_df["RegulatedDoneeType"]
                .map(lambda x: f"Donation to {x}"
                     if pd.notna(x) else None)
            ))
        loadclean_df["NatureOfDonation"] = (
            loadclean_df["NatureOfDonation"].fillna(
                loadclean_df["RegulatedEntityType"]
                .map(lambda x: f"Donation to {x}"
                     if pd.notna(x) else None)
            ))
        loadclean_df["NatureOfDonation"] = (
            loadclean_df["NatureOfDonation"].replace(
                {"Donation to nan": "Other", "Other Payment": "Other"}
            ))
        loadclean_df["NatureOfDonation"] = (
            loadclean_df["NatureOfDonation"].fillna(
                loadclean_df["DonationAction"].map(lambda x: f"{x}"
                                                   if pd.notna(x) else None)
            ))
        loadclean_df["NatureOfDonation"] = (
            loadclean_df["NatureOfDonation"].fillna(
                loadclean_df["DonationType"].map(lambda x: f"{x}"
                                                 if pd.notna(x) else None)
            ))
        loadclean_df["NatureOfDonation"] = (
            loadclean_df["NatureOfDonation"].fillna(
                loadclean_df["DonationType"].map(lambda x: f"{x}"
                                                 if pd.notna(x) else None)
            ))
        loadclean_df['NatureOfDonation'] = (
            loadclean_df['NatureOfDonation'].replace("Donation to ", "Other"))

    # Create a DubiousData flag for problematic records
    if (("PLACEHOLDER_DATE" not in st.session_state) or
            ("PLACEHOLDER_ID" not in st.session_state)):
        raise ValueError("Session state variables PLACEHOLDER_DATE "
                         "and PLACEHOLDER_ID must be initialized before use.")

    if "dubious_donation_types" not in st.session_state:
        raise ValueError("Session state variable dubious_donation_types must"
                         " be initialized before use.")

    if "safe_donor_types" not in st.session_state:
        raise ValueError("Session state variables PLACEHOLDER_DATE and"
                         " PLACEHOLDER_ID must be initialized before use.")

    # Extend dubious donor criteria using session state variables
    loadclean_df["DubiousDonor"] = (
        (loadclean_df["DonorId"]
         .eq(st.session_state.PLACEHOLDER_ID)
         .astype(int)) +
        (loadclean_df["DonorName"]
         .isin(["Unidentified Donor", "Anonymous Donor"])
         .astype(int)) +
        (loadclean_df["DonationType"]
         .isin(["Unidentified Donor", "Impermissible Donor"])
         .astype(int))
    )

    # Use session state variables
# Use session state variables
    loadclean_df["DubiousData"] = (
        loadclean_df["DubiousDonor"] +
        (loadclean_df["DonationType"]
         .isin(st.session_state
               .dubious_donation_types).astype(int)) +
        loadclean_df["DonationAction"].ne("Accepted").astype(int) +
        loadclean_df["IsAggregation"].eq("True").astype(int) +
        (loadclean_df["NatureOfDonation"]
         .eq("Aggregated Donation")
         .astype(int)) +
        (loadclean_df["ReceivedDate"]
         .eq(st.session_state.PLACEHOLDER_DATE)
         .astype(int)) +
        (loadclean_df["RegulatedEntityId"]
         .eq(st.session_state.PLACEHOLDER_ID).astype(int)) +
        (loadclean_df["RegulatedEntityName"]
         .eq("Unidentified Entity")
         .astype(int)) +
        (loadclean_df["DonorId"]
         .eq(st.session_state.PLACEHOLDER_ID)
         .astype(int)) +
        loadclean_df["DonorName"].eq("Unidentified Donor").astype(int) -
        (loadclean_df["DonorStatus"].isin(st.session_state.safe_donor_types)
            .astype(int)) -  # Safe donors should be excluded
        (((loadclean_df["IsAggregation"].eq("True")) &
         (loadclean_df["DonorStatus"].isin(st.session_state.safe_donor_types)))
         .astype(int))  # Fixing subtraction
    )

    # if "DubiousData" is less than 0, set it to 0
    loadclean_df["DubiousData"] = loadclean_df["DubiousData"].clip(lower=0)

    # Create simple column to enable count of events using sum
    loadclean_df["EventCount"] = 1

    # Load party summary data to get RegEntity_Group
    RegulatedEntity_df = st.session_state.get("data_party_sum", None)
    if RegulatedEntity_df is None:
        RegulatedEntity_df = load_entity_summary_data()
        st.session_state["data_party_sum"] = RegulatedEntity_df

    # Create a dictionary to map RegulatedEntityName to RegEntity_Group
    reg_entity_dict = (
        RegulatedEntity_df
        .set_index("RegulatedEntityName")[["RegEntity_Group"]]
        .to_dict(orient="index")
        )

    # Apply dictionary to populate RegEntity_Group
    if "RegulatedEntityName" in loadclean_df.columns:
        loadclean_df["RegEntity_Group"] = (
            loadclean_df["RegulatedEntityName"]
            .map(lambda x: reg_entity_dict.get(x, {})
                 .get("RegEntity_Group", "Unknown"))
        )
    # Ensure all columns that are in data are also in data_clean
    for col in orig_df.columns:
        if col not in loadclean_df.columns:
            loadclean_df[col] = orig_df[col]

    # Drop Columns that are not needed
    loadclean_df = (
        loadclean_df.drop(['ReportingPeriodName_Date',
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
                           ], axis=1)
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
        cleaned_data_filename = (
            st.session_state.filenames["cleaned_data_fname"]
        )
        cleaned_data_filename = (
            os.path.join(output_dir, cleaned_data_filename)
        )
        # Save the cleaned data to a CSV file for further analysis or reporting
        loadclean_df.to_csv(cleaned_data_filename)

    return loadclean_df


def load_donorList_data(datafile=None, streamlitrun=True, output_csv=False):
    if streamlitrun:
        donorlist_df = st.session_state.get("data_clean", None)
        if donorlist_df is None:
            st.error("No data found in session state!")
            return None
    else:
        if datafile is None:
            donorlist_df = donorlist_df
        else:
            donorlist_df = datafile
    donorlist_df = (
        donorlist_df.groupby(['DonorId',
                              'DonorName'])
                    .agg({'Value': ['sum',
                                    'count',
                                    'mean']}).reset_index()
    )
    donorlist_df.columns = ['DonorId',
                            'Donor Name',
                            'Donations Value',
                            'Donation Events',
                            'Donation Mean']
    if output_csv:
        output_dir = st.session_state.directories["output_dir"]
        cleaned_donor_filename = (
            st.session_state.filenames["cleaned_donorlist_fname"]
        )
        cleaned_donor_filename = os.path.join(output_dir,
                                              cleaned_donor_filename)
        donorlist_df.to_csv(cleaned_donor_filename)

    return donorlist_df


def load_regulated_entity_data(datafile=None,
                               streamlitrun=True,
                               output_csv=False):
    if streamlitrun:
        regent_df = st.session_state.get("data_clean", None)
        if regent_df is None:
            st.error("No data found in session state!")
            return None
    else:
        if datafile is None:
            regent_df = regent_df
        else:
            regent_df = datafile
    regent_df = (
        regent_df.groupby(['RegulatedEntityId',
                           'RegulatedEntityName',
                           'RegEntity_Group'])
                 .agg({'Value': ['sum',
                                 'count',
                                 'mean']}).reset_index()
    )
    regent_df.columns = ['RegulatedEntityId',
                         'Regulated Entity Name',
                         'Regulated Entity Group',
                         'Donations Value',
                         'Donation Events',
                         'Donation Mean']
    if output_csv:
        output_dir = st.session_state.directories["output_dir"]
        cleaned_regentity_filename = (
            st.session_state.filenames["cleaned_regentity_fname"]
        )
        cleaned_regentity_filename = (
            os.path.join(output_dir, cleaned_regentity_filename)
        )
        regent_df.to_csv(cleaned_regentity_filename)

    return regent_df
