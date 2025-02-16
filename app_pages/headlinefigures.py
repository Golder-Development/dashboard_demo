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
    cash_donations = ppcalc.get_donationtype_ct(filtered_df, {"DonationType": "Cash"})
    cash_don_percent = (cash_donations / unique_donations) * 100 if total_value_donations > 0 else 0
    cash_donations_value = ppcalc.get_value_total(filtered_df, {"DonationType": "Cash"})
    cash_don_value_percent = (cash_donations_value / total_value_donations) * 100 if total_value_donations > 0 else 0
    PP_donations = ppcalc.get_donationtype_ct(filtered_df, {"DonorStatus": "Registered Political Party"})
    PP_donations_value = ppcalc.get_value_total(filtered_df, {"DonorStatus": "Registered Political Party"})
    PP_donations_percent = (PP_donations / unique_donations) * 100 if total_value_donations > 0 else 0
    PP_donations_value_percent = (PP_donations_value / total_value_donations) * 100 if total_value_donations > 0 else 0
    
    min_date = ppcalc.get_mindate(filtered_df, filters).date()
    max_date = ppcalc.get_maxdate(filtered_df, filters).date()

    # Get the regulated entity with the greatest value of donations
    top_entity, top_value = ppcalc.get_top_entity_by_value(filtered_df, filters)
    # Get the regulated entity with the greatest number of donations
    top_entity_ct, top_donations = ppcalc.get_top_entity_by_donations(filtered_df, filters)
    # Get the donationtype with the greatest number of donations
    top_dontype_ct, top_dontype_dons = ppcalc.get_top_donationType_by_donations(filtered_df, filters)
    # Get the donationtype with the greatest number of donations
    top_dontype_value = ppcalc.get_value_total(filtered_df,{'DonationType':top_dontype_ct})
    top_dontype_value_percent = (top_dontype_value / total_value_donations) * 100 if total_value_donations > 0 else 0
    top_dontype_dons_percent = (top_dontype_dons / unique_donations) * 100 if total_value_donations > 0 else 0

    # Display the headline figures
    st.write("## Topline Summary of Political Donations to the UK Political "
             "Parties")
    st.write("### Headline Figures")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"* During the period from {min_date} to {max_date},  {unique_regulated_entities:.0f} "
                 "regulated political bodies received donations.")
        st.write(f"* These received a total value of £{format_number(total_value_donations)} from {format_number(unique_donors)} unique donors")
        st.write(f"* The average donation was £{format_number(mean_value_donations)} and there were {format_number(unique_donations)} unique donations")
        st.write(f"* Political parties were identified as the donor in {PP_donations_percent:.0f}% of dontations. These donations were worth £{format_number(cash_donations_value)} or {PP_donations_value_percent:.2f}% of the total value of donations.")
    with col2:
        st.write(f"* Most Donations were in {top_dontype_ct}, these represented {top_dontype_dons_percent:.2f}% of donations and were {top_dontype_value_percent:.2f}% of the total value of donations.")    
        # use data from the summary dataset
        st.write(f"* The {top_entity} received the most donations by value, with a total value of £{format_number(top_value)} or {top_value/total_value_donations*100:.2f}% of all donations.") 
        st.write(f"* The {top_entity_ct} received the most donations by count, having {top_donations:,.0f} donations which represented {top_donations/unique_donations*100:.2f}% of all donations.")
    st.write("### Topline Visuals")
    st.write("#### Click on any Visualisation to view it full screen.") 
    if filtered_df.empty:
        st.write("No data available for the selected filters.")
        return
    else:
        vis.plot_donations_by_year(filtered_df, XValues="YearReceived", YValue="EventCount", GGroup="RegulatedEntityType", XLabel="Year", YLabel="Donations", Title="Donations by Year and Entity Type")
    if filtered_df.empty:
        st.write("No data available for the selected filters.")
        return
    else:
        vis.plot_donations_by_year(filtered_df, XValues="YearReceived", YValue="Value", GGroup="RegEntity_Group", XLabel="Year", YLabel="Total Value (£)", Title="Value of Donations by Year")


