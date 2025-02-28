import streamlit as st
from components.modular_page_blocks import (topline_summary_block,
                                            load_and_filter_data,
                                            display_summary_statistics,
                                            display_textual_insights,
                                            display_visualizations)
from components.predefined_visualizations import (display_donations_by_entity,
                                                  display_donations_by_year_and_entity,
                                                  display_donations_by_donor_type,
                                                  display_donations_by_donor_type_chart)
from components.calculations import (compute_summary_statistics, get_mindate,
                                     get_maxdate, calculate_percentage,
                                     format_number)
from components.Visualisations import (plot_custom_bar_chart,
                                       plot_bar_line_by_year)
from utils.logger import logger
from utils.logger import log_function_call  # Import decorator

@log_function_call
def cash_donations_page():
    """Displays the Cash Donations page in Streamlit."""
    # Load dataset
    cash_ftr = st.session_state.get("cash_ftr", None)
    target_label = "Cash Donation"
    pageref_label = "filtered_key" + "target_label"
    (cleaned_df,
     cleaned_c_d_df) = load_and_filter_data(cash_ftr, pageref_label)

    if cleaned_df is None:
        st.error("No data found. Please upload a dataset.")
        return

    (min_date,
     max_date,
     tstats,
     ostats,
     perc_target) = display_summary_statistics(
        cleaned_c_d_df,
        cleaned_df,
        target_label,
        pageref_label
    )
    if perc_target is None:
        perc_target = st.session_state.get("perc_target", 0.5)

    # Compute Statistics
    perc_cash_donations_d = calculate_percentage(tstats['unique_donations'],
                                                 ostats['unique_donations'])

    topline_summary_block(target_label,
                          min_date,
                          max_date,
                          tstats,
                          perc_cash_donations_d)

    display_textual_insights(
        pageref_label,
        target_label,
        min_date,
        max_date,
        tstats,
        ostats,
        perc_target
    )

    left, right = st.columns(2)
    with left:
        st.write("## Explaination")
        st.write("* The most donations to political parties are in cash."
                 "These vary from small donations from individuals, to larger "
                 "aggregated donations from multiple donors, and include "
                 "donations from trade unions,business and bequests.")
        st.write("* These are identified by the regulator and marked in the"
                 " data. "
                 "This page provides a summary of the cash donations to "
                 "political parties and other regulated political."
                 " organisations and entities.")
    with right:
        st.write("## Topline Figures")
        st.write(f"* During the period between {min_date} to {max_date},"
                 f" there were {tstats['unique_donations']:,.0f} "
                 "cash donations made to "
                 f"{tstats['unique_reg_entities']} regulated entities.")
        st.write(f"* These had a mean value of £"
                 f"{format_number(tstats['mean_value'])} "
                 f"and were made by {format_number(tstats['unique_donors'])} "
                 "unique donors.")
        st.write(f"* Cash donations were {perc_cash_donations_d:.2f}% of "
                 f"all donations made to political parties between {min_date}"
                 f"and {max_date}. All these had a total value of £ "
                 f"{format_number(tstats['total_value'])}")
    st.write("---")
    left, right = st.columns(2)
    with left:
        st.write("## Topline Visuals")
    with right:
        st.write("### Click on any Visualisation to view it full screen.")
    st.write("---")
    # Display visualizations
    display_visualizations(cleaned_c_d_df, target_label, pageref_label)
    left_column, right_column = st.columns(2)
    with left_column:
        # Display results
        # Call the function
        display_donations_by_entity(cleaned_c_d_df)
    with right_column:
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            # Call the function
            display_donations_by_year_and_entity(cleaned_c_d_df)
    st.write("---")
    left, right = st.columns(2)
    with left:
        st.write('#### Cash Donations by Donor Type')
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            # Call the function
            display_donations_by_donor_type(cleaned_c_d_df)
    with right:
        st.write('#### Average Donation Value by Donor Type')
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            # Call the function
            display_donations_by_donor_type_chart(cleaned_c_d_df)
    st.write("---")
