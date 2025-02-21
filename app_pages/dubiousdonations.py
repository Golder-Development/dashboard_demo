def dubiousdonations_body():
    """
    Displays the content of the Donations by Political Party page.
    """
    import streamlit as st
    import components.calculations as ppcalc
    import components.Visualisations as vis

    # Page Title
    st.write("## Dubious Donations to ")
    st.write("## UK Regulated Political Entities")
    # Load dataset from session state
    df = st.session_state.get("data_clean", None)
    # filters = {}
    # Get min and max dates from the dataset
    min_date = ppcalc.get_mindate(df).date()
    max_date = ppcalc.get_maxdate(df).date()

    # Extract start and end dates from the slider
    start_date = min_date
    end_date = max_date

    # Apply entity filter to dataset
    filtered_df2 = df
    # Call each function separately with the selected date and entity filter
    total_value_of_donations = ppcalc.get_value_total(filtered_df2)
    total_count_of_donors = ppcalc.get_donors_ct(filtered_df2)
    total_count_of_donations = ppcalc.get_donations_ct(filtered_df2)
    blank_received_date_ct = ppcalc.get_blank_received_date_ct(filtered_df2)
    blank_regulated_entity_id_ct = (
        ppcalc.get_blank_regulated_entity_id_ct(filtered_df2)
        )
    dubious_donors = ppcalc.get_dubious_donors_ct(filtered_df2)
    dubious_donors_value = ppcalc.get_dubious_donors_value(filtered_df2)
    dubious_donation_actions = (
        ppcalc.get_dubious_donation_actions(filtered_df2)
        )
    total_value_dubious_donations = (
        ppcalc.get_dubious_donation_value(filtered_df2)
        )
    dubious_donors_percent_of_value = (
        ((dubious_donors_value / total_value_of_donations) * 100)
        if total_value_of_donations > 0 else 0
        )
    dubious_percent_of_value = (
        ((total_value_dubious_donations / total_value_of_donations) * 100)
        if total_value_of_donations > 0 else 0
        )
    dubious_percent_of_donors = (
        ((dubious_donors / total_count_of_donors) * 100)
        if total_count_of_donors > 0 else 0
        )
    dubious_percent_of_donation_actions = (
        ((dubious_donation_actions / total_count_of_donations) * 100)
        if total_count_of_donations > 0 else 0
        )
    returned_donations = ppcalc.get_returned_donations_ct(filtered_df2)
    returned_donations_value = (
        ppcalc.get_returned_donations_value(filtered_df2)
        )
    returned_donations_percent_value = (
        ((returned_donations_value / total_value_dubious_donations) * 100)
        if total_value_dubious_donations > 0 else 0
        )
    returned_donations_percent_donations = (
        ((returned_donations / dubious_donation_actions) * 100)
        if dubious_donation_actions > 0 else 0
        )
    aggregated_donations = (
        ppcalc.get_donations_ct(
            filtered_df2,
            filters={"DonationType": "Aggregated donations"})
    )
    aggregated_donations_value = (
        ppcalc.get_value_total(
            filtered_df2,
            filters={"DonationType": "Aggregated donations"})
    )
    aggregated_percent_of_donation_actions = (
        ((aggregated_donations / total_count_of_donations) * 100)
        if total_count_of_donations > 0
        else 0
    )
    aggregated_percent_of_value = (
        ((aggregated_donations_value / total_value_of_donations) * 100)
        if total_value_of_donations > 0
        else 0
    )
    donated_visits = (
        ppcalc.get_donations_ct(
            filtered_df2,
            filters={"DonationType": "Visit"})
    )
    donated_visits_value = (
        ppcalc.get_value_total(filtered_df2, filters={"DonationType": "Visit"})
    )
    donated_visits_percent_of_donation_actions = (
        ((donated_visits / total_count_of_donations) * 100)
        if total_count_of_donations > 0
        else 0
    )
    donated_visits_percent_of_value = (
        ((donated_visits_value / total_value_of_donations) * 100)
        if total_value_of_donations > 0
        else 0
    )
    # Format text
    st.write("### Explanation")
    st.write(
        "* Certain Political Donations represent funds either donated "
        "by donors who are not allowed to donate to UK Political Parties or"
        "are perceived to have been made with an aim to gain influence or in a"
        " manner that is not in line with the spirit of the law.")
    st.write(
        "* These are identified by the regulator and marked in the data. "
        "These are often returned to the donor after investigation, but"
        "the number and nature of these donations can be indicative of the "
        "state of a party's happiness to interact with dubious people and"
        " entities.")
    st.write("* These figures also include aggregated donations where "
             "individual donors can not be identified, these may not "
             "be from dubious sources or of dubious nature, but the "
             "lack of transparency means that they represent a risk "
             "to the integrity of the political system.")
    st.write("### Topline Figures")
    if dubious_donors >= 1:
        st.write(
            f"* Between {start_date} and {end_date},"
            f" there were {dubious_donors} donors identified as dubious."
            f" These donors represented {dubious_percent_of_donors:.2f}%"
            " of donors to regulated entities,"
            f" and includes Impremissible Donors, Unidentified Donors "
            f" and Aggregated Donors.  They donated a total of "
            f"£{ppcalc.format_number(dubious_donors_value)},"
            f" which represented {dubious_donors_percent_of_value:.2f}%"
            " of the total value of donations made in the period.")
    else:
        st.write("* No donations from dubious donors were identified.")
    if dubious_donation_actions >= 1:
        st.write(
            f"* There were {dubious_donation_actions:,.0f} donations that were"
            " identified as of questionable nature."
            f" These donations represented"
            f" {dubious_percent_of_donation_actions:.2f}% "
            "of all donations made in the period.")
    if blank_received_date_ct >= 1:
        st.write(f"* {blank_received_date_ct} donations had no recorded date.")
    if blank_regulated_entity_id_ct >= 1:
        st.write(f"* {blank_regulated_entity_id_ct} donations had no recorded "
                 "regulated entity.")
    if total_value_dubious_donations >= 1:
        st.write(
            f"* Of these donations {returned_donations} or"
            f" {returned_donations_percent_donations:.2f}% "
            "were returned to the donor,"
            f"representing £{ppcalc.format_number(returned_donations_value)}"
            f" or {returned_donations_percent_value:.2f}% of the total "
            "value of dubious donations.")
    if aggregated_donations >= 1:
        st.write(
            f"* There were {aggregated_donations} aggregated donations,"
            f" representing {aggregated_percent_of_donation_actions:.2f}%"
            "of all donation actions."
            f" The total value of these aggregated donations was"
            f" £{ppcalc.format_number(aggregated_donations_value)},"
            f" representing {aggregated_percent_of_value:.2f}% of "
            "the total value of all donations.")
    if donated_visits >= 1:
        st.write(
            f"* There were {donated_visits:,.0f} visits donated to regulated"
            " entities, representing "
            f"{donated_visits_percent_of_donation_actions:.2f}% of all "
            "donation actions. The total value of these visits was "
            f" £{ppcalc.format_number(donated_visits_value)}, representing "
            f" {donated_visits_percent_of_value:.2f}% of the total value of "
            "all donations.")
    st.write("---")
    st.write("### Visuals")
    # Display the filtered data (Optional)
    col1, col2 = st.columns(2)
    with col1:
        if not filtered_df2.empty:
            filtered_df3 = filtered_df2.query("DubiousData >= 1")
            vis.plot_bar_line_by_year(
                filtered_df3,
                XValues="YearReceived",
                YValue="Value",
                GGroup="DonationType",
                XLabel="Year",
                YLabel="Total Value (£)",
                y_scale="linear",
                Title="Dubious Donations by Year and Nature",
                widget_key="dubious_donations_by_year_and_nature")
        else:
            st.write("No data to display")
    with col2:
        if not filtered_df2.empty:
            filtered_df3 = filtered_df2.query("DubiousData >= 1")
            vis.plot_bar_line_by_year(
                filtered_df3,
                XValues="YearReceived",
                YValue="Value",
                GGroup="RegEntity_Group",
                XLabel="Year",
                YLabel="Total Value (£)",
                Title="Dubious Donations by Year and Regulated Entity",
                use_custom_colors=True,
                y_scale="linear",
                ChartType="line",
                widget_key="dubious_donations_by_year_and_entity")
        else:
            st.write("No data to display")
    if not filtered_df2.empty:
        st.write("### Scrollable table of identified donations")
        filtered_df3 = filtered_df3[["ReceivedDate",
                                     "RegulatedEntityName",
                                     "DonorName",
                                     "Value",
                                     "DonationAction",
                                     "DonationType",
                                     "RegulatedDoneeType",
                                     "NatureOfDonation",
                                     "DonorStatus",
                                     "DubiousData"]].query("DubiousData >= 1")
        st.write(filtered_df3)
    st.write("### Click on Visuals to expand the graphs."
             "Tables are scrollable")
    # add a link to the streamlit dubiousdonationsbyDonor screen to allow
    # users to explore the data further
    st.write("### Explore the data further using the Dubious Donations by"
             " Donor link in the menu")
    st.write(
        "### or Check out Transparency International's"
        "[Recent Publication]"
        "(https://www.transparency.org.uk/news/new-research-reveals-almost-ps1-every-ps10-political-donations-comes-unknown-or-questionable)"
        "for more information on donations to UK Political Parties.")
