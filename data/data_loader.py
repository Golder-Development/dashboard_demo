import streamlit as st
from data.datasetupandclean import load_raw_data
from data.clean_and_enhance import load_cleaned_data
from data.load_donor_regent_lists import (load_donorList_data,
                                          load_regulated_entity_data
                                          )
from utils.logger import log_function_call, logger


@log_function_call
@st.cache_data
def get_raw_data():
    return load_raw_data(
        main_file="raw_data",
        cleaned_file="raw_data_clean",
        output_csv=True,
        dedupe_donors=True,
        dedupe_regentity=True,
        originaldatafilepath="source_data_fname",
        processeddatafilepath="imported_raw_fname")


@log_function_call
@st.cache_data
def get_cleaned_data():
    return load_cleaned_data(
        originaldatafilepath="cleaned_donations_fname",
        processeddatafilepath="cleaned_data_fname",
        datafile="raw_data",
        streamlitrun=True,
        output_csv=True,
        main_file="raw_data",
        cleaned_file="data_clean")


@log_function_call
@st.cache_data
def get_donor_data():
    return load_donorList_data(
        main_file="data_clean",
        cleaned_file="data_donor",
        streamlitrun=True,
        output_csv=True,
        originaldatafilepath="cleaned_data_fname",
        cleaneddatafilepath="cleaned_donorlist_fname")


@log_function_call
@st.cache_data
def get_regentity_data():
    return load_regulated_entity_data(
        main_file="data_clean",
        cleaned_file="data_regentity",
        streamlitrun=True,
        output_csv=True,
        originaldatafilepath="cleaned_data_fname",
        cleaneddatafilepath="cleaned_regentity_fname",
        )


@log_function_call
@st.cache_data
def firstload():
    # Ensure g_thresholds is available as a global dictionary
    # if 'g_thresholds' not in st.session_state:
    #     create_thresholds()
    def load_data_to_session(key, loader_function):
        if key not in st.session_state:
            st.session_state[key] = loader_function()
            return key
        else:
            return key

    # Load and cache data correctly
    load_data_to_session("raw_data", get_raw_data)
    logger.debug(f"st.session_state.raw_data: {len(st.session_state.raw_data)}")
    load_data_to_session("data_clean", get_cleaned_data)
    logger.debug(f"st.session_state.raw_data: {len(st.session_state.data_clean)}")
    # load_data_to_session("data_party_sum", get_party_summary_data)
    load_data_to_session("data_donor", get_donor_data)
    logger.debug(f"st.session_state.data_donor: {len(st.session_state.data_donor)}")
    logger.debug(f"st.session_state.data_clean: {len(st.session_state.data_clean)}")
    load_data_to_session("data_regentity", get_regentity_data)
    logger.debug(f"st.session_state.data_regentity: {len(st.session_state.data_regentity)}")
    logger.debug(f"st.session_state.data_donor: {len(st.session_state.data_donor)}")
    logger.debug(f"st.session_state.data_clean: {len(st.session_state.data_clean)}")
