import streamlit as st
from Visualisations import (
    plot_bar_line,
    plot_pie_chart,
    plot_bar_chart
)
from utils.logger import log_function_call, logger
from components.calculations import (
    format_number,
    calculate_percentage,
    get_top_or_bottom_entity_by_column,
    calculate_agg_by_variable,
    compute_summary_statistics
    )
from components.modular_page_blocks import (
    load_and_filter_data,
    display_summary_statistics,
    )


@log_function_call
def hlf_body():
    """
    This function displays the content of Page two.
    """
    (tab1,
     tab2,
     tab3,
     tab4,
     tab5) = st.tabs(["HeadLine Figures",
                      "Topline Graphs",
                      "More Graphs",
                      "Pie Charts",
                      "Avg Donations"])
    filter_key = None
    # Load and filter data
    with tab1:
        cleaned_df, filtered_df = (
            load_and_filter_data(filter_key=filter_key,
                                 pagereflabel="headlinefigures"))
        if cleaned_df is None or filtered_df is None:
            logger.error("Data not loaded or filtered")
            return
        # Display summary statistics
        (min_date_df,
         max_date_df,
         tstats,
         ostats,
         perc_target) = display_summary_statistics(
            filtered_df,
            cleaned_df,
            "Political Donations",
            "headlinefigures"
        )

        # # Get the regulated entity with the greatest value of donations
        top_entity, top_value = get_top_or_bottom_entity_by_column(
            df=filtered_df, column="PartyName",
            value_column="Value", top=True)
        # Get the regulated entity with the greatest number of donations
        top_entity_ct, top_donations = get_top_or_bottom_entity_by_column(
            df=filtered_df, column="PartyName",
            value_column="EventCount", top=True)
        # Get the donation type with the greatest number of donations
        top_dontype_ct, top_dontype_dons = get_top_or_bottom_entity_by_column(
            df=filtered_df, column="DonationType",
            value_column="EventCount", top=True)
        # Get the donation type with the greatest value of donations
        top_dontype, top_dontype_value = get_top_or_bottom_entity_by_column(
            df=filtered_df, column="DonationType",
            value_column="Value", top=True)
        # calculate the percentage of donations and value for political parties
        top_dontype_value_percent = (
            calculate_percentage(top_dontype_value, tstats["total_value"]))
        top_dontype_dons_percent = (
            calculate_percentage(top_dontype_dons, tstats["unique_donations"]))
        st.write("---")
        st.write("### Headline Figures")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"* During the period {min_date_df} to {max_date_df} "
                     f"{tstats['unique_reg_entities']:,.0f} regulated "
                     "political bodies received donations.")
            st.write(
                "* These had a total value of "
                f"£{format_number(tstats['total_value'])} "
                f"from {format_number(tstats['unique_donors'])} unique donors."
                f"  The average donation was "
                f"£{format_number(tstats['mean_value'])} "
                f"and there were {format_number(tstats['unique_donations'])}"
                " unique donations"
            )
            pstats = (
                compute_summary_statistics(
                    filtered_df,
                    {"RegulatedEntityType": "Political Party"})
            )
            PP_donations_percent = calculate_percentage(
                pstats["unique_donations"], tstats["unique_donations"]
            )
            PP_donations_value_percent = calculate_percentage(
                pstats["total_value"], tstats["total_value"]
            )
            st.write(
                f"* Political parties were identified as the "
                f"donor in {PP_donations_percent:.2f}% "
                f"of donations. These donations were worth"
                f" £{format_number(pstats['total_value'])} "
                f"or {PP_donations_value_percent:.2f}% of the total "
                "value of donations."
            )
            sde_stats = (
                compute_summary_statistics(
                    filtered_df,
                    {"Party_Group": "Single Donation Entity"})
            )
            if sde_stats["unique_donations"] == 0:
                st.write(
                    "* There were no donations to entities that"
                    " only received one donation."
                )
            else:
                single_donation_percent = calculate_percentage(
                    sde_stats["unique_donations"], tstats["unique_donations"]
                )
                single_donation_entity_value_percent = calculate_percentage(
                    sde_stats["total_value"], tstats["total_value"]
                )
                single_donation_entity_percent = calculate_percentage(
                    sde_stats["unique_reg_entities"],
                    tstats["unique_reg_entities"]
                )
                st.write(
                    f"* {sde_stats['unique_donations']} of the"
                    " donations were to entities "
                    "that only received one donation. "
                    "These donations represented "
                    f"{single_donation_percent:.2f}% of all donations, were "
                    f" worth £{format_number(sde_stats['total_value'])} or "
                    f"{single_donation_entity_value_percent:.2f}% of"
                    " the total value of donations"
                    f" and were {single_donation_entity_percent:.0f}"
                    "% ofthe regulated entities."
                )
        with col2:
            st.write(
                f"* Most Donations were in {top_dontype_ct}, these "
                f"represented {top_dontype_dons_percent:.2f}% of "
                f"donations and were {top_dontype_value_percent:.2f}% "
                f"of the total value of donations.")
            st.write(
                f"* The {top_entity} received the most donations by value, "
                f"with a total value of £{format_number(top_value)} or "
                f"{top_value/tstats['total_value']*100:.2f}% "
                "of all donations.")
            st.write(
                f"* The {top_entity_ct} received the most donations by count, "
                f"having {top_donations:,.0f} donations which represented "
                f"{top_donations/tstats['unique_donations']*100:.2f}%"
                " of all donations.")
        st.write("---")
    with tab2:
        mid, right = st.columns(2)
        with mid:
            if cleaned_df.empty:
                st.write("No data available for the selected filters.")
                return
            else:
                plot_bar_line.plot_bar_line_by_year(
                    graph_df=cleaned_df,
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
                filtered_df_sort = filtered_df_sort[
                    filtered_df_sort["DubiousData"] > 0
                ]  
                filtered_df_sort = filtered_df_sort.rename(
                    columns={"DubiousData": "Data Safety Score"}
                )
                plot_bar_line.plot_bar_line_by_year(
                    graph_df=filtered_df_sort,
                    XValues="YearReceived",
                    YValues="Value",
                    GroupData="Data Safety Score",
                    XLabel="Year",
                    YLabel="Donations GBP",
                    Title="Donations Risk Score by Year",
                    CalcType='sum',
                    LegendTitle="Data Safety Score",
                    ChartType="line",
                    y_scale="linear",
                    widget_key="dons_by_year_n_type")
        st.write("---")
    with tab3:
        mid, right = st.columns(2)
        with mid:
            if filtered_df.empty:
                st.write("No data available for the selected filters.")
                return
            else:
                plot_bar_line.plot_bar_line_by_year(
                    graph_df=filtered_df,
                    XValues="YearReceived",
                    YValues="Value",
                    GroupData="Party_Group",
                    XLabel="Year",
                    YLabel="Donations GBP",
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
                plot_bar_line.plot_bar_line_by_year(
                    graph_df=filtered_df,
                    XValues="YearReceived",
                    YValues="Value",
                    GroupData="DonationType",
                    XLabel="Year",
                    YLabel="Total Value GBP",
                    y_scale="log",
                    ChartType="Line",
                    LegendTitle="Donation Type",
                    Title="Donations GBP Types by Year",
                    widget_key="value_by_year_n_type",
                    CalcType='sum')
        st.write("---")
    with tab4:
        col1, col2 = st.columns(2)
        with col1:
            if filtered_df.empty:
                st.write("No data available for the selected filters.")
                return
            else:
                plot_pie_chart.plot_pie_chart(
                    graph_df=filtered_df,
                    XValues="Party_Group",
                    YValues="Value",  # Use None for count
                    color_column="Party_Group",
                    use_custom_colors=True,  # Use custom colors
                    color_map=None,
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
                plot_pie_chart.plot_pie_chart(
                    graph_df=filtered_df,
                    XValues="Party_Group",
                    YValues="EventCount",  # Use None for count
                    color_column="Party_Group",
                    use_custom_colors=True,  # Use custom colors
                    color_map=None,
                    Title="Distribution of Donations by Entity",
                    YLabel="Regulated Entity",
                    XLabel="Percentage of Donation Events",
                    hole=0.3,  # Adjust for more or less donut effect
                    widget_key="pie_donations_by_entity",
                    )
        st.write("---")
    with tab5:
        col1, col2 = st.columns(2)
        # Calculate the average donation per regular entity
        avg_donation = calculate_agg_by_variable(
            datafile=filtered_df,
            groupby_variable="PartyName",
            groupby_name="Party",
            agg_variable="Value",
            agg_type="mean",
            agg_name="Average Donation"
        )
        # display the average donation per entity on a
        # graph showing the top 10 and variance from the mean
        with col1:
            if filtered_df.empty:
                st.write("No data available for the selected filters.")
                return
            else:
                plot_bar_chart.plot_custom_bar_chart(
                    graph_df=filtered_df,
                    XValues="Party_Group",
                    YValues="Value",
                    group_column=None,
                    barmode="group",
                    orientation="v",
                    agg_func="avg",
                    use_custom_colors=True,
                    title="Average Donation per Party",
                    XLabel="Political Party",
                    YLabel="Average Donation GBP",
                    widget_key="avg_donations",
                    x_scale="category",
                    y_scale="linear",
                    )
        with col2:
            # diplay a table of the data
            st.write("### Average Donation per Party")
            avg_donation_sorted = (
                avg_donation.sort_values(by="Average Donation",
                                         ascending=False).head(10))
            avg_donation_sorted["Average Donation"] = (
                avg_donation_sorted["Average Donation"]
                .apply(lambda x: f"£{format_number(x)}"))
            st.dataframe(avg_donation_sorted, hide_index=True)
        st.write("---")
# End of hlf_body function
# Path: app_pages/headlinefigures.py
