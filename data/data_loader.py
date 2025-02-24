import streamlit as st
from components.global_variables import initialize_session_state
from data.datasetupandclean import (load_cleaned_data, load_data,
                                    load_donorList_data,
                                    load_regulated_entity_data,
                                    create_thresholds,
                                    load_party_summary_data)


@st.cache_data
def get_data():
    return load_data(output_csv=False,
                     dedupe_donors=True,
                     dedupe_regentity=True
                     )


@st.cache_data
def get_party_summary_data():
    return load_party_summary_data(datafile=None,
                                   output_csv=False,
                                   streamlitrun=True)


@st.cache_data
def get_cleaned_data():
    return load_cleaned_data(datafile=None,
                             output_csv=False,
                             streamlitrun=True)


@st.cache_data
def get_donor_data():
    return load_donorList_data(datafile=None,
                               output_csv=False,
                               streamlitrun=True)


@st.cache_data
def get_regentity_data():
    return load_regulated_entity_data(datafile=None,
                                      output_csv=False,
                                      streamlitrun=True)


def firstload():
    initialize_session_state()

    # Ensure g_thresholds is available as a global dictionary
    if 'g_thresholds' not in st.session_state:
        create_thresholds()

    # Load and cache data correctly
    if "data" not in st.session_state:
        st.session_state["data"] = get_data()

    if "data_party_sum" not in st.session_state:
        st.session_state["data_party_sum"] = get_party_summary_data()

    if "data_clean" not in st.session_state:
        st.session_state["data_clean"] = get_cleaned_data()

    if "data_donor" not in st.session_state:
        st.session_state["data_donor"] = get_donor_data()

    if "data_regentity" not in st.session_state:
        st.session_state["data_regentity"] = get_regentity_data()

    # Remove the loading message

