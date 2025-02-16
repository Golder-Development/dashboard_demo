import streamlit as st



def introduction_body():
    """
    This function displays the content of Page one.
    """

    # format text
    st.write("## Political Donation Analysis")
    st.write('### Introduction')
    st.write("* This dashboard is a simple tool to provide insights into "
             "Political donations in the United Kingdom.")

    st.write("* The first section of this dashboard provides an overview of "
             "the whole dataset.")
    st.write("* The Second section provides a information of donations that are "
                "considered dubious.  This includes donations with missing dates, "
                "missing donor names and donations that are considered to be from "
                "dubious donors or where the donor is not identifiable. ")
    st.write("* The Third section provides a details of a subset of the data "
             "focusing on the Cash donations to Politcal Parties, excluding donations by "
             "the parties to other political actors and campaigns.  It also summarises the "
             "data to focus on the top parties creating summary groups for the rest.")
