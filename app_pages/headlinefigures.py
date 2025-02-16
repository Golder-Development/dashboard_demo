def hlf_body():
    """
    This function displays the content of Page two.
    """
    import streamlit as st
    import calculations as ppcalc
    import Visualisations as vis

    def format_number(value):
        if value >= 1_000_000:
            return f"{value / 1_000_000:,.1f}M"
        elif value >= 10_000:
            return f"{value / 1_000:,.1f}k"
        else:
            return f"{value:,.0f}"

    df = st.session_state.get("data_clean", None)
    sum_df = st.session_state.get("data_party_sum", None)
    # set filters to None and filtered_df to the original dataset
    filters = None
    filtered_df = df
    # Call each function separately with the selected filter
    unique_donors = ppcalc.get_donors_ct(filtered_df, filters)
    total_value_donations = ppcalc.get_value_total(filtered_df, filters)
    mean_value_donations = ppcalc.get_value_mean(filtered_df, filters)
    unique_donations = ppcalc.get_donations_ct(filtered_df, filters)
    unique_regulated_entities = ppcalc.get_regentity_ct(filtered_df, filters)
    min_date = ppcalc.get_mindate(filtered_df, filters).date()
    max_date = ppcalc.get_maxdate(filtered_df, filters).date()

    # Display the headline figures
    st.write("## Topline Summary of Political Donations to the UK Political "
             "Parties")
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Headline Figures")
        st.write(f"* During the period from {min_date} to {max_date}, {unique_regulated_entities:,.0f} "
                 "regulated political bodies received donations")
        st.write(f"* These received a total value of £{format_number(total_value_donations)} from {format_number(unique_donors)} unique donors")
        st.write(f"* The average donation was £{format_number(mean_value_donations)} and there were {format_number(unique_donations)} unique donations")
        # Add a graph comparing the number of donations per RegulatedEntity to the value of donations
        if sum_df is not None:
            vis.plot_regressionplot(
                sum_df,
                x_column="DonationEvents",
                y_column="DonationsValue",
                x_label="Total Donations",
                y_label="Donation Amount (£)",
                title="Impact of Donations on Political Entities"
            )
        else:
            st.error("Summary data not found. Please check dataset loading in the main app.")
        if filtered_df.empty:
            st.write("No data available for the selected filters.")
            return
        vis.plot_donations_by_year(filtered_df, XValues="YearReceived", YValue="EventCount", GGroup="RegulatedEntityType", XLabel="Year", YLabel="Donations", Title="Donations by Year and Entity Type")
    with col2:
        # use data from the summary dataset
        st.write("### Headline Visuals")
        if sum_df is not None:
            # Plot the pie chart
            vis.plot_pie_chart(sum_df, category_column="RegEntity_Group", title="Donations by Regulated Entity")
        else:
            st.error("Summary data not found. Please check dataset loading in the "
                     "main app.")
        if sum_df is not None:
            # Create the pie chart
            vis.plot_pie_chart(sum_df, category_column="RegEntity_Group", value_column="DonationsValue", title="Value of Donations by Regulated Entity")
        else:
            st.error("Summary data not found. Please check dataset loading in the "
                     "main app.")
        if filtered_df.empty:
            st.write("No data available for the selected filters.")
            return
        vis.plot_donations_by_year(filtered_df, XValues="YearReceived", YValue="Value", GGroup="RegEntity_Group", XLabel="Year", YLabel="Total Value (£)", Title="Donations by Year")
    st.write("### Click on any Visualisation to view it full screen.")
