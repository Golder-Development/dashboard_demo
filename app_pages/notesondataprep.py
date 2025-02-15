import streamlit as st
import calculations as ppcalc


def notesondataprep_body():
    df = st.session_state.get("data_clean", None)
    # set filters to None and filtered_df to the original dataset
    filters = None
    filtered_df = df
    min_date = ppcalc.get_mindate(filtered_df, filters).date()
    max_date = ppcalc.get_maxdate(filtered_df, filters).date()
    # use markdown to create headers and sub headers
    st.write("# Notes on Data, Data Preperation and Assumptions")
    st.write("## Notes on Data")
    st.write(f"* The data covers the period from {min_date} to {max_date}")
    st.write("## Data and Cleansing")
    st.write("* The data was cleaned and transformed using Python and Pandas.")
    st.write("* The first section of this dashboard provides an overview of "
             "the whole dataset.")
    st.write("* The second section provides a details of a subset of the data "
             "focusing on the")
    st.write("* Cash donations to Politcal Parties, excluding donations by "
             "the parties to other")
    st.write("* political actors and campaigns.  It also summarises the "
             "data to focus on the top")
    st.write("* parties creating summary groups for the rest.")
