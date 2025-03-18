import streamlit as st


def introduction_body():
    """
    This function displays the content of Page one.
    """

    # format text
    st.write('### Introduction')
    st.write("* This dashboard is a simple tool to provide insights into "
             "Political donations in the United Kingdom.")
    st.write("* The first section of this dashboard provides an overview of "
             "the whole dataset.")
    st.write("* The Second section provides information "
             "of cash donations made "
             "to Political Parties during the period.  This is the largest "
             "category of donations in the dataset.")
    st.write("* The Third section provides details of a subset of the data "
             "focusing on the Non Cash donations to Politcal Parties.")
    st.write("* The Fourth section provides a summary of Public Funds donated "
             "to Political Partys.")
    st.write("* The Fifth section provides a look at donations from Bequests.")
    st.write("* The Sixth section covers donations from Corporate Entities, "
             "Limited Liability Partnerships and Unincorporated Associations.")
    st.write("* The Seventh section lookgs at donations made as Sponsorships. "
             " These come from various sources and are not always financial.")
    st.write("* The Eighth section provides details of Visits"
             " made by Political "
              "Entities that were funded by a third party.")
    st.write("* The Ninth section provides details of donations that were "
             "made by Dubioud Donors that have been identified as such by the "
             "Regulatory, it also includes large aggregated donations from "
             "Unregulated entities.")
    st.write("* In the tenth section, we look at donations that"
             " were identified as "
             "dubious in nature, this can be due to missing information or "
             "donations where the donor can not be identified. "
             " Not all of these "
             "are dubious, but they would need investigation to confirm their "
             "status and so a better classification is Possibly Dubious.")
    st.write("* The Eleventh section provides a way to look at"
             " donations made to "
             "specific Regulated Entities, and provides details"
             " on all donations received.")
    st.write("* The Twelfth section is a narative on the data"
             " and how it was manipulated, "
             "cleaned and prepared for analysis.  Along with any"
             " assumptions and links "
             "to the underlying code and related sites.")
    st.write("* The login and logout are for maintenance purposes only.")
    st.write("---")
# End of introduction.py
# PATH: app_pages/headlinefigures.py
