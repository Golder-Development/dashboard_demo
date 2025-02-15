def dubiousdonations_body():
    """
    Displays the content of the Donations by Political Party page.
    """
    import streamlit as st
    import calculations as ppcalc
    import pandas as pd
    df = st.session_state.get("data", None)  # Load dataset from session state

    # # Ensure ReceivedDate is in datetime format
    # df["ReceivedDate"] = pd.to_datetime(df["ReceivedDate"], errors="coerce")

    # # Get min and max dates from the dataset
    # min_date = df["ReceivedDate"].min()
    # max_date = df["ReceivedDate"].max()

    # # Add a date range slider to filter by received date
    # date_range = st.slider(
    #     "Select Date Range",
    #     min_value=min_date,
    #     max_value=max_date,
    #     value=(min_date, max_date),
    #     format="YYYY-MM-DD"
    # )

    # # Extract start and end dates from the slider
    # start_date, end_date = date_range

    # # Filter by date range
    # date_filter = (df["ReceivedDate"] >= start_date) & (df["ReceivedDate"] <= end_date)

    # --- Dropdown for Regulated Entity ---
    # Create a mapping of RegulatedEntityName -> RegulatedEntityId
    entity_mapping = dict(zip(df["RegulatedEntityName"], df["RegulatedEntityId"]))

    # Add "All" as an option and create a dropdown that displays names but returns IDs
    selected_entity_name = st.selectbox("Filter by Regulated Entity", ["All"] + sorted(entity_mapping.keys()))

    # Get the corresponding ID for filtering
    selected_entity_id = entity_mapping.get(selected_entity_name, None)

    # Apply filters
    filters = {"RegulatedEntityId": selected_entity_id} if selected_entity_name != "All" else None

    # Apply filters to the dataset
    #filtered_df = df[date_filter]
    filtered_df = df.copy()
    if filters:
        filtered_df = filtered_df[filtered_df["RegulatedEntityId"] == filters["RegulatedEntityId"]]

    # Call each function separately with the selected filter
    # impermissible_donors_ct = ppcalc.get_impermissible_donors_ct(df, filters)
    # dubious_donation_actions_ct = ppcalc.get_dubious_donation_actions_ct(df, filters)
    blank_received_date_ct = ppcalc.get_blank_received_date_ct(filtered_df, filters)
    blank_regulated_entity_id_ct = ppcalc.get_blank_regulated_entity_id_ct(filtered_df, filters)
    # blank_donor_id_ct = ppcalc.get_blank_donor_id_ct(df, filters)
    # blank_donor_name_ct = ppcalc.get_blank_donor_name_ct(df, filters)
    dubious_donors = ppcalc.get_dubious_donors_ct(filtered_df, filters)
    dubious_donation_actions = ppcalc.get_dubious_donation_actions(filtered_df, filters)
    total_value_dubious_donations = ppcalc.get_total_value_dubious_donations(filtered_df, filters)

    st.write("# Donations Identified as Potentially Questionable")
    st.write("## Explaination")
    st.write("* Certain Political Donations represent funds either "
             "donated by donors who are not allowed to donate to UK Political Parties or"
             "are precieved to have been made with an aim to gain influence or in a "
             "manner that is not in line with the spirit of the law.")
    st.write("* These are identified by the regulator and marked in the data. "
             "These are often returned to the donor after investigation, but"
             "the number and nature of these donations can be indicative of the "
             "state of a party's happiness to interact with dubious people and entities.")
    st.write("## Topline Figures")
    st.write(f"* During the period of the data, there were "
             f"{dubious_donors} donations from dubious donors.")
    if dubious_donation_actions >= 1:
        st.write(f"* There were {dubious_donation_actions} donations that were "
                 "identified as of questionable nature.")
    if blank_received_date_ct >= 1:
        st.write(f"* {blank_received_date_ct} donations had no recorded date.")
    if blank_regulated_entity_id_ct >= 1:
        st.write(f"* {blank_regulated_entity_id_ct} donations had no recorded "
                 "regulated entity.")
    st.write(f"* All these had a value of £{total_value_dubious_donations}")
    st.write("---")
    
    # Display the filtered data (Optional)
    st.write(filtered_df)
