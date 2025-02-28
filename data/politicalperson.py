import streamlit as st
import pandas as pd
from utils.logger import logger
from utils.logger import log_function_call  # Import decorator


@log_function_call
def map_mp_to_party(loaddata_df):
    if st.session_state.politician_party_fname is None:
        # check file ListOfPoliticalPeople.csv is present
        logger.error("ListOfPoliticalPeople_final.csv file is missing")
        return
    else:
        # import ListOfPoliticalPeople_Final.csv file
        politician_party_dict = (
             pd.read_csv(st.session_state.politician_party_fname)
        )
        # print top 5 rows of the dataframe
        logger.info("politician_party_dict: %s", politician_party_dict.head())
        # Keep OriginalRegulatedEntityId and PoliticalParty_pdpy columns
        politician_party_dict = (
             politician_party_dict[['Original RegulatedEntityId',
                                    'PoliticalParty_pdpy']]
        )
        # rename OriginalRegulatedEntityId to RegulatedEntityId
        # and PoliticalParty_pdpy to PartyName
        politician_party_dict.rename(
             columns={'Original RegulatedEntityId': 'RegulatedEntityId',
                      'PoliticalParty_pdpy': 'PartyName'}, inplace=True)
        # load PartyParents Dictionary
        PartyUpdate_dict = st.session_state.data_remappings["PartyParents"]
        logger.info("PartyUpdate_df: %s", PartyUpdate_dict)
        # use PartyUpdate_dict to map PartyId based of PartyName
        loaddata_df['PartyId'] = (
             politician_party_dict['PartyName'].map(PartyUpdate_dict)
        )
        # print top 5 rows of the dataframe
        logger.info("loaddata_df: %s", loaddata_df.head())
        # load regulatedentitymap file
        RegulatedEntityNameMatch = (
             pd.read_csv(st.session_state.regentity_map_fname)
        )
        # rename reagulatedentitynamematch column RegulatedEntityID to PartyId
        # and RegulatedEntityName to PartyName
        RegulatedEntityNameMatch.rename(
             columns={'CleanedRegulatedEntityId': 'PartyId',
                      'CleanedRegulatedEntityName': 'PartyName'},
             inplace=True)
        # print top 5 rows of the dataframe
        logger.info("RegulatedEntityNameMatch: %s",
                    RegulatedEntityNameMatch.head())
        # drop all other columns from RegulatedEntityNameMatch except PartyId
        # and PartyName
        RegulatedEntityNameMatch = (
             RegulatedEntityNameMatch[['PartyId', 'PartyName']]
        )
        # update PartyName based on PartyId
        loaddata_df = pd.merge(loaddata_df,
                               RegulatedEntityNameMatch,
                               how='left',
                               on='PartyId')
        # print top 5 rows of the dataframe
        logger.info("loaddata_df: %s", loaddata_df.head())
        # update blank PartyName to RegulatedEntityName and PartyId
        # to RegulatedEntityId
        loaddata_df['PartyName'] = (
             loaddata_df['PartyName'].replace("",
                                              loaddata_df['RegulatedEntityName'])
             )
        loaddata_df['PartyName'] = (
             loaddata_df['PartyName'].isna(loaddata_df['RegulatedEntityName'])
             )
        loaddata_df['PartyId'] = (
             loaddata_df['PartyId'].replace("",
                                            loaddata_df['RegulatedEntityId'])
             )
        loaddata_df['PartyId'] = (
             loaddata_df['PartyId'].isna(loaddata_df['RegulatedEntityId'])
             )
        # update blank PartyName to "Unidentified Party"
        loaddata_df['PartyName'] = (
             loaddata_df['PartyName'].replace("",
                                              "Unidentified Party")
             )
        loaddata_df['PartyName'] = (
             loaddata_df['PartyName'].isna("Unidentified Party")
             )
        # update blank PartyId to "1000001"
        loaddata_df['PartyId'] = (
             loaddata_df['PartyId'].replace("", 10000001)
             )
        loaddata_df['PartyId'] = (
             loaddata_df['PartyId'].isna(10000001)
             )

    return loaddata_df
