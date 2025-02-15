def dubiousdonations_body():
    """
    Displays the content of the Donations by Political Party page.
    """
    import streamlit as st
    import calculations as ppcalc
    import datetime as dt
    import Visualisations as vis

    def format_number(value):
        if value >= 1_000_000:
            return f"{value / 1_000_000:,.1f}M"
        elif value >= 10_000:
            return f"{value / 1_000:,.1f}k"
        else:
            return f"{value:,.2f}"

    # Load dataset from session state
    df = st.session_state.get("data_clean", None)

    # Get min and max dates from the dataset
    min_date = ppcalc.get_mindate(df).date()
    max_date = ppcalc.get_maxdate(df).date()

    # Add a date range slider to filter by received date
    date_range = st.slider(
        "Select Date Range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )

    # Extract start and end dates from the slider
    start_date, end_date = date_range
    start_date = dt.datetime.combine(start_date, dt.datetime.min.time())
    end_date = dt.datetime.combine(end_date, dt.datetime.max.time())

    # Filter by date range
    date_filter = (((df["ReceivedDate"] >= start_date) & (df["ReceivedDate"] <= end_date)) | (df["ReceivedDate"] == "1900-01-01 00:00:00"))
    # Create a mapping of RegulatedEntityName -> RegulatedEntityId
    entity_mapping = dict(zip(df["RegulatedEntityName"], df["RegulatedEntityId"]))

    # Add "All" as an option and create a dropdown that displays names but returns IDs
    selected_entity_name = st.selectbox("Filter by Regulated Entity", ["All"] + sorted(entity_mapping.keys()))

    # Get the corresponding ID for filtering
    selected_entity_id = entity_mapping.get(selected_entity_name, None)

    # Apply filters
    filters = {"RegulatedEntityId": selected_entity_id} if selected_entity_name != "All" else None

    # Apply filters to the dataset
    filtered_df = df[date_filter]
    if filters:
        filtered_df = filtered_df[filtered_df["RegulatedEntityId"] == filters["RegulatedEntityId"]]

    # Call each function separately with the selected filter
    blank_received_date_ct = ppcalc.get_blank_received_date_ct(filtered_df, filters)
    blank_regulated_entity_id_ct = ppcalc.get_blank_regulated_entity_id_ct(filtered_df, filters)
    dubious_donors = ppcalc.get_dubious_donors_ct(filtered_df, filters)
    dubious_donation_actions = ppcalc.get_dubious_donation_actions(filtered_df, filters)
    total_value_dubious_donations = ppcalc.get_total_value_dubious_donations(filtered_df, filters)
    dubious_percent_of_value = (total_value_dubious_donations / ppcalc.get_value_total(filtered_df, filters)) * 100
    dubious_percent_of_donors = (dubious_donors / ppcalc.get_donors_ct(filtered_df, filters)) * 100
    dubious_percent_of_donation_actions = (dubious_donation_actions / ppcalc.get_donations_ct(filtered_df, filters)) * 100

    # Format text
    st.write("# Donations Identified as Potentially Questionable")
    st.write("## Explanation")
    st.write("* Certain Political Donations represent funds either "
             "donated by donors who are not allowed to donate to UK Political Parties or"
             "are perceived to have been made with an aim to gain influence or in a "
             "manner that is not in line with the spirit of the law.")
    st.write("* These are identified by the regulator and marked in the data. "
             "These are often returned to the donor after investigation, but"
             "the number and nature of these donations can be indicative of the "
             "state of a party's happiness to interact with dubious people and entities.")
    st.write("## Topline Figures")
    if dubious_donors >= 1:
        st.write(f"* During the period of the data, there were {dubious_donors} donors identified as dubious.")
        st.write(f"* These donors represented {dubious_percent_of_donors:.2f}% of donors to the regulated entity.")
    else:
        st.write("* No donations from dubious donors were identified.")
    if dubious_donation_actions >= 1:
        st.write(f"* There were {dubious_donation_actions} donations that were identified as of questionable nature.")
        st.write(f"* These donations represented {dubious_percent_of_donation_actions:.2f}% of all donations made to the entity.")
    if blank_received_date_ct >= 1:
        st.write(f"* {blank_received_date_ct} donations had no recorded date.")
    if blank_regulated_entity_id_ct >= 1:
        st.write(f"* {blank_regulated_entity_id_ct} donations had no recorded "
                 "regulated entity.")
    if total_value_dubious_donations >= 1:
        st.write(f"* All these had a value of £{format_number(total_value_dubious_donations)} and represented {dubious_percent_of_value:.2f}% in value of all donations.")
    st.write("---")
    # Add a visualization in col2 showing the share of all donations by year by RegulatedEntityType
    st.write("### Dubious Donations by Year and Nature")
    filtered_df = filtered_df[filtered_df["DubiousData"] == 1]
    if filtered_df.empty:
        st.write("No data available for the selected filters.")
        return
    vis.plot_donations_by_year(filtered_df, XValues="YearReceived", YValue="Value", GGroup="NatureOfDonation", XLabel="Year", YLabel="Total Value (£)", Title="Dubious Donations by Year and Nature")
    st.write("## Next Steps")
    # Display the filtered data (Optional)
    filtered_df = filtered_df[["ReceivedDate",
                               "DonorName",
                               "Value",
                               "DonationAction",
                               "DonationType",
                               "RegulatedDoneeType",
                               "NatureOfDonation",
                               "DonorStatus",
                               "DubiousData"]].query("DubiousData == 1")
    if not filtered_df.empty:
        st.write("## Filtered Data")
        st.write(filtered_df)
