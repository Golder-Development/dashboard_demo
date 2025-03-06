import streamlit as st
import pandas as pd
from utils.logger import logger
from utils.logger import log_function_call  # Import decorator


@log_function_call
def map_mp_to_party(loaddata_df):
    logger.debug("loaddata_df RegulatedEntityName unique values: %s",
                 len(loaddata_df['RegulatedEntityName'].unique()))
    # Recollect data from Parliament API
    if st.session_state.politician_party_fname is None:
        logger.critical("ListOfPoliticalPeople_final.csv file is missing")
    # Load and preprocess the political people dataset
        try:
            politician_party_dict = (
                pd.read_csv(st.session_state.politician_party_fname))
            politician_party_dict.columns = (
                politician_party_dict.columns.str.strip())
            # drop RegisterName, RegulatedDoneeType, RegulatedEntityType,
            # Status, OriginalRegulatedEntityId, OriginalRegulatedEntityName
            politician_party_dict = politician_party_dict.drop(
                columns=["RegisterName", "RegulatedDoneeType",
                         "RegulatedEntityType", "Status",
                         "OriginalRegulatedEntityId",
                         "OriginalRegulatedEntityName"])
            # filter out PoliticalParty_pdpy == "Unknown"
            politician_party_dict = politician_party_dict[
                politician_party_dict["PoliticalParty_pdpy"] != "Unknown"]
            # rename PoliticalParty_pdpy to PartyName
            politician_party_dict = politician_party_dict.rename(
                columns={"PoliticalParty_pdpy": "PartyName"})
            RegulatedEntityNameMatch = (
                pd.read_csv(st.session_state.regentity_map_fname)
                )
            RegulatedEntityNameMatch.columns = (
                RegulatedEntityNameMatch.columns.str.strip()
                )
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
            PartyUpdate_dict = (
                st.session_state.data_remappings.get("PartyParents", {}))
        except Exception as e:
            logger.error("Error reading files for party matching: %s", e)       
            loaddata_df['PartyName'] = pd.NA
            loaddata_df['PartyId'] = pd.NA
            st.error("Political Party Mataching will not be done")
            return loaddata_df
    # Validate PartyParents mapping dictionary
    loaddata_df['PartyName'] = pd.NA
    loaddata_df['PartyId'] = pd.NA
    # Normalize case for mapping
    loaddata_df['PartyName'] = loaddata_df['PartyName'].str.strip().str.lower()
    PartyUpdate_dict = {k.lower(): v for k, v in PartyUpdate_dict.items()}
    # add PartyId based on PartyName from PartyUpdate_dict to political_party_dict
    politician_party_dict['PartyId'] = (
        politician_party_dict['PartyName'].map(PartyUpdate_dict)
        .combine_first(politician_party_dict['RegulatedEntityId'])
        )
    logger.debug("Updated politician_party_dict with PartyId:")
    # rename columns to match expected columns
    RegulatedEntityNameMatch = (
        RegulatedEntityNameMatch
        .rename(columns=expected_cols)[['PartyId', 'RegEntPartyName']]
        )
    # drop all columns except PartyId and RegEntPartyName
    RegulatedEntityNameMatch = RegulatedEntityNameMatch.dropna(
        subset=['PartyId', 'RegEntPartyName'])
    logger.debug("Loaded RegulatedEntityNameMatch: ")
    # add RegulatedEntityName as RegEntPartyName to political_party_dict based of PartyId
    politician_party_dict = pd.merge(politician_party_dict,
                                     RegulatedEntityNameMatch,
                                     how='left',
                                     on='PartyId',
                                     suffixes=('', '_y'))
    # Remove duplicate columns from merging
    politician_party_dict.drop(columns=[col for col in politician_party_dict.
                                        columns if col.endswith('_y')],
                                 inplace=True)
    # remove duplicate rows based on RegulatedEntityId if more than 1 row keep the first
    politician_party_dict = politician_party_dict.drop_duplicates(
        subset=['RegulatedEntityId'], keep='first')
    # USING political_party_dict to update loaddata_df with PartyName and PartyId by
    # matching on RegulatedEntityId
    loaddata_df = pd.merge(loaddata_df,
                           politician_party_dict,
                           how='left',
                           on='RegulatedEntityId',
                           suffixes=('', '_y'))
    # Remove duplicate columns from merging
    loaddata_df.drop(columns=[col for col in loaddata_df.columns
                              if col.endswith('_y')],
                      inplace=True)
    # Ensure PartyName and PartyId are properly assigned, if null try and set to RegulatedEntityName and RegulatedEntityId
    # if no match then fill with "Unidentified Party" and 10000001
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
    logger.debug("loaddata_df PartyName unique values: %s",
                 len(loaddata_df['PartyName'].unique()))
    logger.debug("loaddata_df RegulatedEntityName unique values: %s",
                 len(loaddata_df['RegulatedEntityName'].unique()))
    logger.info("Data Updated with PartyName and PartyId successfully")
    st.success("Data Updated with PartyName and PartyId successfully")
    # return updated data
    return loaddata_df
