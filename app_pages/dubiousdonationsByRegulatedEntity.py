def dubiousdonationsByDonor_body():
    """
    Displays the content of the Donations by Political Party page.
    """
    import streamlit as st
    import calculations as ppcalc
    import datetime as dt
    import Visualisations as vis
    import pandas as pd

    def format_number(value):
        if value >= 1_000_000:
            return f"{value / 1_000_000:,.1f}M"
        elif value >= 10_000:
            return f"{value / 1_000:,.1f}k"
        else:
            return f"{value:,.2f}"
    ## Page Title
    st.write("## Investigate Dubious Donations by Period and Regulated Entity")
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
    # Apply filters to the dataset
    filtered_df = df[date_filter]
    # Call each function separately with the selected date filter for benchmarking
    total_value_of_donations = ppcalc.get_value_total(filtered_df)
    total_count_of_donors = ppcalc.get_donors_ct(filtered_df)
    total_count_of_donations = ppcalc.get_donations_ct(filtered_df)
    # bm_blank_received_date_ct = ppcalc.get_blank_received_date_ct(filtered_df)
    # bm_blank_regulated_entity_id_ct = ppcalc.get_blank_regulated_entity_id_ct(filtered_df)
    bm_dubious_donors = ppcalc.get_dubious_donors_ct(filtered_df)
    bm_dubious_donation_actions = ppcalc.get_dubious_donation_actions(filtered_df)
    bm_total_value_dubious_donations = ppcalc.get_total_value_dubious_donations(filtered_df)
    bm_dubious_percent_of_value = (bm_total_value_dubious_donations / ppcalc.get_value_total(filtered_df) * 100) if ppcalc.get_value_total(filtered_df) > 0 else 0
    bm_dubious_percent_of_donors = ((bm_dubious_donors / ppcalc.get_donors_ct(filtered_df)) * 100) if ppcalc.get_donors_ct(filtered_df) > 0 else 0
    bm_dubious_percent_of_donation_actions = ((bm_dubious_donation_actions / ppcalc.get_donations_ct(filtered_df)) * 100) if ppcalc.get_donations_ct(filtered_df) > 0 else 0
    bm_returned_donations = ppcalc.get_returned_donations_ct(filtered_df)
    bm_returned_donations_value = ppcalc.get_returned_donations_value(filtered_df)
    bm_returned_donations_percent_value = ((bm_returned_donations_value / bm_total_value_dubious_donations) * 100) if bm_total_value_dubious_donations > 0 else 0
    bm_returned_donations_percent_donations = ((bm_returned_donations / bm_dubious_donation_actions) * 100) if bm_dubious_donation_actions > 0 else 0
    bm_aggregated_donations = ppcalc.get_donations_ct(filtered_df, filters={"DonationType": "Total value of donations not reported individually"})
    bm_aggregated_donations_value = ppcalc.get_value_total(filtered_df, filters={"DonationType": "Total value of donations not reported individually"})
    bm_aggregated_percent_of_donation_actions = ((bm_aggregated_donations / total_count_of_donations) * 100) if total_count_of_donations > 0 else 0
    bm_aggregated_percent_of_value = ((bm_aggregated_donations_value / total_value_of_donations) * 100) if total_value_of_donations > 0 else 0
    bm_donated_visits = ppcalc.get_donations_ct(filtered_df, filters={"DonationType": "Visit"})
    bm_donated_visits_value = ppcalc.get_value_total(filtered_df, filters={"DonationType": "Visit"})
    bm_donated_visits_percent_of_donation_actions = ((bm_donated_visits / total_count_of_donations) * 100) if total_count_of_donations > 0 else 0
    bm_donated_visits_percent_of_value = ((bm_donated_visits_value / total_value_of_donations) * 100) if total_value_of_donations > 0 else 0

    min_date = ppcalc.get_mindate(filtered_df).date()
    max_date = ppcalc.get_maxdate(filtered_df).date()

    # Create a mapping of RegulatedEntityName -> RegulatedEntityId
    entity_mapping = dict(zip(df["RegulatedEntityName"], df["RegulatedEntityId"]))

    # Add "All" as an option and create a dropdown that displays names but returns IDs
    selected_entity_name = st.selectbox("Filter by Regulated Entity", ["All"] + sorted(entity_mapping.keys()))

    # Get the corresponding ID for filtering
    selected_entity_id = entity_mapping.get(selected_entity_name, None)

    # Apply filters
    filters = {"RegulatedEntityId": selected_entity_id} if selected_entity_name != "All" else None

    # Apply entity filter to dataset
    if filters:
        filtered_df2 = filtered_df[filtered_df["RegulatedEntityId"] == filters["RegulatedEntityId"]]
    else:
        filtered_df2 = filtered_df
    # Call each function separately with the selected date and entity filter

    blank_received_date_ct = ppcalc.get_blank_received_date_ct(filtered_df2)
    blank_regulated_entity_id_ct = ppcalc.get_blank_regulated_entity_id_ct(filtered_df2)
    dubious_donors = ppcalc.get_dubious_donors_ct(filtered_df2)
    dubious_donation_actions = ppcalc.get_dubious_donation_actions(filtered_df2)
    total_value_dubious_donations = ppcalc.get_total_value_dubious_donations(filtered_df2)
    dubious_percent_of_value = ((total_value_dubious_donations / total_value_of_donations) * 100) if total_value_of_donations > 0 else 0
    dubious_percent_of_donors = ((dubious_donors / total_count_of_donors) * 100) if total_count_of_donors > 0 else 0
    dubious_percent_of_donation_actions = ((dubious_donation_actions / total_count_of_donations) * 100) if total_count_of_donations > 0 else 0
    returned_donations = ppcalc.get_returned_donations_ct(filtered_df2)
    returned_donations_value = ppcalc.get_returned_donations_value(filtered_df2)
    returned_donations_percent_value = ((returned_donations_value / total_value_dubious_donations) * 100) if total_value_dubious_donations > 0 else 0
    returned_donations_percent_donations = ((returned_donations / dubious_donation_actions) * 100) if dubious_donation_actions > 0 else 0
    aggregated_donations = ppcalc.get_donations_ct(filtered_df2, filters={"DonationType": "Total value of donations not reported individually"})
    aggregated_donations_value = ppcalc.get_value_total(filtered_df2, filters={"DonationType": "Total value of donations not reported individually"})
    aggregated_percent_of_donation_actions = ((aggregated_donations / total_count_of_donations) * 100) if total_count_of_donations > 0 else 0
    aggregated_percent_of_value = ((aggregated_donations_value / total_value_of_donations) * 100) if total_value_of_donations > 0 else 0
    donated_visits = ppcalc.get_donations_ct(filtered_df2, filters={"DonationType": "Visit"})
    donated_visits_value = ppcalc.get_value_total(filtered_df2, filters={"DonationType": "Visit"})
    donated_visits_percent_of_donation_actions = ((donated_visits / total_count_of_donations) * 100) if total_count_of_donations > 0 else 0
    donated_visits_percent_of_value = ((donated_visits_value / total_value_of_donations) * 100) if total_value_of_donations > 0 else 0
    # Format text
    st.write(f"### Summary of Dubious Donations for {selected_entity_name}")
    if dubious_donors >= 1:
        st.write(f"* Between {start_date} and {end_date}, there were {dubious_donors} donors identified as dubious."
                 f" These donors represented {dubious_percent_of_donors:.2f}% of donors to regulated entities,"
                 " and includes Impremissible Donors and Unidentified Donors.")
    else:
        st.write("* No donations from dubious donors were identified.")
    if dubious_donation_actions >= 1:
        st.write(f"* There were {dubious_donation_actions} donations that were identified as of questionable nature."
                 f" These donations represented {dubious_percent_of_donation_actions:.2f}% of all donations made in the period."
                 f" These had a combined value of £{format_number(total_value_dubious_donations)} and represented {dubious_percent_of_value:.2f}% in value of all donations.")
    if blank_received_date_ct >= 1:
        st.write(f"* {blank_received_date_ct} donations had no recorded date.")
    if blank_regulated_entity_id_ct >= 1:
        st.write(f"* {blank_regulated_entity_id_ct} donations had no recorded "
                 "regulated entity.")
    if total_value_dubious_donations >= 1:
        st.write(f"* Of these donations {returned_donations} or {returned_donations_percent_donations:.2f}% were returned to the donor,"
                 f"representing £{format_number(returned_donations_value)} or {returned_donations_percent_value:.2f}% of the total value of dubious donations.")
    if aggregated_donations >= 1:
        st.write(f"* There were {aggregated_donations} aggregated donations, representing {aggregated_percent_of_donation_actions:.2f}% of all donation actions."
                 f" The total value of these aggregated donations was £{format_number(aggregated_donations_value)}, representing {aggregated_percent_of_value:.2f}% of the total value of all donations.")
    if donated_visits >= 1:
        st.write(f"* There were {donated_visits} visits donated to regulated entities, representing {donated_visits_percent_of_donation_actions:.2f}% of all donation actions."
                 f" The total value of these visits was £{format_number(donated_visits_value)}, representing {donated_visits_percent_of_value:.2f}% of the total value of all donations.")
    st.write("---")
    st.write("### Benchmarked Figures")
    if filters:
        st.write("* The benchmarked figures are based on the selected date range and regulated entity.")
        # Table comparing figures for the selected entity with the benchmarked figures for the whole dataset
        df = pd.DataFrame(
            {
                "Measure": [
                    "Perc of Donors",
                    "Perc of Donations",
                    "Perc of Value Donated",
                    "Perc of Donations Returned",
                    "Perc Value of Donations Returned",
                    "Perc of Donations identified as Aggregated",
                    "Perc of Donated Value identified as Aggregated",
                    "Donated Visits as Perc of Donations",
                    "Value of Donated Visits as Perc of Value Donated"
                ],
                selected_entity_name: [
                    f"{dubious_percent_of_donors:.2f}%",
                    f"{dubious_percent_of_donation_actions:.2f}%",
                    f"{dubious_percent_of_value:.2f}%",
                    f"{returned_donations_percent_donations:.2f}%",
                    f"{returned_donations_percent_value:.2f}%",
                    f"{aggregated_percent_of_donation_actions:.2f}%",
                    f"{aggregated_percent_of_value:.2f}%",
                    f"{donated_visits_percent_of_donation_actions:.2f}%",
                    f"{donated_visits_percent_of_value:.2f}%"
                ],
                "Benchmarked": [
                    f"{bm_dubious_percent_of_donors:.2f}%",
                    f"{bm_dubious_percent_of_donation_actions:.2f}%",
                    f"{bm_dubious_percent_of_value:.2f}%",
                    f"{bm_returned_donations_percent_donations:.2f}%",
                    f"{bm_returned_donations_percent_value:.2f}%",
                    f"{bm_aggregated_percent_of_donation_actions:.2f}%",
                    f"{bm_aggregated_percent_of_value:.2f}%",
                    f"{bm_donated_visits_percent_of_donation_actions:.2f}%",
                    f"{bm_donated_visits_percent_of_value:.2f}%"
                ],
                "Difference": [
                    dubious_percent_of_donors - bm_dubious_percent_of_donors,
                    dubious_percent_of_donation_actions - bm_dubious_percent_of_donation_actions,
                    dubious_percent_of_value - bm_dubious_percent_of_value,
                    returned_donations_percent_donations - bm_returned_donations_percent_donations,
                    returned_donations_percent_value - bm_returned_donations_percent_value,
                    aggregated_percent_of_donation_actions - bm_aggregated_percent_of_donation_actions,
                    aggregated_percent_of_value - bm_aggregated_percent_of_value,
                    donated_visits_percent_of_donation_actions - bm_donated_visits_percent_of_donation_actions,
                    donated_visits_percent_of_value - bm_donated_visits_percent_of_value
                ],
            }
        )

        def color_negative_red(val):
            color = 'green' if val[0] == "-" else 'black' if val[0] == 0 else 'red'
            return f'color: {color}'

        df["Difference"] = df["Difference"].map(lambda x: f"{x:.2f}%")
        styled_df = df.style.map(color_negative_red, subset=["Difference"]).hide(axis='index')
        st.table(styled_df)
    else:
        st.write("* No benchmarking as analysis is for entire dataset, so variance to average is not relevant.")
    st.write("### Visuals")
    if not filtered_df2.empty:
        filtered_df2 = filtered_df2.query("DubiousData >=1")
        vis.plot_donations_by_year(filtered_df2, XValues="YearReceived", YValue="Value", GGroup="DonationType", XLabel="Year", YLabel="Total Value (£)", Title="Dubious Donations by Year and Nature")
        # Display the filtered data (Optional)
    filtered_df3 = filtered_df2[["ReceivedDate",
                                 "DonorName",
                                 "Value",
                                 "DonationAction",
                                 "DonationType",
                                 "RegulatedDoneeType",
                                 "NatureOfDonation",
                                 "DonorStatus",
                                 "DubiousData"]].query("DubiousData >= 1")
    if not filtered_df3.empty:
        st.write("### Scrollable table of identified donations")
        st.write(filtered_df3)
    st.write("### Click on Visuals to expand the graphs. Tables are scrollable")
