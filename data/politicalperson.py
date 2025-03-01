import streamlit as st
import pandas as pd
from utils.logger import logger
from utils.logger import log_function_call  # Import decorator

@log_function_call
def map_mp_to_party(loaddata_df):
    # Ensure required files exist
    if st.session_state.politician_party_fname is None:
        logger.error("ListOfPoliticalPeople_final.csv file is missing")
        return loaddata_df
    if st.session_state.regentity_map_fname is None:
        logger.error("Regulated entity mapping file is missing")
        return loaddata_df

    # Clean column names in loaddata_df
    loaddata_df.columns = loaddata_df.columns.str.strip()

    # Check if 'PartyName' exists
    if 'PartyName' not in loaddata_df.columns:
        logger.error("Missing column: 'PartyName' in loaddata_df. Available columns: %s", loaddata_df.columns)
        loaddata_df['PartyName'] = pd.NA

    # Load and preprocess the political people dataset
    try:
        politician_party_dict = pd.read_csv(st.session_state.politician_party_fname)
        politician_party_dict.columns = politician_party_dict.columns.str.strip()
    except Exception as e:
        logger.error("Error reading politician_party_fname: %s", e)
        return loaddata_df

    # Rename columns and ensure required fields exist
    expected_cols = {'Original RegulatedEntityId': 'RegulatedEntityId', 'PoliticalParty_pdpy': 'PartyName'}
    missing_cols = [col for col in expected_cols if col not in politician_party_dict.columns]

    if missing_cols:
        logger.error("Missing columns in politician_party_dict: %s", missing_cols)
        return loaddata_df

    politician_party_dict = politician_party_dict.rename(columns=expected_cols)[['RegulatedEntityId', 'PartyName']]
    logger.info("Loaded politician_party_dict: %s", politician_party_dict.head())

    # Validate PartyParents mapping dictionary
    PartyUpdate_dict = st.session_state.data_remappings.get("PartyParents", {})

    if not isinstance(PartyUpdate_dict, dict):
        logger.error("PartyParents mapping is not a valid dictionary")
        return loaddata_df

    # Log keys for debugging
    logger.info("PartyUpdate_dict keys: %s", PartyUpdate_dict.keys())

    # Normalize case for mapping
    loaddata_df['PartyName'] = loaddata_df['PartyName'].str.strip().str.lower()
    PartyUpdate_dict = {k.lower(): v for k, v in PartyUpdate_dict.items()}

    # Map PartyId based on PartyName
    loaddata_df['PartyId'] = loaddata_df['PartyName'].map(PartyUpdate_dict).combine_first(loaddata_df['RegulatedEntityId'])
    logger.info("Updated loaddata_df with PartyId: %s", loaddata_df.head())

    # Load and preprocess the regulated entity mapping file
    try:
        RegulatedEntityNameMatch = pd.read_csv(st.session_state.regentity_map_fname)
        RegulatedEntityNameMatch.columns = RegulatedEntityNameMatch.columns.str.strip()
    except Exception as e:
        logger.error("Error reading regentity_map_fname: %s", e)
        return loaddata_df

    # Ensure required columns exist
    expected_cols = {'CleanedRegulatedEntityId': 'PartyId', 'CleanedRegulatedEntityName': 'PartyName'}
    missing_cols = [col for col in expected_cols if col not in RegulatedEntityNameMatch.columns]

    if missing_cols:
        logger.error("Missing columns in RegulatedEntityNameMatch: %s", missing_cols)
        return loaddata_df

    RegulatedEntityNameMatch = RegulatedEntityNameMatch.rename(columns=expected_cols)[['PartyId', 'PartyName']]
    logger.info("Loaded RegulatedEntityNameMatch: %s", RegulatedEntityNameMatch.head())

    # Merge regulated entity names
    loaddata_df = pd.merge(loaddata_df, RegulatedEntityNameMatch, how='left', on='PartyId', suffixes=('', '_y'))

    # Remove duplicate columns from merging
    loaddata_df.drop(columns=[col for col in loaddata_df.columns if col.endswith('_y')], inplace=True)
    logger.info("loaddata_df after merging: %s", loaddata_df.head())

    # Ensure PartyName and PartyId are properly assigned
    loaddata_df['PartyName'] = loaddata_df['PartyName'].replace("", pd.NA).combine_first(loaddata_df['RegulatedEntityName']).fillna("Unidentified Party")
    loaddata_df['PartyId'] = loaddata_df['PartyId'].replace("", pd.NA).combine_first(loaddata_df['RegulatedEntityId']).fillna(10000001)

    logger.info("loaddata_df after updating PartyName and PartyId: %s", loaddata_df.head())
    logger.info("loaddata_df PartyName unique values: %s", loaddata_df['PartyName'].unique())
    logger.info("Data Updated with PartyName and PartyId successfully")
    return loaddata_df
