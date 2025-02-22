import streamlit as st
from data.datasetupandclean import (load_cleaned_data, load_data,
                                    load_donorList_data,
                                    load_regulated_entity_data,
                                    load_party_summary_data)


@st.cache_data
def get_data():
    return load_data(output_csv=False,
                     dedupe_donors=False,
                     dedupe_regentity=False
                     )


@st.cache_data
def get_party_summary_data():
    return load_party_summary_data(output_csv=False)


@st.cache_data
def get_cleaned_data():
    return load_cleaned_data(output_csv=False)


@st.cache_data
def get_donor_data():
    return load_donorList_data(output_csv=False)


@st.cache_data
def get_regentity_data():
    return load_regulated_entity_data(output_csv=False)
