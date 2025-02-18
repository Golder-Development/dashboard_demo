import streamlit as st


def sponsorship_body():
    """
    This function displays the content of Page two.
    """
    sponsorship_df = st.session_state.get("data", None)

    st.write("# Donations from Dubious Sources")
    st.write("## Explaination of Dubious Donations")
    st.write("* Certain Political Donations are considered dubious, "
             "this can be due to the donor or the amount donated.")
    st.write("* These are identified by the regulator and marked in the data. "
             "For more information on which donations are such marked,"
             "Please refer to the notes on the Data and Manipulations page.")
    st.write("## Topline Figures")
    st.write(f"* During the period of the data, there were "
             f"{dubious_donors} donations from dubious donors.")
    st.write(f"* There were {dubious_donation_actions} donations that were "
             "identified as of questionable nature.")
    st.write(f"* {blank_received_date_ct} donations had no recorded date.")
    st.write(f"* {blank_regulated_entity_id_ct} donations had no recorded "
             "regulated entity.")
    st.write(f"* All these had a value of £{totalvaluedubiousdonations}")
    st.write("---")
