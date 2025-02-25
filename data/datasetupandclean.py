import pandas as pd
import streamlit as st
import os
from rapidfuzz import process, fuzz
from collections import defaultdict
from components import mappings as mp
from components import calculations as calc


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


def load_entity_summary_data(datafile=None,
                             streamlitrun=True,
                             output_csv=False):
    # Load the data
    output_dir = st.session_state.directories["output_dir"]

    if streamlitrun:
        entitysummary_df = st.session_state.get("raw_data", None)
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
    thresholds = st.session_state.thresholds
    RegulatedEntity_df['RegEntity_Group'] = calc.determine_groups_optimized(RegulatedEntity_df,
                       'RegulatedEntityName',
                       "DonationEvents",
                       thresholds)

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


def dedupe_entity_file(loaddata_dd_df,
                       entity,
                       map_filename,
                       threshold=85,
                       output_csv=False):
    """
    loads a dedupe mapping file from reference folder and
    merges it with the original data.  Merges on field named
    {entity]id creates new columns original{entity}id and
    original{entity}name - new data is returned in a dataframe
    called loaddata_dd_df.  If the file does not exist, the
    dedupe_entity_fuzzy function is called to dedupe the data
    and return the new data in loaddata_dd_df
    """
    # Load the data
    ref_dir = st.session_state.directories["reference_dir"]
    originalentityname = f"Original{entity}Name"
    originalentityid = f"Original{entity}Id"
    entityname = f"{entity}Name"
    entityid = f"{entity}Id"
    cleanedentityname = f"Cleaned{entity}Name"
    cleanedentityid = f"Cleaned{entity}Id"
    # check that reentity_deduped file exists using global variables
    if map_filename not in st.session_state.filenames:
        raise ValueError(f"{map_filename} not found"
                         " in session state filenames")
    else:
        # check that join on field exists in the data
        if entityid not in loaddata_dd_df.columns:
            raise ValueError(f"{entityid} not found in data")
    # check that file exists at identified path from global var
    if os.path.exists(os.path.join(ref_dir,
                                   st.session_state
                                   .filenames[map_filename])):
        # load regentity_map_fname file using global variables
        dedupedfilename = (
            st.session_state.filenames[map_filename])
        dedupedfilepath = os.path.join(ref_dir, dedupedfilename)
        re_dedupe_df = pd.read_csv(dedupedfilepath)
        # merge re_dedupe_df with original data
        loaddata_dd_df = pd.merge(loaddata_dd_df,
                                  re_dedupe_df,
                                  how='left',
                                  on=entityid)
        # rename RegulatedEntityName_x to RegulatedEntityName
        # and RegulatedEntityName_y to OriginalRegulatedEntityName
        entityname_x = f"{entityname}_x"
        entityname_y = f"{entityname}_y"
        loaddata_dd_df.rename(
            columns={entityname_x: entityname,
                     entityname_y: originalentityname
                     }, inplace=True)
        # use the RegulatedEntityId and RegulatedEntityName columns
        # to update the original data with new columns called
        # parententityid and parententityname - in no match exists
        # the original data will be used

        loaddata_dd_df['ParentEntityId'] = (
            loaddata_dd_df[cleanedentityid].replace("", pd.NA)
        )
        loaddata_dd_df['ParentEntityName'] = (
            loaddata_dd_df[cleanedentityname].replace("", pd.NA)
        )
        loaddata_dd_df['ParentEntityId'] = (
            loaddata_dd_df['ParentEntityId']
            .fillna(loaddata_dd_df[entityid])
        )
        loaddata_dd_df['ParentEntityName'] = (
            loaddata_dd_df['ParentEntityName']
            .fillna(loaddata_dd_df[entityname])
        )
        loaddata_dd_df.rename(
            columns={entityid: originalentityid,
                     entityname: originalentityname,
                     "ParentEntityId": entityid,
                     "ParentEntityName": entityname},
            inplace=True)
        return loaddata_dd_df
    else:
        # Run dedupe logic if file does not exist
        loaddata_dd_df = dedupe_entity_fuzzy(loaddata_dd_df,
                                             entity,
                                             threshold=85,
                                             output_csv=output_csv)
    return loaddata_dd_df


