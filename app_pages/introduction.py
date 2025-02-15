import streamlit as st


def introduction_body():
    """
    This function displays the content of Page one.
    """
    electoral_commission = "https://www.electoralcommission.org.uk/"
    # format text
    st.write("# Political Donation Analysis")
    st.write('## Introduction')
    st.write("* This dashboard is a simple tool to provide insights into "
             "Political donations in the United Kingdom.")
    st.write("* This was built using Streamlit and Python following training "
             "from the [Code Institute](%s)." % "https://codeinstitute.net/")
    st.write("* On a Data Analytics and AI Course sponsored by the [WMCA](%s)." % "https://www.wmca.org.uk/")
    st.write("* The data was sourced from the [Electoral Commission](%s)." % electoral_commission)
    st.write("* Having been initially extracted and compiled by https://data.world/vizwiz.")
    st.write("* The data is a snapshot of donations made to Political Parties ")
    st.write("")
