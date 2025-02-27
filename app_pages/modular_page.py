import streamlit as st
from components.modular_page_blocks import (
    display_summary_statistics,
    display_textual_insights,
    display_visualizations,
    load_and_filter_data,
)
from utils.logger import logger
from utils.decorators import log_function_call  # Import decorator


def display_data_page(filter_key, target_label):
    """
    Template function to generate a Streamlit
    page for a specific data slice.
    """
    pageref_label = "filtered_key" + "target_label"
    cleaned_df, filtered_df = load_and_filter_data(filter_key, pageref_label)
    if cleaned_df is None:
        return

    (min_date, max_date, tstats, ostats, perc_target) = display_summary_statistics(
        filtered_df, cleaned_df, target_label, pageref_label
    )
    perc_target = st.session_state.get("perc_target", 0.5)
    display_textual_insights(
        pageref_label, target_label, min_date, max_date, tstats, ostats, perc_target
    )

    st.write("---")
    display_visualizations(filtered_df, target_label, pageref_label)
