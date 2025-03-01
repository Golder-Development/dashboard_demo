import streamlit as st
from components.modular_page_blocks import (
    load_and_filter_pergroup,
    display_summary_statistics,
    display_textual_insights,
    display_visualizations,
)
# from utils.logger import logger
from utils.logger import log_function_call  # Import decorator


@log_function_call
def display_data_page(filter_key=None, target_label="default", entity="Donor"):
    """
    Template function to generate a
    Streamlit page for a specific data slice.
    """
    perc_target = st.session_state.get("perc_target", 0.5)
    pageref_label = "filter_key" + "target_label"
    (
        cleaned_df,
        cleaned_d_df,
        cleaned_r_df,
        cleaned_c_df,
        cleaned_c_d_df,
        cleaned_r_d_df,
        cleaned_c_r_df,
        cleaned_c_r_d_df,
    ) = load_and_filter_pergroup(
        groupentity=entity, filter_key=filter_key, pageref_label=pageref_label
    )

    if cleaned_df is None:
        return

    (min_date,
     max_date,
     tstats,
     ostats,
     perc_target) = display_summary_statistics(
        filtered_df=cleaned_c_r_d_df,
        overall_df=cleaned_df,
        target_label=target_label,
        pageref_label=pageref_label,
    )

    display_textual_insights(
        pageref_label=pageref_label,
        target_label=target_label,
        min_date=min_date,
        max_date=max_date,
        tstats=tstats,
        ostats=ostats,
        perc_target=perc_target,
    )

    st.write("---")
    display_visualizations(
        cleaned_c_r_d_df,
        target_label=target_label,
        pageref_label=pageref_label
    )
