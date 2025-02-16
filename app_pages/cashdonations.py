def cashdonations_body():
    """
    Displays the content of the Cash Donations by Political Party page.
    """
    import streamlit as st
    import calculations as ppcalc

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
    # filtered_df = df[date_filter]
    filtered_df = df[df['DonationType' == 'cash']].copy()
    if filters:
        filtered_df = filtered_df[filtered_df["RegulatedEntityId"] == filters["RegulatedEntityId"]]

    # Call each function separately with the selected filter
    unique_donors = ppcalc.get_donors_ct(filtered_df, filters)
    total_value_donations = ppcalc.get_value_total(filtered_df, filters)
    mean_value_donations = ppcalc.get_value_mean(filtered_df, filters)
    unique_donations = ppcalc.get_donations_ct(filtered_df, filters)
    unique_regulated_entities = ppcalc.get_regentity_ct(filtered_df, filters)
    min_date = ppcalc.get_mindate(filtered_df, filters)
    max_date = ppcalc.get_maxdate(filtered_df, filters)

    st.write("# Cash Donations to Political Parties")
    st.write("## Explaination")
    st.write("* The majority of donations to political parties are in cash."
             "These vary from small donations from individuals, to larger aggregated"
             "donations from multiple donors, and include donations from trade unions,"
             "business and bequests.")
    st.write("* These are identified by the regulator and marked in the data. "
             "This page provides a summary of the cash donations to political parties.")
    st.write("## Topline Figures")
    st.write(f"* During the period between {min_date} and {max_date}, there were "
             f"{unique_donations} cash donations made to {unique_regulated_entities}.")
    st.write(f"* These had a mean value of {mean_value_donations} and were made by {unique_donors} unique donors.")
    st.write(f"* All these had a value of £{total_value_donations}")
    st.write("---")
