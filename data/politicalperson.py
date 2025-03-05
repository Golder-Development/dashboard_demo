import streamlit as st
import pandas as pd
from utils.logger import logger
from utils.logger import log_function_call  # Import decorator
from components.cleanpoliticalparty import get_party_df_from_pdpy


@log_function_call
def map_mp_to_party(loaddata_df):
    # Recollect data from Parliament API
    if st.session_state.RERUN_MP_PARTY_MEMBERSHIP:
        # check that pdpy is installed
        try:
            get_party_df_from_pdpy(from_date=st.session_state.min_date,
                                   to_date=st.session_state.max_date,
                                   while_mp=False,
                                   collapse=True)
        except ImportError:
            logger.error("pdpy is not installed. Please install pdpy first"
                         " if you wish to use the Parliament API."
                         " Will proceed with last copy of saved data.")
    # Ensure required files exist
    if st.session_state.politician_party_fname is None:
        logger.critical("ListOfPoliticalPeople_final.csv file is missing")
        st.error("ListOfPoliticalPeople_final.csv file is missing"
                 " Political Party Mataching will not be done")
        return loaddata_df
    if st.session_state.regentity_map_fname is None:
        logger.critical("Regulated entity mapping file is missing")
        st.error("Regulated entity mapping file is missing"
                 " Political Party Mataching will not be done")
        return loaddata_df
    # Clean column names in loaddata_df
    loaddata_df.columns = loaddata_df.columns.str.strip()
    # Check if 'PartyName' exists
    loaddata_df['PartyName'] = pd.NA
    if 'PartyName' not in loaddata_df.columns:
        logger.error("Missing column: 'PartyName' in"
                     " loaddata_df. Available columns: %s",
                     loaddata_df.columns)
    # Load and preprocess the political people dataset
    try:
        politician_party_dict = (
            pd.read_csv(st.session_state.politician_party_fname))
        politician_party_dict.columns = (
            politician_party_dict.columns.str.strip())
    except Exception as e:
        logger.error("Error reading politician_party_fname: %s", e)
        return loaddata_df
    # Rename columns and ensure required fields exist
    expected_cols = {'Original RegulatedEntityId': 'RegulatedEntityId',
                     'PoliticalParty_pdpy': 'PartyName'}
    missing_cols = [
        col for col in expected_cols
        if col not in politician_party_dict.columns
    ]
    if missing_cols:
        logger.error("Missing columns in politician_party_dict: %s",
                     missing_cols)
        st.error("Missing columns in politician_party_dict: %s",
                 missing_cols)
        return loaddata_df
    # Rename columns and select required columns
    politician_party_dict = (
        politician_party_dict.rename(columns=expected_cols)[
            ['RegulatedEntityId', 'PartyName']
        ])
    logger.debug("Loaded politician_party_dict: %s",
                 politician_party_dict.head())
    # Validate PartyParents mapping dictionary
    PartyUpdate_dict = st.session_state.data_remappings.get("PartyParents", {})
    if not isinstance(PartyUpdate_dict, dict):
        logger.error("PartyParents mapping is not a valid dictionary")
        st.error("PartyParents mapping is not a valid dictionary"
                 " Political Party Mataching will not be done")
        return loaddata_df
    # Log keys for debugging
    logger.debug("PartyUpdate_dict keys: %s", PartyUpdate_dict.keys())
    # Normalize case for mapping
    loaddata_df['PartyName'] = loaddata_df['PartyName'].str.strip().str.lower()
    PartyUpdate_dict = {k.lower(): v for k, v in PartyUpdate_dict.items()}
    # Map PartyId based on PartyName
    loaddata_df['PartyId'] = (
        loaddata_df['PartyName'].map(PartyUpdate_dict)
        .combine_first(loaddata_df['RegulatedEntityId'])
        )
    logger.debug("Updated loaddata_df with PartyId: %s", loaddata_df.head())
    # Load and preprocess the regulated entity mapping file
    try:
        RegulatedEntityNameMatch = (
            pd.read_csv(st.session_state.regentity_map_fname)
            )
        RegulatedEntityNameMatch.columns = (
            RegulatedEntityNameMatch.columns.str.strip()
            )
    except Exception as e:
        logger.error("Error reading regentity_map_fname: %s", e)
        st.error("Error reading regentity_map_fname: %s", e,
                 " Political Party Mataching will not be done")
        return loaddata_df
    # Ensure required columns exist
    expected_cols = {'CleanedRegulatedEntityId': 'PartyId',
                     'CleanedRegulatedEntityName': 'PartyName'}
    missing_cols = [
        col for col in expected_cols
        if col not in RegulatedEntityNameMatch.columns
    ]
    if missing_cols:
        logger.error("Missing columns in"
                     " RegulatedEntityNameMatch: %s", missing_cols,
                     "political party matching will not be done")
        st.error("Missing columns in"
                 " RegulatedEntityNameMatch: %s", missing_cols,
                 "political party matching will not be done")
        return loaddata_df
    RegulatedEntityNameMatch = (
        RegulatedEntityNameMatch
        .rename(columns=expected_cols)[['PartyId', 'PartyName']]
        )
    logger.debug("Loaded RegulatedEntityNameMatch: %s",
                 RegulatedEntityNameMatch.head())
    # Merge regulated entity names
    loaddata_df = pd.merge(loaddata_df,
                           RegulatedEntityNameMatch,
                           how='left',
                           on='PartyId',
                           suffixes=('', '_y'))
    # Remove duplicate columns from merging
    loaddata_df.drop(columns=[col for col in loaddata_df.
                              columns if col.endswith('_y')],
                     inplace=True)
    logger.debug("loaddata_df after merging: %s",
                 loaddata_df.head())
    
    # Ensure PartyName and PartyId are properly assigned
    loaddata_df['PartyName'] = (
        loaddata_df['PartyName'].
        replace("", pd.NA).
        combine_first(loaddata_df['RegulatedEntityName']).
        fillna("Unidentified Party")
    )
    loaddata_df['PartyId'] = (
        loaddata_df['PartyId'].
        replace("", pd.NA).
        combine_first(loaddata_df['RegulatedEntityId']).
        fillna(10000001)
    )
    
    # compare rows in dataset to original data to check for duplicates
    if len(loaddata_df) != len(st.session_state.raw_data):
        logger.error("Number of rows in loaddata_df and raw_data do not match"
                     f" {len(loaddata_df)} !="
                     f" {len(st.session_state.raw_data)}")
        st.error("Number of rows in loaddata_df and raw_data do not match"
                 f" {len(loaddata_df)} != {len(st.session_state.raw_data)}")
        logger.error("Attempting to remove duplicates")
        st.error("Attempting to remove duplicates")
        loaddata_df = loaddata_df.drop_duplicates()

        # recompare rows in dataset to original data to check for duplicates
        if len(loaddata_df) != len(st.session_state.raw_data):
            logger.error("Number of rows in loaddata_df and raw_data"
                         " do not match"
                         f" {len(loaddata_df)} !="
                         f" {len(st.session_state.raw_data)}"
                         " Political Party Mataching reversed")
            st.error("Number of rows in loaddata_df and raw_data do not match"
                     f" {len(loaddata_df)} != {len(st.session_state.raw_data)}"
                     " Political Party Mataching will not be done")
            return None

    # Log unique values for PartyName
    logger.debug("loaddata_df after updating PartyName and PartyId: %s",
                 loaddata_df.head())
    logger.debug("loaddata_df PartyName unique values: %s",
                 loaddata_df['PartyName'].unique())
    logger.info("Data Updated with PartyName and PartyId successfully")
    st.success("Data Updated with PartyName and PartyId successfully")
    # return updated data
    return loaddata_df
