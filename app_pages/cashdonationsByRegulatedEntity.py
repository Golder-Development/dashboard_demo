def cashdonationsregentity_body():
    """
    Displays the content of the Cash Donations by Political Party page.
    """
    import streamlit as st
    import calculations as ppcalc
    import Visualisations as vis
    import datetime as dt
    import pandas as pd
    # Load dataset from session state
    cleaned_df = st.session_state.get("data_clean", None)

    # # Ensure ReceivedDate is in datetime format
    # df["ReceivedDate"] = pd.to_datetime(df["ReceivedDate"], errors="coerce")

    # # Get min and max dates from the dataset
    min_date = ppcalc.get_mindate(cleaned_df).date()
    max_date = ppcalc.get_maxdate(cleaned_df).date()

    st.write("# Cash Donations: Political Entity and Date Range")
    # # Add a date range slider to filter by received date
    date_range2 = st.slider(
        "Select Date Range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )

    # # Extract start and end dates from the slider
    start_date, end_date = date_range2
    start_date = dt.datetime.combine(start_date, dt.datetime.min.time())
    end_date = dt.datetime.combine(end_date, dt.datetime.max.time())

    # # Filter by date range
    date_filter = (cleaned_df["ReceivedDate"] >= start_date) & (cleaned_df
                                                                ["ReceivedDate"]
                                                                <= end_date)

    # --- Dropdown for Regulated Entity ---
    # Create a mapping of RegulatedEntityName -> RegulatedEntityId
    entity_mapping = dict(zip(cleaned_df["RegulatedEntityName"], cleaned_df
                              ["RegulatedEntityId"]))

    # Add "All" as an option and create a dropdown that displays names but
    # returns IDs
    selected_entity_name = st.selectbox("Filter by Regulated Entity", ["All"]
                                        + sorted(entity_mapping.keys()))

    # Get the corresponding ID for filtering
    selected_entity_id = entity_mapping.get(selected_entity_name, None)

    # Apply filters
    filters = {"RegulatedEntityId": selected_entity_id} if\
        selected_entity_name != "All" else None

    # Apply filters to the dataset
    cleaned_d_df = cleaned_df[date_filter]

    if filters:
        cleaned_r_d_df = cleaned_d_df[cleaned_d_df["RegulatedEntityId"] ==
                                      filters["RegulatedEntityId"]]
    else:
        cleaned_r_d_df = cleaned_d_df

    cleaned_c_r_d_df = cleaned_r_d_df[cleaned_r_d_df['DonationType'] == 'Cash']
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
    perc_cash_donations = (unique_donations_c / unique_donations_pop) * 100 if\
        unique_donations_pop > 0 else 0
    perc_cash_donations_d = (unique_donations_c_d / unique_donations_d) * 100\
        if unique_donations_d > 0 else 0
    min_date_df = ppcalc.get_mindate(cleaned_c_d_df, filters)
    max_date_df = ppcalc.get_maxdate(cleaned_c_d_df, filters)

    st.write("## Explaination")
    st.write("* The majority of donations to political parties are in cash."
             "These vary from small donations from individuals, to larger "
             "aggregated donations from multiple donors, and include "
             "donations from trade unions, business and bequests.")
    st.write("* These are identified by the regulator and marked in the data. "
             "This page provides a summary of the cash donations to political "
             "parties.")
    st.write("## Topline Figures")
    st.write(f"* During the period between {min_date_df} and {max_date_df},"
             f"there were {unique_donations_c_d} cash donations made to "
             f"{unique_regulated_entities_c_d}.")
    st.write(f"* These had a mean value of £{ppcalc.format_number
             (mean_value_donations_c_d)} "
             f"and were made by {ppcalc.format_number(unique_donors_c_d)} "
             "unique donors.")
    st.write(f"* Cash donations represented {perc_cash_donations_d:.2f}% of"
             f"all donations during the period selected and had a value of "
             f"£{ppcalc.format_number(total_value_donations_c_d)}")
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
                                       Title="Donations by Year and Entity "
                                       "Type",
                                       CalcType='sum',
                                       widget_key="cash_dons_by_party")
    with right:
        st.write('As can  be seen from the chart to the left'
                 'most cash donations are made to Political Parties.'
                 'This is not surprising as this is true for all '
                 'donations.')
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
                                       Title="Value of Donations by Year "
                                       "and Entity",
                                       CalcType='count',
                                       widget_key="cash_dons_by_reg_entity")
    with right:
        # write code to return analysis of the graph above highlighting
        # interesting factors that will refresh when the input changes.

        st.write("### description")
    left, right = st.columns(2)
    with left:
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            vis.plot_donations_by_year(cleaned_c_d_df,
                                       XValues="YearReceived",
                                       YValue="Value",
                                       GGroup="DonationType",
                                       XLabel="Year",
                                       YLabel="Total Value (£)",
                                       Title="Value of Donations Types "
                                       "by Year",
                                       CalcType='sum',
                                       widget_key="cash_dons_by_type")
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
