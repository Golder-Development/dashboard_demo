import streamlit as st
from components.modular_page_blocks import (
    load_and_filter_pergroup,
    display_summary_statistics,
    display_textual_insights_predefined,
    display_textual_insights_custom,
    display_visualizations,
)
# from utils.logger import logger
from utils.logger import log_function_call  # Import decorator


@log_function_call
def display_per_group_data_page(
                                functionname="display_per_group_data_page",
                                filter_key=None,
                                target_label="default",
                                group_entity="Donor",
                                tab_name=None):
    perc_target = st.session_state.get("perc_target", 0.5)
    pageref_label = f"{functionname}{target_label}{tab_name}"
    (cleaned_df,
        cleaned_d_df,
        cleaned_r_df,
        cleaned_c_df,
        cleaned_c_d_df,
        cleaned_r_d_df,
        cleaned_c_r_df,
        cleaned_c_r_d_df,
     ) = load_and_filter_pergroup(
        group_entity=group_entity,
        filter_key=filter_key,
        pageref_label=pageref_label,
        functionname=functionname,
        tab_name=tab_name
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

    st.write("---")
    left, right = st.columns(2)
    with left:
        display_textual_insights_predefined(
            pageref_label,
            target_label,
            min_date,
            max_date,
            tstats,
            ostats,
            perc_target
        )
    with right:
        display_textual_insights_custom(
            target_label=target_label,
            pageref_label=pageref_label)

    st.write("---")
    display_visualizations(
        cleaned_c_r_d_df,
        target_label=target_label,
        pageref_label=pageref_label
    )
