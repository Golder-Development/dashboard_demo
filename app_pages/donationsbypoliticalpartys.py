def donationsbypoliticalpartys_body():
    """
    Displays the content of the Donations by Political Party page.
    """
    import streamlit as st
    import components.calculations as ppcalc

    df = st.session_state.get("data", None)
    if df is None:
        st.error("No data available. Please check if the dataset is loaded.")
        return

    # Example: Get filtered results for a specific party (if needed)
    selected_party = st.selectbox("Filter by Political Party", ["All"] +
                                  sorted(df["RegulatedEntityId"].unique()))
    filters = {"RegulatedEntityId": selected_party} if selected_party != "All"\
        else None

    # Call each function separately with the selected filter
    # impermissible_donors_ct = ppcalc.get_impermissible_donors_ct(df, filters)
    # dubious_donation_actions_ct = ppcalc.get_dubious_donation_actions_ct(df,
    # filters)
    blank_received_date_ct = ppcalc.get_blank_received_date_ct(df, filters)
    blank_regulated_entity_id_ct = (
        ppcalc.get_blank_regulated_entity_id_ct(df, filters))
    # blank_donor_id_ct = ppcalc.get_blank_donor_id_ct(df, filters)
    # blank_donor_name_ct = ppcalc.get_blank_donor_name_ct(df, filters)
    dubious_donors = ppcalc.get_dubious_donors_ct(df, filters)
    dubious_donation_actions = ppcalc.get_dubious_donation_actions(df, filters)
    total_value_dubious_donations = (
        ppcalc.get_dubious_donation_value(df, filters))

    st.write("# Donations Where a Political Party is the Donor")
    st.write("## Explaination")
    st.write("* Certain Political Donations represent funds either "
             "donated to other Political Parties or regional Party Branches.")
    st.write("* These are identified by the regulator and marked in the data. "
             "These in part artificially inflate the value of donations made,"
             "and as such need to be looked at seperately.")
    st.write("## Topline Figures")
    st.write(f"* During the period of the data, there were "
             f"{dubious_donors} donations from dubious donors.")
    st.write(f"* There were {dubious_donation_actions} donations that were "
             "identified as of questionable nature.")
    st.write(f"* {blank_received_date_ct} donations had no recorded date.")
    st.write(f"* {blank_regulated_entity_id_ct} donations had no recorded "
             "regulated entity.")
    st.write(f"* All these had a value of £{total_value_dubious_donations}")
    st.write("---")
