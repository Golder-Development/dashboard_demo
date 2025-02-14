import streamlit as st


def page1_body():
    """
    This function displays the content of Page one.
    """
    st.write("# Political Donation Analysis")
    st.write('## Introduction')
    st.write("* This dashboard is a simple tool to provide insights into "
             "Political donations in the United Kingdom.")
    st.write("* This was built using Streamlit and Python following training "
             "from the Code Institute, on a Data Analytics and AI Course "
             "sponsored by the WMCA.")
    st.write("* The data was sourced from the Electoral Commission, Via "
             "https://data.world/vizwiz it covers data between 2001 and 2019")
    st.write("")
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