def dedupe_entity_fuzzy(deupedf, entity, threshold=85, output_csv=False):
    # Load the data
    output_dir = st.session_state.directories["output_dir"]

    originalentityname = f"Original{entity}Name"
    originalentityid = f"Original{entity}Id"
    entityname = f"{entity}Name"
    entityid = f"{entity}Id"
    cleanedentityname = f"Cleaned{entity}Name"
    cleanedentityid = f"Cleaned{entity}Id"
    # Extract donor names and IDs
    loaddata_dd_df = deupedf.copy()
    entity_names = (
        loaddata_dd_df[[entityid,
                        entityname]].drop_duplicates()
        )

    # Preprocess names (lowercase and remove special characters)
    entity_names["CleanedName"] = (
        entity_names[entityname]
        .str.lower()
        .str.replace(r"[^a-z0-9\s]", "", regex=True)
        )

    # Create a mapping of donor names to IDs
    name_to_id = (
        entity_names.set_index("CleanedName")[entityid].to_dict()
    )

    # Dictionary to store potential duplicates
    potential_duplicates = defaultdict(set)

    # Apply fuzzy matching
    for cleaned_name, entityid in name_to_id.items():
        matches = process.extract(cleaned_name,
                                  name_to_id.keys(),
                                  scorer=fuzz.ratio,
                                  limit=5)
        for match_name, score, _ in matches:
            if score >= threshold and match_name != cleaned_name:
                match_id = name_to_id[match_name]
                potential_duplicates[entityid].add(match_id)
                potential_duplicates[match_id].add(entityid)

    # Convert sets to lists
    potential_duplicates = {k: list(v) for k,
                            v in potential_duplicates.items()}

    # Save results to a CSV file
    fname = f"potential_{entity}_duplicates_fname"
    if output_csv:
        potential_regentity_duplicates_filemane = (
            st.session_state
            .filenames[fname]
        )
        potential_regentity_duplicates_filemane = (
            os.path.join(output_dir,
                         potential_regentity_duplicates_filemane)
        )
        output_df = (
            pd.DataFrame(potential_duplicates.items(),
                         columns=[entityid,
                         "Potential Duplicates"])
            )

        output_df.to_csv(potential_regentity_duplicates_filemane,
                         index=False)

    # Create mappings for cleansed ID and Name
    id_to_cleansed = {}
    name_to_cleansed = {}

    for main_id, duplicate_ids in potential_duplicates.items():
        all_ids = [main_id] + duplicate_ids
        # Choose the smallest entityid
        cleansed_id = min(all_ids)

        # Get all names corresponding to these IDs
        matching_names = (
            loaddata_dd_df[loaddata_dd_df[entityid].isin(all_ids)][entityname]
        )

        # Choose the most frequent name
        cleansed_name = matching_names.value_counts().idxmax()

        # Store mappings
        for entityid in all_ids:
            id_to_cleansed[entityid] = cleansed_id
            name_to_cleansed[entityid] = cleansed_name

    # convert Id = "" to null
    loaddata_dd_df[entityid] = (
        loaddata_dd_df[entityid].replace("", pd.NA)
    )
    # Apply mappings to the dataset
    loaddata_dd_df[cleanedentityid] = (
        loaddata_dd_df[entityid]
        .map(id_to_cleansed)
        .fillna(loaddata_dd_df[entityid])
        )
    loaddata_dd_df[cleanedentityname] = (
        loaddata_dd_df[entityname]
        .map(name_to_cleansed)
        .fillna(loaddata_dd_df[entityname])
        )

    # rename Cleansed ID to Id and Cleansed Name to Name
    loaddata_dd_df.rename(
        columns={entityid: originalentityid,
                 entityname: originalentityname,
                 cleanedentityid: entityid,
                 cleanedentityname: entityname},
        inplace=True
        )
    return loaddata_dd_df


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
    # Fill blank ReceivedDate with ReportedDate, AcceptedDate,
    # or ReportingPeriodName_Date
    loadclean_df['ReceivedDate'] = (
        loadclean_df['ReceivedDate']
        .fillna(loadclean_df['ReportedDate'])
        .fillna(loadclean_df['AcceptedDate'])
        .fillna(pd.to_datetime(
            loadclean_df['ReportingPeriodName'].str.strip().str[-10:],
            dayfirst=True,
            format='mixed',
            errors='coerce'
        ).dt.normalize())
    )
    # Convert ReceivedDate to datetime and set any remaining missing dates
    # to 1900-01-01
    loadclean_df['ReceivedDate'] = (
        pd.to_datetime(loadclean_df['ReceivedDate'],
                       dayfirst=True,
                       format='mixed',
                       errors='coerce')
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
        loadclean_df["NatureOfDonation"] = (
            loadclean_df.apply(mp.map_nature_of_donation, axis=1)
        )
        loadclean_df["NatureOfDonation"] = (
            loadclean_df["NatureOfDonation"].replace(
                {"Donation to nan": "Other", "Other Payment": "Other"}
            ))

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

    # Apply dictionary to populate RegEntity_Group
    thresholds = st.session_state.thresholds
    if "RegulatedEntityName" in loadclean_df.columns:
        loadclean_df["RegEntity_Group"] = calc.determine_groups_optimized(
                loadclean_df,
                'RegulatedEntityName',
                "EventCount",
                thresholds)

    # Ensure all columns that are in data are also in data_clean
    for col in orig_df.columns:
        if col not in loadclean_df.columns:
            loadclean_df[col] = orig_df[col]

    # Drop Columns that are not needed
    loadclean_df = (
        loadclean_df.drop([
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
        # Load the data
        output_dir = st.session_state.directories["output_dir"]

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
    # Load the data
    output_dir = st.session_state.directories["output_dir"]
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
                           'RegEntity_Group'], observed=True)
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


def map_mp_to_party():
    # if ListOfPoliticalPeople_Final.csv file does not exist:
    #     # import ListOfPoliticalPeople_Final.csv file
    #     base_dir = st.session_state.base_dir
    #     politician_party_filename = st.session_state.filenames
    # ["politician_party_fname"]
    #     politician_party_filepath = os.path.join(base_dir,
    # politician_party_filename)
    #     politician_party_df = pd.read_csv(politician_party_filepath)
    #     # merge ListOfPoliticalPeople_Final.csv file with original data
    #     loaddata_df = pd.merge(df, politician_party_df, how='left',
    # on='RegulatedEntityID')
    #     # update blank PartyName to "Unidentified Party"
    #     loaddata_df['PartyName'] = loaddata_df['PartyName'].replace("",
    # RegulatedEntityName)
    #     # update blank PartyId to "1000001"
    #     loaddata_df['PartyId'] = loaddata_df['PartyId'].replace("",
    # RegulatedEntityId)
    #     # update blank PoliticianName to "Unidentified Politician"
    #     loaddata_df['PoliticianName'] = loaddata_df['PoliticianName']
    # .replace("", "Unidentified Politician")
    #     # update blank PoliticianId to "1000001"
    #     loaddata_df['PoliticianId'] = loaddata_df['PoliticianId'].replace("",
    # "1000001")

    return
