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
    from data.data_file_defs import normalize_string_columns_for_streamlit
    cleaned_df = load_cleaned_data(
        originaldatafilepath="cleaned_donations_fname",
        processeddatafilepath="cleaned_data_fname",
        datafile="raw_data",
        streamlitrun=True,
        output_csv=True,
        main_file="raw_data",
        cleaned_file="data_clean")
    return normalize_string_columns_for_streamlit(cleaned_df)


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
def firstload():
    def load_data_to_session(key, loader_function):
        if key not in st.session_state:
            st.session_state[key] = loader_function()
            return key
        else:
            return key

    # Load and cache data correctly
    load_data_to_session("raw_data", get_raw_data)
    if "raw_data" not in st.session_state:
        logger.info("raw_data not in session state.")
    else:
        logger.debug("st.session_state.raw_data:"
                     f" {len(st.session_state.raw_data)}")
    load_data_to_session("data_clean", get_cleaned_data)
    if "data_clean" not in st.session_state:
        logger.info("data_clean not in session state.")
    else:
        logger.debug("st.session_state.raw_data:"
                    f" {len(st.session_state.data_clean)}")
    # load_data_to_session("data_party_sum", get_party_summary_data)
    load_data_to_session("data_donor", get_donor_data)
    if "data_clean" not in st.session_state:
        logger.info("data_clean not in session state.")
    else:
        logger.debug("st.session_state.data_donor:"
                    f" {len(st.session_state.data_donor)}")
        logger.debug("st.session_state.data_clean:"
                    f" {len(st.session_state.data_clean)}")
    load_data_to_session("data_regentity", get_regentity_data)
    if "data_clean" not in st.session_state:
        logger.info("data_clean not in session state.")
    else:
        logger.debug("st.session_state.data_regentity:"
                    f" {len(st.session_state.data_regentity)}")
        logger.debug("st.session_state.data_donor:"
                    f" {len(st.session_state.data_donor)}")
        logger.debug("st.session_state.data_clean:"
                    f" {len(st.session_state.data_clean)}")
