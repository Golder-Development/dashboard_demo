import streamlit as st
from app_pages.modular_page_blocks import (display_summary_statistics,
                                           display_textual_insights,
                                           display_visualizations,
                                           load_and_filter_data)


def display_data_page(filter_key, target_label):
    """
    Template function to generate a Streamlit
    page for a specific data slice.
    """
    cleaned_df, filtered_df = load_and_filter_data(filter_key)
    if cleaned_df is None:
        return

    (min_date,
     max_date,
     tstats,
     ostats,
     perc_target) = display_summary_statistics(filtered_df,
                                               cleaned_df,
                                               target_label)

    display_textual_insights(target_label,
                             min_date,
                             max_date,
                             tstats,
                             ostats,
                             perc_target)

    st.write("---")
    display_visualizations(filtered_df, target_label)
