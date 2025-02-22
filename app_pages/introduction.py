import streamlit as st


def introduction_body():
    """
    This function displays the content of Page one.
    """

    # format text
    st.write("---")
    st.write("## Political Donation Analysis")
    st.write("---")
    st.write('### Introduction')
    st.write("* This dashboard is a simple tool to provide insights into "
             "Political donations in the United Kingdom.")
    st.write("* The first section of this dashboard provides an overview of "
             "the whole dataset.")
    st.write("* The Second section provides information of donations that are "
             "considered dubious.  This includes donations with missing dates,"
             " missing donor names and donations that are considered to be "
             "from dubious donors or where the donor is not identifiable. ")
    st.write("* The Third section provides details of a subset of the data "
             "focusing on the Cash donations to Politcal Parties, excluding"
             " donations by the parties to other political actors and "
             " campaigns.  It also summarises the data to focus on the top "
             " parties creating summary groups for the rest.")
    st.write("* The Fourth section provides a summary of sponsorships made "
             "to Political Partys.")
    st.write("* The Fifth section provides a look at the paid visits donated"
             " to Political Parties.")
    st.write("* The Sixth section provides a look at the activity levels of"
             " donors to Political Parties, and offers a way to look at"
             " the activity levels of particular donors to different parties.")
    st.write("* The Seventh section provides details on the data sources used"
             " how it was cleaned and prepared for analysis/visualization."
             " It also provides a link to the original data source,"
             " and outlines any assumptions made in the data preparation "
             " and analysis.")
    st.write("* You should be able to access the code through the github link"
             " at the top of the page.")
    st.write("---")
