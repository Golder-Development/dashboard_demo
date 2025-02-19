def hlf_body():
    """
    This function displays the content of Page two.
    """
    import streamlit as st
    import calculations as ppcalc
    import Visualisations as vis

    df = st.session_state.get("data_clean", None)
    # sum_df = st.session_state.get("data_party_sum", None)
    # set filters to None and filtered_df to the original dataset
    filters = None
    filtered_df = df
    # Call each function separately with the selected filter
    unique_donors = ppcalc.get_donors_ct(filtered_df, filters)
    total_value_donations = ppcalc.get_value_total(filtered_df, filters)
    mean_value_donations = ppcalc.get_value_mean(filtered_df, filters)
    unique_donations = ppcalc.get_donations_ct(filtered_df, filters)
    unique_regulated_entities = ppcalc.get_regentity_ct(filtered_df, filters)
    PP_donations = ppcalc.get_donationtype_ct(
        filtered_df, {"DonorStatus": "Registered Political Party"}
    )
    PP_donations_value = ppcalc.get_value_total(
        filtered_df, {"DonorStatus": "Registered Political Party"}
    )
    PP_donations_percent = (
        (PP_donations / unique_donations) * 100
        if total_value_donations > 0
        else 0
    )
    PP_donations_value_percent = (
        (PP_donations_value / total_value_donations) * 100
        if total_value_donations > 0
        else 0
    )
    single_donation_entity = ppcalc.get_donations_ct(
        filtered_df, {"RegEntity_Group": "Single Donation Entity"}
    )
    single_donation_entity_value = ppcalc.get_value_total(
        filtered_df, {"RegEntity_Group": "Single Donation Entity"}
    )
    single_donation_percent = (
        (single_donation_entity / unique_donations) * 100
        if total_value_donations > 0
        else 0
    )
    single_donation_entity_value_percent = (
        (single_donation_entity_value / total_value_donations) * 100
        if total_value_donations > 0
        else 0
    )
    single_donation_entity_percent = (
        (single_donation_entity / unique_regulated_entities) * 100
        if total_value_donations > 0
        else 0
    )
    min_date = ppcalc.get_mindate(filtered_df, filters).date()
    max_date = ppcalc.get_maxdate(filtered_df, filters).date()

    # Get the regulated entity with the greatest value of donations
    top_entity, top_value = ppcalc.get_top_entity_by_value(
        filtered_df, filters
    )
    # Get the regulated entity with the greatest number of donations
    top_entity_ct, top_donations = ppcalc.get_top_entity_by_donations(
        filtered_df, filters)
    # Get the donationtype with the greatest number of donations
    top_dontype_ct, top_dontype_dons = ppcalc.get_top_donType_by_don(
        filtered_df, filters)
    # Get the donationtype with the greatest number of donations
    top_dontype_value = ppcalc.get_value_total(
        filtered_df, {'DonationType': top_dontype_ct}
    )
    top_dontype_value_percent = (
        (top_dontype_value / total_value_donations) * 100
        if total_value_donations > 0
        else 0
    )
    top_dontype_dons_percent = (
        (top_dontype_dons / unique_donations) * 100
        if total_value_donations > 0
        else 0
    )

    # Display the headline figures
    st.write("## Topline Summary of Political Donations to the UK Political "
             "Parties")
    st.write("### Headline Figures")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"* During the period from {min_date} to {max_date}, "
                 f"{unique_regulated_entities:.0f} regulated political "
                 "bodies received donations.")
        st.write(
            "* These received a total value of "
            f"£{ppcalc.format_number(total_value_donations)} "
            f"from {ppcalc.format_number(unique_donors)} unique donors"
        )
        st.write(
            f"* The average donation was "
            f"£{ppcalc.format_number(mean_value_donations)} "
            f"and there were {ppcalc.format_number(unique_donations)}"
            " unique donations"
        )
        st.write(
            f"* Political parties were identified as the "
            f"donor in {PP_donations_percent:.0f}% "
            f"of dontations. These donations were worth"
            f" £{ppcalc.format_number(PP_donations_value)} "
            f"or {PP_donations_value_percent:.2f}% of the total "
            "value of donations."
        )
        st.write(
            f"* {single_donation_entity} of the donations were to entities"
            f"that only received one donation. These donations represented "
            f"{single_donation_percent:.2f}% of all donations, were worth "
            f" £{ppcalc.format_number(single_donation_entity_value)} or "
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
            f"a total value of £{ppcalc.format_number(top_value)} or "
            f"{top_value/total_value_donations*100:.2f}% of all donations.")
        st.write(
            f"* The {top_entity_ct} received the most donations by count, "
            f"having {top_donations:,.0f} donations which represented "
            f"{top_donations/unique_donations*100:.2f}% of all donations.")
    st.write("### Topline Visuals")
    st.write("#### Click on any Visualisation to view it full screen.")
    mid, right = st.columns(2)
    with mid:
        if filtered_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            vis.plot_bar_line_by_year(filtered_df,
                                      XValues="YearReceived",
                                      YValue="EventCount",
                                      GGroup="RegulatedEntityType",
                                      XLabel="Year", YLabel="Donations",
                                      Title="Donations per Year & Entity Type",
                                      CalcType='sum',
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
                                      YValue="EventCount",
                                      GGroup="Data Safety Score",
                                      XLabel="Year", YLabel="Donations",
                                      Title="Donations by Year and Type",
                                      CalcType='sum',
                                      ChartType="Line",
                                      y_scale="log",
                                      widget_key="dons_by_year_n_type")
    mid, right = st.columns(2)
    with mid:
        if filtered_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            vis.plot_bar_line_by_year(filtered_df,
                                      XValues="YearReceived",
                                      YValue="Value",
                                      GGroup="RegEntity_Group",
                                      XLabel="Year",
                                      YLabel="Value of Donations £ 000's",
                                      Title="Donations GBP by Year & Entity",
                                      use_custom_colors=True,
                                      widget_key="value_by_year_n_entity",
                                      CalcType='sum')
    with right:
        if filtered_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            vis.plot_bar_line_by_year(filtered_df,
                                      XValues="YearReceived",
                                      YValue="Value",
                                      GGroup="DonationType",
                                      XLabel="Year",
                                      YLabel="Total Value (£)",
                                      y_scale="log",
                                      ChartType="Line",
                                      Title="Donations GBP Types by Year",
                                      widget_key="value_by_year_n_type",
                                      CalcType='sum')
    col1, col2 = st.columns(2)
    with col1:
        if filtered_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            st.write("### Entity Distribution")
            vis.plot_pie_chart(
                df=filtered_df,
                category_column="RegEntity_Group",
                value_column="Value",  # Use None for count
                color_column="RegEntity_Group",
                title="Distribution of Donated Value by Entity",
                category_label="Regulated Entity",
                value_label="Percentage of Total Donations",
                use_custom_colors=True,  # Use custom colors
                hole=0.3,  # Adjust for more or less donut effect
                widget_key="Value_by_entity"
            )
    with col2:
        if filtered_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            st.write("### Entity Distribution")
            vis.plot_pie_chart(
                df=filtered_df,
                category_column="RegEntity_Group",
                value_column=None,  # Use None for count
                color_column="RegEntity_Group",
                title="Distribution of Donations by Entity",
                category_label="Regulated Entity",
                use_custom_colors=True,  # Use custom colors
                value_label="Percentage of Donation Events",
                hole=0.3,  # Adjust for more or less donut effect
                widget_key="pie_donations_by_entity"
            )
