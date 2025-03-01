import streamlit as st
import components.Visualisations as vis
from utils.logger import logger  # Import the logger
from utils.logger import log_function_call  # Import decorator
from components.calculations import (format_number,
                                     calculate_percentage,
                                     get_donors_ct,
                                     get_value_total,
                                     get_value_mean,
                                     get_donations_ct,
                                     get_regentity_ct,
                                     get_donationtype_ct,
                                     get_mindate,
                                     get_maxdate,
                                     get_top_entity_by_value,
                                     get_top_entity_by_donations,
                                     get_top_donType_by_don,
                                     )

def hlf_body():
    """
    This function displays the content of Page two.
    """
    df = st.session_state.get("data_clean", None)
    # sum_df = st.session_state.get("data_party_sum", None)
    # set filters to None and filtered_df to the original dataset
    filters = None
    filtered_df = df
    # Call each function separately with the selected filter
    unique_donors = get_donors_ct(filtered_df)
    total_value_donations = get_value_total(filtered_df)
    mean_value_donations = get_value_mean(filtered_df)
    unique_donations = get_donations_ct(filtered_df)
    unique_regulated_entities = get_regentity_ct(filtered_df)
    PP_donations = get_donationtype_ct(
        filtered_df, {"RegulatedEntityType": "Political Party"}
    )
    PP_donations_value = get_value_total(
        filtered_df, {"RegulatedEntityType": "Political Party"}
    )
    PP_donations_percent = calculate_percentage(
        PP_donations, unique_donations)
    PP_donations_value_percent = calculate_percentage(
        PP_donations_value, total_value_donations)
    single_donation_entity = get_donations_ct(
        filtered_df, {"RegEntity_Group": "Single Donation Entity"}
    )
    single_donation_entity_value = get_value_total(
        filtered_df, {"RegEntity_Group": "Single Donation Entity"}
    )
    single_donation_percent = calculate_percentage(
        single_donation_entity, unique_donations)
    single_donation_entity_value_percent = calculate_percentage(
        single_donation_entity_value, total_value_donations)
    single_donation_entity_percent = calculate_percentage(
        single_donation_entity,  unique_regulated_entities)
    min_date = get_mindate(filtered_df, filters).date()
    max_date = get_maxdate(filtered_df, filters).date()

    # Get the regulated entity with the greatest value of donations
    top_entity, top_value = get_top_entity_by_value(
        filtered_df, filters
    )
    # Get the regulated entity with the greatest number of donations
    top_entity_ct, top_donations = get_top_entity_by_donations(
        filtered_df, filters)
    # Get the donationtype with the greatest number of donations
    top_dontype_ct, top_dontype_dons = get_top_donType_by_don(
        filtered_df, filters)
    # Get the donationtype with the greatest number of donations
    top_dontype_value = get_value_total(
        filtered_df, {'DonationType': top_dontype_ct}
    )
    top_entity_value_percent = calculate_percentage(
        top_value, total_value_donations)
    top_dontype_value_percent = calculate_percentage(
        top_dontype_value, total_value_donations)
    top_dontype_dons_percent = calculate_percentage(
        top_dontype_dons, unique_donations)
    # Display the headline figures
    st.write("---")
    st.write("## Topline Summary of Political Donations "
             f" from {min_date} to {max_date}")
    d, left, a, b, mid, c, right = st.columns(7)
    with d:
        st.metric(label="Total Value of Donations",
                  value=f"£{format_number(total_value_donations)}")
    with left:
        st.metric(label="Total Donations",
                  value=f"{format_number(unique_donations)}")
    with a:
        st.metric(label=f"{top_entity} %",
                  value=f"{format_number(top_entity_value_percent)}%")
    with b:
        st.metric(label=f"{top_dontype_ct} Donations",
                  value=f"{format_number(top_dontype_dons)}")
    with mid:
        st.metric(label="Average Donation Value",
                  value=f"£{format_number(mean_value_donations)}")
    with c:
        st.metric(label="Total Regulated Entities",
                  value=f"{format_number(unique_regulated_entities)}")
    with right:
        st.metric(label="Total Donors",
                  value=f"{format_number(unique_donors)}")
    st.write("---")
    mid, right = st.columns(2)
    with mid:
        if filtered_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            vis.plot_bar_line_by_year(filtered_df,
                                      XValues="YearReceived",
                                      YValues="EventCount",
                                      GroupData="RegulatedEntityType",
                                      XLabel="Year", YLabel="Donations",
                                      Title="Donations per Year & Entity Type",
                                      CalcType='sum',
                                      LegendTitle="Regulated Entity Type",
                                      widget_key="dons_by_year_n_entity")
    with right:
        if filtered_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            filtered_df_sort = filtered_df.sort_values(
                by=["YearReceived", "DubiousData"],
                ascending=[True, False]
            )
            filtered_df_sort = filtered_df_sort.rename(
                columns={"DubiousData": "Data Safety Score"}
            )
            vis.plot_bar_line_by_year(filtered_df_sort,
                                      XValues="YearReceived",
                                      YValues="EventCount",
                                      GroupData="Data Safety Score",
                                      XLabel="Year",
                                      YLabel="Donations",
                                      Title="Donations Risk Score by Year",
                                      CalcType='sum',
                                      LegendTitle="Data Safety Score",
                                      ChartType="line",
                                      y_scale="linear",
                                      widget_key="dons_by_year_n_type")
    st.write("---")
    st.write("### Headline Figures")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"* During the period from {min_date} to {max_date} "
                 f"{unique_regulated_entities:,.0f} regulated political "
                 "bodies received donations.")
        st.write(
            "* These had a total value of "
            f"£{format_number(total_value_donations)} "
            f"from {format_number(unique_donors)} unique donors."
            f"  The average donation was "
            f"£{format_number(mean_value_donations)} "
            f"and there were {format_number(unique_donations)}"
            " unique donations"
        )
        st.write(
            f"* Political parties were identified as the "
            f"donor in {PP_donations_percent:.2f}% "
            f"of donations. These donations were worth"
            f" £{format_number(PP_donations_value)} "
            f"or {PP_donations_value_percent:.2f}% of the total "
            "value of donations."
        )
        st.write(
            f"* {single_donation_entity} of the donations were to entities "
            f"that only received one donation. These donations represented "
            f"{single_donation_percent:.2f}% of all donations, were worth "
            f" £{format_number(single_donation_entity_value)} or "
            f"{single_donation_entity_value_percent:.2f}% of the total value "
            f"of donations and were {single_donation_entity_percent:.0f}% of "
            f"the regulated entities."
        )
    with col2:
        st.write(
            f"* Most Donations were in {top_dontype_ct}, these "
            f"represented {top_dontype_dons_percent:.2f}% of "
            f"donations and were {top_dontype_value_percent:.2f}% "
            f"of the total value of donations.")
        st.write(
            f"* The {top_entity} received the most donations by value, with "
            f"a total value of £{format_number(top_value)} or "
            f"{top_value/total_value_donations*100:.2f}% of all donations.")
        st.write(
            f"* The {top_entity_ct} received the most donations by count, "
            f"having {top_donations:,.0f} donations which represented "
            f"{top_donations/unique_donations*100:.2f}% of all donations.")
    st.write("---")
    mid, right = st.columns(2)
    with mid:
        if filtered_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            vis.plot_bar_line_by_year(filtered_df,
                                      XValues="YearReceived",
                                      YValues="Value",
                                      GroupData="RegEntity_Group",
                                      XLabel="Year",
                                      YLabel="Value of Donations £ 000's",
                                      Title="Donations GBP by Year & Entity",
                                      use_custom_colors=True,
                                      LegendTitle="Regulated Entity",
                                      widget_key="value_by_year_n_entity",
                                      CalcType='sum')
    with right:
        if filtered_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            vis.plot_bar_line_by_year(filtered_df,
                                      XValues="YearReceived",
                                      YValues="Value",
                                      GroupData="DonationType",
                                      XLabel="Year",
                                      YLabel="Total Value (£)",
                                      y_scale="log",
                                      ChartType="Line",
                                      LegendTitle="Donation Type",
                                      Title="Donations GBP Types by Year",
                                      widget_key="value_by_year_n_type",
                                      CalcType='sum')
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if filtered_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            st.write("### Entity Distribution")
            vis.plot_pie_chart(
                graph_df=filtered_df,
                YValues="RegEntity_Group",
                XValues="Value",  # Use None for count
                color_column="RegEntity_Group",
                use_custom_colors=True,  # Use custom colors
                color_mapping=None,
                Title="Distribution of Donated Value by Entity",
                YLabel="Regulated Entity",
                XLabel="Percentage of Total Donations",
                hole=0.3,  # Adjust for more or less donut effect
                widget_key="pie_Value_by_entity"
            )
    with col2:
        if filtered_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            st.write("### Entity Distribution")
            vis.plot_pie_chart(
                graph_df=filtered_df,
                YValues="RegEntity_Group",
                XValues="EventCount",  # Use None for count
                color_column="RegEntity_Group",
                use_custom_colors=True,  # Use custom colors
                color_mapping=None,
                Title="Distribution of Donations by Entity",
                YLabel="Regulated Entity",
                XLabel="Percentage of Donation Events",
                hole=0.3,  # Adjust for more or less donut effect
                widget_key="pie_donations_by_entity"
            )
    st.write("---")
