import streamlit as st
from app_pages.modular_page_blocks import (load_and_filter_perentity,
                                           display_summary_statistics,
                                           display_textual_insights,
                                           display_visualizations)


def display_data_page(filter_key,
                      target_label="default",
                      groupentity="RegulatedEntity"):
    """
    Template function to generate a Streamlit
    page for a specific data slice.
    """
    (cleaned_df,
     cleaned_d_df,
     cleaned_r_df,
     cleaned_c_df,
     cleaned_c_d_df,
     cleaned_r_d_df,
     cleaned_c_r_df,
     cleaned_c_r_d_df) = load_and_filter_perentity(groupentity,
                                                   filter_key)
    if cleaned_df is None:
        return

    (min_date,
     max_date,
     tstats,
     ostats,
     perc_target) = display_summary_statistics(cleaned_c_r_d_df,
                                               cleaned_df,
                                               target_label)

    display_textual_insights(target_label,
                             min_date,
                             max_date,
                             tstats,
                             ostats,
                             perc_target)

    st.write("---")
    display_visualizations(cleaned_c_r_d_df,
                           target_label)
