import streamlit as st
import datetime as dt
from data.data_loader import load_cleaned_data
from components.filters import filter_by_date, apply_filters
from components.calculations import (compute_summary_statistics, get_mindate,
                                     get_maxdate, calculate_percentage,
                                     format_number)
from components.Visualisations import (plot_custom_bar_chart,
                                       plot_bar_line_by_year)
from components.predefined_visualizations import (visit_graph1, visits_graph2,
                                                   visits_graph3, visits_graph4)

def visits_body_page():
    """Displays the Cash Donations page in Streamlit."""

    # Load dataset
    cleaned_df = load_cleaned_data()
    if cleaned_df is None:
        st.error("No data found. Please upload a dataset.")
        return

    # Date range selection
    min_date = get_mindate(cleaned_df).date()
    max_date = get_maxdate(cleaned_df).date()

    # Convert selected dates to datetime
    start_date, end_date = (
        dt.datetime.combine(min_date, dt.datetime.min.time()),
        dt.datetime.combine(max_date, dt.datetime.max.time())
        )

    # Define filter condition
    current_target = st.session_state["filter_def"].get("DonatedVisits_ftr")
    target_label = "Donated Visit"
    filters = {}

    # Apply filters apply date filter
    cleaned_d_df = filter_by_date(cleaned_df, start_date, end_date)
    # limit to target type of donation
    cleaned_c_d_df = apply_filters(cleaned_d_df,
                                   current_target,
                                   logical_operator="or")

    # Compute Statistics
    min_date_df = get_mindate(cleaned_c_d_df, filters).date()
    max_date_df = get_maxdate(cleaned_c_d_df, filters).date()
    tstats = compute_summary_statistics(cleaned_c_d_df, filters)
    ostats = compute_summary_statistics(cleaned_d_df, filters)
    perc_cash_donations_d = calculate_percentage(tstats['unique_donations'],
                                                 ostats['unique_donations'])

    st.write(f"## Summary Statistics for {target_label}s,"
             f" from {min_date_df} to {max_date_df}")
    left, a, b, mid, c, right = st.columns(6)
    with left:
        st.metric(label=f"Total {target_label}",
                  value=f"£{tstats['total_value']:,.0f}")
    with a:
        st.metric(label=f"{target_label} % of Total Donations",
                  value=f"{perc_cash_donations_d:.2f}%")
    with b:
        st.metric(label=f"{target_label} Donations",
                  value=f"{tstats['unique_donations']:,}")
    with mid:
        st.metric(label=f"Mean {target_label} Value",
                  value=f"£{tstats['mean_value']:,.0f}")
    with c:
        st.metric(label=f"Total {target_label} Entities",
                  value=f"{tstats['unique_reg_entities']:,}")
    with right:
        st.metric(label=f"Total {target_label} Donors",
                  value=f"{tstats['unique_donors']:,}")
    st.write("---")
    left, right = st.columns(2)
    with left:
        st.write("## Explaination")
        st.write("* Political Entities also get support from donors in the"
                 " form of funded visits. These are identified by the regulator and"
                 " marked in the data. This page provides a summary of the"
                 " visits funded for political parties and other regulated"
                 " political organisations and entities.")
        st.write("* Over the years there have been occurances where the"
                 " funding of visits has been used as a source of dubious"
                 " funding. This page provides a summary of the visits funded"
                 f" between {min_date_df} and {max_date_df}.")
    with right:
        st.write(f"## Topline Figures for {target_label}s")
        st.write(f"* During the period between {min_date_df} to {max_date_df},"
                 f" there were {tstats['unique_donations']:,.0f} "
                 f"{target_label}s made to "
                 f"{tstats['unique_reg_entities']} regulated entities.")
        st.write(f"* These had a mean value of £"
                 f"{format_number(tstats['mean_value'])} "
                 f"and were made by {format_number(tstats['unique_donors'])} "
                 "unique donors.")
        st.write(f"* {target_label}s were {perc_cash_donations_d:.2f}% of "
                 f"all donations made to political parties between {min_date}"
                 f"and {max_date}. All these had a total value of £ "
                 f"{format_number(tstats['total_value'])}")
    st.write("---")
    left, right = st.columns(2)
    with left:
        st.write(f"## Topline Visuals for {target_label}s")
    with right:
        st.write("### Click on any Visualisation to view it full screen.")
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        # Display results
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            visit_graph1(target_label, cleaned_c_d_df)
    # Display visualizations
    with right_column:
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            visits_graph2(target_label, cleaned_c_d_df)
    st.write("---")
    left, right = st.columns(2)
    with left:
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            visits_graph3(target_label, cleaned_c_d_df)
    with right:
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            visits_graph4(target_label, cleaned_c_d_df)
        st.write("some wonderful insights here.")
    st.write("---")
