import streamlit as st
import datetime as dt
from components.filters import filter_by_date, apply_filters
from components.calculations import (compute_summary_statistics,
                                     get_mindate,
                                     get_maxdate,
                                     calculate_percentage,
                                     format_number)
from components.Visualisations import (
                                       plot_bar_line_by_year)


def dubiousdonations_body():
    """
    Displays the content of the Donations by Political Party page.
    """
    # Page Title
    st.write("---")
    # Load dataset
    cleaned_df = st.session_state.get("data_clean", None)
    if cleaned_df is None:
        st.error("No data found. Please upload a dataset.")
        return
    # Define filter condition
    current_target = st.session_state.filter_def.get("DubiousDonations_ftr")
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
        st.session_state["filter_def"].get("AggregatedDonations_ftr"))
    # Unidentified Donors
    udstats = compute_summary_statistics(
        cleaned_c_d_df,
        st.session_state["filter_def"].get("DubiousDonors_ftr"))
    # visits
    dvstats = compute_summary_statistics(
        cleaned_c_d_df,
        st.session_state["filter_def"].get("DonatedVisits_ftr"))
    # returned and forfeited donations
    return_filters = (
        st.session_state["filter_def"].get("ReturnedDonations_ftr")
    )
    rfdstats = compute_summary_statistics(
        cleaned_c_d_df, return_filters)
    # blank received date
    blank_date_filters = st.session_state["filter_def"].get("BlankDate_ftr")
    brdstats = compute_summary_statistics(
        cleaned_c_d_df, blank_date_filters)
    # blank regulated entity data
    blank_reg_entity_filters = (
        st.session_state["filter_def"].get("BlankRegEntity_ftr")
    )
    bredstats = compute_summary_statistics(
        cleaned_c_d_df, blank_reg_entity_filters)
    # donated sponsorships
    sponstats = compute_summary_statistics(
        cleaned_c_d_df, st.session_state["filter_def"].get("Sponsorships_ftr"))
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
        st.write('udstats', udstats)
        st.write("---")
    # Calculate the percentage of donations that are cash donations
    dubious_donors_percent_of_value = calculate_percentage(
        tstats["unique_donors"], ostats["unique_donors"])
    dubious_percent_of_value = calculate_percentage(
        tstats["total_value"], ostats["total_value"])
    dubious_percent_of_donors = calculate_percentage(
        tstats['unique_donors'], ostats["unique_donors"])
    dubious_percent_of_donation_actions = calculate_percentage(
        tstats["unique_donations"], ostats["unique_donations"])
    returned_donations_percent_value = calculate_percentage(
          rfdstats["total_value"], tstats["total_value"])
    returned_donations_percent_donations = calculate_percentage(
          rfdstats["unique_donations"], tstats["unique_donations"])
    aggregated_percent_of_donation_actions = calculate_percentage(
        adstats['unique_donations'], ostats['unique_donations'])
    aggregated_percent_of_value = calculate_percentage(
        adstats['total_value'], ostats['total_value'])
    donated_visits_percent_of_donation_actions = calculate_percentage(
        dvstats['unique_donations'], ostats['unique_donations'])
    donated_visits_percent_of_value = calculate_percentage(
        dvstats['total_value'], ostats['total_value'])
    min_date = get_mindate(cleaned_d_df).date()
    max_date = get_maxdate(cleaned_d_df).date()

    # Format text
    st.write(f"### Summary Statistics for {target_label}s,"
             f"### from {min_date} to {max_date}")
    left, a, b, mid, c, right = st.columns(6)
    with left:
        st.metric(label=f"Total {target_label}",
                  value=f"£{tstats['total_value']:,.0f}")
    with a:
        st.metric(label=f"{target_label}%",
                  value=f"{dubious_percent_of_value:.0f}%")
    with b:
        st.metric(label=f"{target_label}",
                  value=f"{tstats['unique_donations']:,}")
    with mid:
        st.metric(label=f"Mean {target_label} Value",
                  value=f"£{tstats['mean_value']:,.0f}")
    with c:
        st.metric(label=f"Political Entities receiving {target_label}",
                  value=f"{tstats['unique_reg_entities']:,}")
    with right:
        st.metric(label=f"Total {target_label} Donors",
                  value=f"{tstats['unique_donors']:,}")
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
    if tstats["unique_donors"] >= 1:
        st.write(f"From {min_date} to {max_date}"
                 f" there were {tstats['unique_donors']:,.0f} donors"
                 "  identified being involved with dubious donations."
                 f" These donors represented {dubious_percent_of_donors:,.0f}%"
                 " of donors to regulated entities,"
                 f" and includes Impremissible Donors, Unidentified Donors "
                 f" and Aggregated Donors.  They donated a total of "
                 f"£{format_number(tstats['total_value'])},"
                 f" which represented {dubious_donors_percent_of_value:.0f}%"
                 " of the total value of donations made in the period.")
    else:
        st.write("* No donations from dubious donors were identified.")
    if tstats["unique_donations"] >= 1:
        st.write(
            f"* There were {tstats['unique_donations']:,.0f} donations that"
            " were identified as of questionable nature."
            f" These donations represented"
            f" {dubious_percent_of_donation_actions:.0f}% "
            "of all donations made in the period.")
    if brdstats["unique_donations"] >= 1:
        st.write(f"* {brdstats['unique_donations']} "
                 "donations had no recorded date.")
    else:
        st.write("* All donations had an identifiable date.")
    if udstats["unique_donors"] >= 1:
        st.write(f"From {min_date} to {max_date}"
                 f" there were {udstats['unique_donors']:,.0f} donors"
                 "  identified as dubious."
                 f" These donors represented {dubious_percent_of_donors:.2f}%"
                 " of donors to regulated entities,"
                 f" and includes Impremissible Donors, Unidentified Donors "
                 f" and Aggregated Donors.  They donated a total of "
                 f"£{format_number(udstats['total_value'])},"
                 f" which represented {dubious_donors_percent_of_value:.2f}%"
                 " of the total value of donations made in the period.")
    else:
        st.write("* No donations from dubious donors were identified.")
    if bredstats["unique_donations"] >= 1:
        st.write(f"* {bredstats['unique_donations']} "
                 "donations had no recorded "
                 "regulated entity.")
    else:
        st.write("* All donations had an identifiable regulated entity.")
    if rfdstats["unique_donations"] >= 1:
        st.write(
            f"* Of these donations {rfdstats['unique_donations']} or"
            f" {returned_donations_percent_donations:.2f}% "
            "were returned to the donor,"
            f"representing £{format_number(rfdstats['total_value'])} or"
            f" or {returned_donations_percent_value:.2f}% of the total "
            "value of dubious donations.")
    else:
        st.write("* No donations were returned or forfeited.")
    if adstats["unique_donations"] >= 1:
        st.write(
            f"* There were {adstats['unique_donations']} aggregated donations,"
            f" representing {aggregated_percent_of_donation_actions:.2f}%"
            "of all donation actions."
            f" The total value of these aggregated donations was"
            f" £{format_number(adstats['total_value'])},"
            f" representing {aggregated_percent_of_value:.2f}% of "
            "the total value of all donations.")
    else:
        st.write("* No aggregated donations were identified.")
    if dvstats["unique_donations"] >= 1:
        st.write(
            f"* There were {dvstats['unique_donations']:,.0f} "
            "visits donated to regulated"
            " entities, representing "
            f"{donated_visits_percent_of_donation_actions:.2f}% of all "
            "donation actions. The total value of these visits was "
            f" £{format_number(dvstats['total_value'])}, representing "
            f" {donated_visits_percent_of_value:.2f}% of the total value of "
            "all donations.")
    else:
        st.write("* No visits were donated.")
    if sponstats["unique_donations"] >= 1:
        st.write(
            f"* There were {sponstats['unique_donations']:,.0f} sponsorships"
            " donated to regulated entities, representing "
            f"{sponstats['unique_donations']:,.0f} of all donation actions."
            f" The total value of these sponsorships was"
            f" £{format_number(sponstats['total_value'])}.")
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
        "(https://www.transparency.org.uk/news/new-research-reveals-almost-ps1"
        "-every-ps10-political-donations-comes-unknown-or-questionable)"
        "for more information on donations to UK Political Parties.")
    st.write("---")
