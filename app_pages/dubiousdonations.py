import streamlit as st
import datetime as dt
from data.data_loader import load_cleaned_data
from components.filters import filter_by_date, apply_filters
from components.calculations import (compute_summary_statistics,
                                     get_mindate,
                                     get_maxdate,
                                     calculate_percentage,
                                     PLACEHOLDER_DATE,
                                     PLACEHOLDER_ID,
                                     format_number)
from components.Visualisations import (
                                       plot_bar_line_by_year)


def dubiousdonations_body():
    """
    Displays the content of the Donations by Political Party page.
    """
    # Page Title
    st.write("---")
    st.write("## Dubious Donations to "
             "UK Regulated Political Entities")
    st.write("---")
    # Load dataset
    cleaned_df = load_cleaned_data()
    if cleaned_df is None:
        st.error("No data found. Please upload a dataset.")
        return
    # Define filter condition
    current_target = {"DubiousData": [1, 2, 3, 4, 5]}
    target_label = "Dubious Donation"
    filters = {}
    # Get min and max dates from the dataset
    min_date = dt.datetime.combine(get_mindate(cleaned_df),
                                   dt.datetime.min.time())
    max_date = dt.datetime.combine(get_maxdate(cleaned_df),
                                   dt.datetime.min.time())
    # Extract start and end dates from the slider
    start_date, end_date = (
        dt.datetime.combine(min_date, dt.datetime.min.time()),
        dt.datetime.combine(max_date, dt.datetime.max.time())
        )
    # Apply filters apply date filter
    cleaned_d_df = filter_by_date(cleaned_df, start_date, end_date)
    # limit to target type of donation
    cleaned_c_d_df = apply_filters(cleaned_d_df,
                                   current_target)
    # all dubious donations
    tstats = compute_summary_statistics(cleaned_c_d_df, filters)
    # aggregated donations
    adstats = compute_summary_statistics(
        cleaned_c_d_df,
        {"DonationType": "Aggregated donations"})
    # visits
    dvstats = compute_summary_statistics(
        cleaned_c_d_df,
        {"DonationType": ["Visit", "visit"]})
    # returned and forfeited donations
    return_filters = {"DonationAction": ["Returned",
                                         "Forfeited",
                                         "returned",
                                         "forfeited"]}
    rfdstats = compute_summary_statistics(
        cleaned_c_d_df, return_filters)
    # blank received date
    blank_date_filters = {"ReceivedDate": PLACEHOLDER_DATE}
    brdstats = compute_summary_statistics(
        cleaned_c_d_df, blank_date_filters)
    # blank regulated entity data
    blank_reg_entity_filters = {"RegulatedEntityId": PLACEHOLDER_ID}
    bredstats = compute_summary_statistics(
        cleaned_c_d_df, blank_reg_entity_filters)
    # donated sponsorships
    sponsorship_filters = {"DonationType": ["Sponsorship", "sponsorship"],
                           "IsSponsorship": True}
    sponstats = compute_summary_statistics(
        cleaned_c_d_df, sponsorship_filters)
    # all data
    ostats = compute_summary_statistics(cleaned_d_df, filters)
    # output stats
    show_debug = False
    if show_debug:
        st.write("---")
        st.write('tstats', tstats)
        st.write('ostats', ostats)
        st.write('adstats', adstats)
        st.write('dvstats', dvstats)
        st.write('rfdstats', rfdstats)
        st.write('brdstats', brdstats)
        st.write('bredstats', bredstats)
        st.write('sponstats', sponstats)
        st.write("---")
    # Calculate the percentage of donations that are cash donations
    dubious_donors_percent_of_value = calculate_percentage(
        tstats["donors_ct"], ostats["donors_ct"])
    dubious_percent_of_value = calculate_percentage(
        tstats["value_total"], ostats["value_total"])
    dubious_percent_of_donors = calculate_percentage(
        tstats['donors_ct'], ostats["donors_ct"])
    dubious_percent_of_donation_actions = calculate_percentage(
        tstats["donations_ct"], ostats["donations_ct"])
    returned_donations_percent_value = calculate_percentage(
          rfdstats["value_total"], tstats["value_total"])
    returned_donations_percent_donations = calculate_percentage(
          rfdstats["donations_ct"], tstats["donations_ct"])
    aggregated_percent_of_donation_actions = calculate_percentage(
        adstats['donations_ct'], ostats['donations_ct'])
    aggregated_percent_of_value = calculate_percentage(
        adstats['value_total'], ostats['value_total'])
    donated_visits_percent_of_donation_actions = calculate_percentage(
        dvstats['donations_ct'], ostats['donations_ct'])
    donated_visits_percent_of_value = calculate_percentage(
        dvstats['value_total'], ostats['value_total'])
    min_date = get_mindate(cleaned_d_df).date()
    max_date = get_maxdate(cleaned_d_df).date()

    # Format text
    st.write(f"## Summary Statistics for {target_label},"
             f" from {min_date} to {max_date}")
    left, a, b, mid, c, right = st.columns(6)
    with left:
        st.metric(label=f"Total {target_label}",
                  value=f"£{tstats['value_total']:,.0f}")
    with a:
        st.metric(label=f"{target_label}%",
                  value=f"{dubious_percent_of_value:.2f}%")
    with b:
        st.metric(label=f"{target_label}",
                  value=f"{tstats['donations_ct']:,}")
    with mid:
        st.metric(label=f"Mean {target_label} Value",
                  value=f"£{tstats['value_mean']:,.0f}")
    with c:
        st.metric(label=f"Political Entities receiving {target_label}",
                  value=f"{tstats['regentity_ct']:,}")
    with right:
        st.metric(label=f"Total {target_label} Donors",
                  value=f"{tstats['donors_ct']:,}")
    st.write("---")
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
    if tstats["donors_ct"] >= 1:
        st.write(f"From {min_date} to {max_date}"
                 f" there were {tstats['donors_ct']:,.0f} donors"
                 "  identified as dubious."
                 f" These donors represented {dubious_percent_of_donors:.2f}%"
                 " of donors to regulated entities,"
                 f" and includes Impremissible Donors, Unidentified Donors "
                 f" and Aggregated Donors.  They donated a total of "
                 f"£{format_number(tstats['value_total'])},"
                 f" which represented {dubious_donors_percent_of_value:.2f}%"
                 " of the total value of donations made in the period.")
    else:
        st.write("* No donations from dubious donors were identified.")
    if tstats["donations_ct"] >= 1:
        st.write(
            f"* There were {tstats['donations_ct']:,.0f} donations that"
            " were identified as of questionable nature."
            f" These donations represented"
            f" {dubious_percent_of_donation_actions:.2f}% "
            "of all donations made in the period.")
    if brdstats["donations_ct"] >= 1:
        st.write(f"* {brdstats['donations_ct']} "
                 "donations had no recorded date.")
    else:
        st.write("* All donations had an identifiable date.")
    if bredstats["donations_ct"] >= 1:
        st.write(f"* {bredstats['donations_ct']} "
                 "donations had no recorded "
                 "regulated entity.")
    else:
        st.write("* All donations had an identifiable regulated entity.")
    if rfdstats["donations_ct"] >= 1:
        st.write(
            f"* Of these donations {rfdstats['donations_ct']} or"
            f" {returned_donations_percent_donations:.2f}% "
            "were returned to the donor,"
            f"representing £{format_number(rfdstats['value_total'])} or"
            f" or {returned_donations_percent_value:.2f}% of the total "
            "value of dubious donations.")
    else:
        st.write("* No donations were returned or forfeited.")
    if adstats["donations_ct"] >= 1:
        st.write(
            f"* There were {adstats['donations_ct']} aggregated donations,"
            f" representing {aggregated_percent_of_donation_actions:.2f}%"
            "of all donation actions."
            f" The total value of these aggregated donations was"
            f" £{format_number(adstats['value_total'])},"
            f" representing {aggregated_percent_of_value:.2f}% of "
            "the total value of all donations.")
    else:
        st.write("* No aggregated donations were identified.")
    if dvstats["donations_ct"] >= 1:
        st.write(
            f"* There were {dvstats['donations_ct']:,.0f} "
            "visits donated to regulated"
            " entities, representing "
            f"{donated_visits_percent_of_donation_actions:.2f}% of all "
            "donation actions. The total value of these visits was "
            f" £{format_number(dvstats['value_total'])}, representing "
            f" {donated_visits_percent_of_value:.2f}% of the total value of "
            "all donations.")
    else:
        st.write("* No visits were donated.")
    if sponstats["donations_ct"] >= 1:
        st.write(
            f"* There were {sponstats['donations_ct']:,.0f} sponsorships"
            " donated to regulated entities, representing "
            f"{sponstats['donations_ct']:,.0f} of all donation actions."
            f" The total value of these sponsorships was"
            f" £{format_number(sponstats['value_total'])}.")
    else:
        st.write("* No sponsorships were donated.")
    st.write("---")
    st.write("### Visuals")
    # Display the filtered data (Optional)
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if not cleaned_c_d_df.empty:
            plot_bar_line_by_year(
                Data=cleaned_c_d_df,
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
        if not cleaned_c_d_df.empty:
            plot_bar_line_by_year(
                Data=cleaned_c_d_df,
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
    st.write("---")
    left, mid, right = st.columns(3)
    with left:
        if not cleaned_c_d_df.empty:
            st.write("### Top 5\n ##### Regulated Entities: "
                     "Share of Total Donations")
            filtered_df2 = cleaned_c_d_df.groupby(
                "RegulatedEntityName")["Value"].sum().reset_index()
            filtered_df2["Perc_of_total"] = filtered_df2["Value"] / \
                filtered_df2["Value"].sum()
            filtered_df2 = filtered_df2.sort_values(
                by="Perc_of_total", ascending=False)
            st.write(filtered_df2.head(5))
        else:
            st.write("No data to display")
    with mid:
        if not cleaned_c_d_df.empty:
            st.write("### Top 5\n ##### Donors of Dubious Donations")
            filtered_df2 = cleaned_c_d_df.groupby(
                "DonorName")["Value"].sum().reset_index()
            filtered_df2 = filtered_df2.sort_values(
                by="Value", ascending=False)
            st.write(filtered_df2.head(5))
        else:
            st.write("No data to display")
    with right:
        if not cleaned_c_d_df.empty:
            st.write("### Top 5\n ##### Nature of Donations by value")
            filtered_df2 = cleaned_c_d_df.groupby(
                "NatureOfDonation")["Value"].sum().reset_index()
            filtered_df2 = filtered_df2.sort_values(by="Value",
                                                    ascending=False)
            st.write(filtered_df2.head(5))
        else:
            st.write("No data to display")
    st.write("---")
    if not cleaned_c_d_df.empty:
        st.write("### Scrollable table of identified donations")
        filtered_df3 = cleaned_c_d_df[["ReceivedDate",
                                       "RegulatedEntityName",
                                       "DonorName",
                                       "Value",
                                       "DonationAction",
                                       "DonationType",
                                       "RegulatedDoneeType",
                                       "NatureOfDonation",
                                       "DonorStatus",
                                       "DubiousData"]]
        st.write(filtered_df3)
    st.write("---")
    st.write("### Click on Visuals to expand the graphs."
             " Tables are scrollable")
    # add a link to the streamlit dubiousdonationsbyDonor screen to allow
    # users to explore the data further
    st.write("### Explore the data further using the Dubious Donations by"
             " Donor link in the menu")
    st.write("---")
    st.write(
        "### or Check out Transparency International's"
        "[Recent Publication]"
        "(https://www.transparency.org.uk/news/new-research-reveals-almost-ps1-every-ps10-political-donations-comes-unknown-or-questionable)"
        "for more information on donations to UK Political Parties.")
    st.write("---")
