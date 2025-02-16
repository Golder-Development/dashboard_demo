def dubiousdonations_body():
    """
    Displays the content of the Donations by Political Party page.
    """
    import streamlit as st
    import calculations as ppcalc
    import Visualisations as vis

    def format_number(value):
        if value >= 1_000_000:
            return f"{value / 1_000_000:,.1f}M"
        elif value >= 10_000:
            return f"{value / 1_000:,.1f}k"
        else:
            return f"{value:,.2f}"
    ## Page Title
    st.write("## Dubious Donations to ")
    st.write("## UK Regulated Political Entities")
    # Load dataset from session state
    df = st.session_state.get("data_clean", None)
    filters= {}
    # Get min and max dates from the dataset
    min_date = ppcalc.get_mindate(df).date()
    max_date = ppcalc.get_maxdate(df).date()

    # Extract start and end dates from the slider
    start_date = min_date
    end_date = max_date

    # Apply filters to the dataset
    filtered_df = df
    # Call each function separately with the selected date filter for benchmarking
    # bm_blank_received_date_ct = ppcalc.get_blank_received_date_ct(filtered_df)
    # bm_blank_regulated_entity_id_ct = ppcalc.get_blank_regulated_entity_id_ct(filtered_df)
    # bm_dubious_donors = ppcalc.get_dubious_donors_ct(filtered_df)
    # bm_dubious_donation_actions = ppcalc.get_dubious_donation_actions(filtered_df)
    # bm_total_value_dubious_donations = ppcalc.get_total_value_dubious_donations(filtered_df)
    # bm_dubious_percent_of_value = (bm_total_value_dubious_donations / ppcalc.get_value_total(filtered_df) * 100) if ppcalc.get_value_total(filtered_df) > 0 else 0
    # bm_dubious_percent_of_donors = ((bm_dubious_donors / ppcalc.get_donors_ct(filtered_df)) * 100) if ppcalc.get_donors_ct(filtered_df) > 0 else 0
    # bm_dubious_percent_of_donation_actions = ((bm_dubious_donation_actions / ppcalc.get_donations_ct(filtered_df)) * 100) if ppcalc.get_donations_ct(filtered_df) > 0 else 0
    # bm_returned_donations = ppcalc.get_returned_donations_ct(filtered_df)
    # bm_returned_donations_value = ppcalc.get_returned_donations_value(filtered_df)
    # bm_returned_donations_percent_value = ((bm_returned_donations_value / bm_total_value_dubious_donations) * 100) if bm_total_value_dubious_donations > 0 else 0
    # bm_returned_donations_percent_donations = ((bm_returned_donations / bm_dubious_donation_actions) * 100) if bm_dubious_donation_actions > 0 else 0

    # Apply entity filter to dataset
    filtered_df2 = filtered_df
    # Call each function separately with the selected date and entity filter
    total_value_of_donations = ppcalc.get_value_total(filtered_df2)
    total_count_of_donors = ppcalc.get_donors_ct(filtered_df2)
    total_count_of_donations = ppcalc.get_donations_ct(filtered_df2)
    blank_received_date_ct = ppcalc.get_blank_received_date_ct(filtered_df2)
    blank_regulated_entity_id_ct = ppcalc.get_blank_regulated_entity_id_ct(filtered_df2)
    dubious_donors = ppcalc.get_dubious_donors_ct(filtered_df2)
    dubious_donation_actions = ppcalc.get_dubious_donation_actions(filtered_df2)
    total_value_dubious_donations = ppcalc.get_total_value_dubious_donations(filtered_df2)
    dubious_percent_of_value = ((total_value_dubious_donations / total_value_of_donations) * 100) if total_value_of_donations > 0 else 0
    dubious_percent_of_donors = ((dubious_donors / total_count_of_donors ) * 100) if total_count_of_donors> 0 else 0
    dubious_percent_of_donation_actions = ((dubious_donation_actions / total_count_of_donations) * 100) if total_count_of_donations> 0 else 0
    returned_donations = ppcalc.get_returned_donations_ct(filtered_df2)
    returned_donations_value = ppcalc.get_returned_donations_value(filtered_df2)
    returned_donations_percent_value = ((returned_donations_value / total_value_dubious_donations) * 100) if total_value_dubious_donations > 0 else 0
    returned_donations_percent_donations = ((returned_donations / dubious_donation_actions) * 100) if dubious_donation_actions > 0 else 0
    aggregated_donations = ppcalc.get_donations_ct(filtered_df2, filters={"DonationType": "Total value of donations not reported individually"})
    aggregated_donations_value = ppcalc.get_value_total(filtered_df2, filters={"DonationType": "Total value of donations not reported individually"})
    aggregated_percent_of_donation_actions = ((aggregated_donations / total_count_of_donations) * 100) if total_count_of_donations > 0 else 0
    aggregated_percent_of_value = ((aggregated_donations_value / total_value_of_donations) * 100) if total_value_of_donations > 0 else 0
    # Format text
    
    st.write("### Explanation")
    st.write("* Certain Political Donations represent funds either "
             "donated by donors who are not allowed to donate to UK Political Parties or"
             "are perceived to have been made with an aim to gain influence or in a "
             "manner that is not in line with the spirit of the law.")
    st.write("* These are identified by the regulator and marked in the data. "
             "These are often returned to the donor after investigation, but"
             "the number and nature of these donations can be indicative of the "
             "state of a party's happiness to interact with dubious people and entities.")
    st.write("* These figures also include aggregated donations where individual donors can not be identified,"
            "these may not be from dubious sources or of dubious nature, but the lack of transparency means that they"
            "represent a risk to the integrity of the political system.")
    st.write("### Topline Figures")
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
    st.write("---")
    st.write("### Visuals")
    vis.plot_donations_by_year(filtered_df2, XValues="YearReceived", YValue="Value", GGroup="DonationType", XLabel="Year", YLabel="Total Value (£)", Title="Dubious Donations by Year and Nature")
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
        st.write("### Scrollable table of identified donations")
        st.write(filtered_df)
    st.write("### Click on Visuals to expand the graphs. Tables are scrollable")
    # add a link to the streamlit dubiousdonationsbyDonor screen to allow users to explore the data further
    st.write("### Explore the data further using the Dubious Donations by Donor link in the menu")
    st.write("### or Check out Transparency International's [Recent Publication](https://www.transparency.org.uk/news/new-research-reveals-almost-ps1-every-ps10-political-donations-comes-unknown-or-questionable) for more information on donations to UK Political Parties.")
