import streamlit as st


def page4_body():
    """
    This function displays the content of Page two.
    """
    df = st.session_state.get("data", None)
    impermissible_donors_ct = df[df.DonationType != 'Impermissible Donor'].count()
    dubious_donation_actions_ct = df[df.DonationAction].count()
    blank_received_date_ct = df[df.ReceivedDate.isnull()].count()
    blank_regulated_entity_id_ct = df[df.RegulatedEntityId.isnull()].count()
    blank_donor_id_ct = df[df.DonorId.isnull()].count()
    blank_donor_name_ct = df[df.DonorName.isnull()].count()
    dubious_donors = impermissible_donors_ct + blank_donor_id_ct + blank_donor_name_ct
    dubious_donation_actions = impermissible_donors_ct + dubious_donation_actions_ct
    totalvaluedubiousdonations = df[
        (df["DonationType"] != "Impermissible Donor") |  # Use `|` for OR
        (df["DonationAction"].notnull()) |  # Correcting isvalue() (assuming you meant notnull)
        (df["ReceivedDate"].isnull()) |
        (df["RegulatedEntityId"].isnull()) |
        (df["DonorId"].isnull()) |
        (df["DonorName"].isnull())
        ]["Value"].sum()
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
