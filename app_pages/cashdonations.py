def cashdonations_body():
    """
    Displays the content of the Cash Donations by Political Party page.
    """
    import streamlit as st
    import calculations as ppcalc
    import Visualisations as vis
    import datetime as dt

    # Load dataset from session state
    cleaned_df = st.session_state.get("data_clean", None)

    # # Ensure ReceivedDate is in datetime format
    # df["ReceivedDate"] = pd.to_datetime(df["ReceivedDate"], errors="coerce")

    # # Get min and max dates from the dataset
    min_date = ppcalc.get_mindate(cleaned_df).date()
    max_date = ppcalc.get_maxdate(cleaned_df).date()

    st.write("# Cash Donations to Political Parties")
    # # Extract start and end dates from the slider
    # start_date, end_date = date_range2
    start_date = dt.datetime.combine(min_date, dt.datetime.min.time())
    end_date = dt.datetime.combine(max_date, dt.datetime.max.time())
    # # Filter by date range
    date_filter = (cleaned_df["ReceivedDate"] >= start_date) & \
                  (cleaned_df["ReceivedDate"] <= end_date)

    # Apply filters
    filters = {}
    filters = None
    # Apply filters to the dataset
    cleaned_d_df = cleaned_df[date_filter]

    cleaned_c_d_df = cleaned_d_df[cleaned_d_df['DonationType'] == 'Cash']
    # Call each function separately with the selected filter
    unique_donors_c_d = ppcalc.get_donors_ct(cleaned_c_d_df, filters)
    total_value_donations_c_d = ppcalc.get_value_total(cleaned_c_d_df, filters)
    mean_value_donations_c_d = ppcalc.get_value_mean(cleaned_c_d_df, filters)
    unique_donations_c_d = ppcalc.get_donations_ct(cleaned_c_d_df, filters)
    unique_regulated_entities_c_d = ppcalc.get_regentity_ct(cleaned_c_d_df,
                                                            filters)
    unique_donations_d = ppcalc.get_donations_ct(cleaned_d_df, filters)
    unique_donations_pop = ppcalc.get_donations_ct(cleaned_df, filters)
    unique_donations_c = ppcalc.get_donations_ct(cleaned_df, {"DonationType":
                                                              "Cash"})
    perc_cash_donations = (unique_donations_c / unique_donations_pop) * 100 \
        if unique_donations_pop > 0 else 0
    perc_cash_donations_d = (unique_donations_c_d / unique_donations_d) * 100 \
        if unique_donations_d > 0 else 0
    min_date_df = ppcalc.get_mindate(cleaned_c_d_df, filters)
    max_date_df = ppcalc.get_maxdate(cleaned_c_d_df, filters)

    st.write("## Explaination")
    st.write("* The majority of donations to political parties are in cash."
             "These vary from small donations from individuals, to larger "
             "aggregated donations from multiple donors, and include "
             "donations from trade unions,business and bequests.")
    st.write("* These are identified by the regulator and marked in the data. "
             "This page provides a summary of the cash donations to political "
             "parties.")
    st.write("## Topline Figures")
    st.write(f"* During the period between {min_date_df} and {max_date_df}, "
             f"there were {unique_donations_c_d} cash donations made to "
             f"{unique_regulated_entities_c_d}.")
    st.write(f"* These had a mean value of £{ppcalc.format_number\
              (mean_value_donations_c_d)} "
             f"and were made by {ppcalc.format_number(unique_donors_c_d)} "
             "unique donors.")
    st.write(f"* Cash donations represented {perc_cash_donations_d:.2f}% of "
             "all donations during the period selected, and "
             f"{perc_cash_donations:.2f}% of all donations made to political "
             f"parties between {min_date} and {max_date},.")
    st.write(f"* All these had a value of £{ppcalc.format_number
             (total_value_donations_c_d)}")
    st.write("---")

    st.write("### Topline Visuals")
    st.write("#### Click on any Visualisation to view it full screen.")
    left, right = st.columns(2)
    with left:
        # visualisation of donations by party over time

        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            vis.plot_donations_by_year(cleaned_c_d_df,
                                       XValues="YearReceived",
                                       YValue="EventCount",
                                       GGroup="RegulatedEntityType",
                                       XLabel="Year", YLabel="Donations",
                                       Title="Donations by Year and "
                                       "Entity Type",
                                       CalcType='sum',
                                       widget_key="donations_by_entity",
                                       use_container_width=True)
    with right:
        # write function to find the top 3 RegulatedEntityTypes and share of
        # donations then update the text below.
        st.write('As can  be seen from the chart to the left'
                 'most cash donations are made to Political Parties.'
                 'This is not surprising as this is true for all '
                 'donations.')
        st.write('In 2016 we see an increase in donations to '
                 'Permitted Participants, this was due to the EU'
                 'Referendum, and the orgnaisations associated.')
    st.write('#### Cash Donations by Regulated Entity')
    left, right = st.columns(2)
    with left:
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            vis.plot_donations_by_year(cleaned_c_d_df,
                                       XValues="YearReceived",
                                       YValue="Value",
                                       GGroup="RegEntity_Group",
                                       XLabel="Year",
                                       YLabel="Value of Donations £",
                                       Title="Value of Donations by Year and"
                                             " Entity",
                                       CalcType='count',
                                       use_custom_colors=True,
                                       widget_key="Value_by_entity",
                                       use_container_width=True)
    with right:
        # write code to find top 3 political entities by value of donations and
        # update the text below
        st.write("The top 3 political entities by value of donations are "
                 "the Conservative Party, the Labour Party and the "
                 "Liberal Democrats. This is not surprising as these are "
                 "the three main political parties in the UK.")
        st.write("This pattern changes in 2016 to coincide with the EU "
                 "Referendum.  Here Medium size political entities such "
                 "as 'Vote Leave' and 'Leave.EU' were very active.")
    st.write('#### Cash Donations by Donor Type')
    left, right = st.columns(2)
    with left:
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            vis.plot_donations_by_year(cleaned_c_d_df,
                                       XValues="YearReceived",
                                       YValue="Value",
                                       GGroup="DonorStatus",
                                       XLabel="Year",
                                       YLabel="Total Value (£)",
                                       Title="Value of Donor Types by Year",
                                       CalcType='sum',
                                       widget_key="Value by type",
                                       use_container_width=True)
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
    with right:
        st.write("The visual shows unsurprisingly that most donations are made\
             by individuals.")
