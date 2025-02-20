def cashdonationsregentity_body():
    """
    Displays the content of the Cash Donations to Political Party page.
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
   # Define filter condition
    current_target = 'DonationType == "Cash"'
    Target_description = "Cash Donations"
    # Apply filters
    filters = {"RegulatedEntityId": selected_entity_id} if selected_entity_name != "All" else {}
    # # Filter by date range
    date_filter = (
        cleaned_df["ReceivedDate"] >= start_date) & (cleaned_df
                                                     ["ReceivedDate"]
                                                     <= end_date)
    # Create dataframe for chosen date range
    cleaned_d_df = cleaned_df[date_filter] if date_filter.any() else cleaned_df
    # Create dataframe for chosen target
    if filters:
        cleaned_c_df = cleaned_df = cleaned_df.query(current_target)
    else:
        cleaned_c_df = cleaned_df
    # Create dataframe for chosen entity
        if filters:
        cleaned_r_df = cleaned_df[
            cleaned_df["RegulatedEntityId"] == filters["RegulatedEntityId"]
            if filters else True  # If no filters, return all rows
        ]
    else:
        cleaned_r_df = cleaned_df
    # Create dataframe for chosen entity and date range
    cleaned_r_d_df = cleaned_r_df[date_filter] if date_filter.any() else cleaned_r_df
    # Create dataframe for chosen target and date range
    cleaned_c_d_df = cleaned_d_df.query(current_target)
    # Create dataframe for chosen target and entity
    cleaned_c_r_df = cleaned_r_df.query(current_target)
    # Create dataframe for chosen target, entity and date range
    cleaned_c_r_d_df = cleaned_r_d_df.query(current_target)
 
    # Values for all entities, all time and all donations
    unique_reg_ent_pop = ppcalc.get_regentity_ct(cleaned_df,
                                                            filters)
    unique_dono_pop = ppcalc.get_donors_ct(cleaned_df, filters)
    unique_dona_pop = ppcalc.get_donations_ct(cleaned_df, filters)
    total_value_pop = ppcalc.get_value_total(cleaned_df, filters)
    mean_value_pop = ppcalc.get_value_mean(cleaned_df, filters)
    # Values for all entities, chosen date range and all donations
    unique_reg_ent_d = ppcalc.get_regentity_ct(cleaned_d_df,
                                                            filters)
    unique_dono_d = ppcalc.get_donors_ct(cleaned_d_df, filters)
    unique_dona_d = ppcalc.get_donations_ct(cleaned_d_df, filters)
    total_value_d = ppcalc.get_value_total(cleaned_d_df, filters)
    mean_value_d = ppcalc.get_value_mean(cleaned_d_df, filters)
    # Values for all entities, all date range and target
    unique_reg_ent_c = ppcalc.get_regentity_ct(cleaned_c_df,
                                                            filters)
    unique_dono_c = ppcalc.get_donors_ct(cleaned_c_df, filters)
    unique_dona_c = ppcalc.get_donations_ct(cleaned_c_df, filters)
    total_value_c = ppcalc.get_value_total(cleaned_c_df, filters)
    mean_value_c = ppcalc.get_value_mean(cleaned_c_df, filters)
    # Values for chosen entity, all date range and all Donations
    unique_reg_ent_r = ppcalc.get_regentity_ct(cleaned_r_df,
                                                            filters)    
    unique_dono_r = ppcalc.get_donors_ct(cleaned_r_df, filters)
    unique_dona_r = ppcalc.get_donations_ct(cleaned_r_df, filters)
    total_value_r = ppcalc.get_value_total(cleaned_r_df, filters)
    mean_value_r = ppcalc.get_value_mean(cleaned_r_df, filters)
    # Values for all entities, chosen date range and current target
    unique_reg_ent_c_d = ppcalc.get_regentity_ct(cleaned_c_d_df,
                                                            filters)
    unique_dono_c_d = ppcalc.get_donors_ct(cleaned_c_d_df, filters)
    unique_dona_c_d = ppcalc.get_donations_ct(cleaned_c_d_df, filters)
    total_value_c_d = ppcalc.get_value_total(cleaned_c_d_df, filters)
    mean_value_c_d = ppcalc.get_value_mean(cleaned_c_d_df, filters)
    # Values for chosen entity, date range and all donations
    unique_reg_ent_r_d = ppcalc.get_regentity_ct(cleaned_r_d_df,
                                                            filters)
    unique_dono_r_d = ppcalc.get_donors_ct(cleaned_r_d_df, filters)
    unique_dona_r_d = ppcalc.get_donations_ct(cleaned_r_d_df, filters)
    total_value_r_d = ppcalc.get_value_total(cleaned_r_d_df, filters)
    mean_value_r_d = ppcalc.get_value_mean(cleaned_r_d_df, filters)
    # Values for chosen entity, date range and all donations
    unique_reg_ent_c_r = ppcalc.get_regentity_ct(cleaned_c_r_df,
                                                            filters)  
    unique_dono_c_r = ppcalc.get_donors_ct(cleaned_c_r_df, filters)
    unique_dona_c_r = ppcalc.get_donations_ct(cleaned_c_r_df, filters)
    total_value_c_r = ppcalc.get_value_total(cleaned_c_r_df, filters)
    mean_value_c_r = ppcalc.get_value_mean(cleaned_c_r_df, filters)
    # Values for chosen entity, date range and current target
    unique_reg_ent_c_r_d = ppcalc.get_regentity_ct(cleaned_c_r_d_df,
                                                            filters)  
    unique_dono_c_r_d = ppcalc.get_donors_ct(cleaned_c_r_d_df, filters)
    unique_dona_c_r_d = ppcalc.get_donations_ct(cleaned_c_r_d_df, filters)
    total_value_c_r_d = ppcalc.get_value_total(cleaned_c_r_d_df,
                                                         filters)
    mean_value_c_r_d = ppcalc.get_value_mean(cleaned_c_r_d_df,
                                                       filters)
    # Relative relationship calculations    
    # percent of target donations for all entities and all time period
    # to all donations for all entries and all time period
    perc_c_V_pop = (
        (unique_dona_c / unique_dona_pop) * 100
        if unique_dona_pop > 0 else 0
        )
    # Percent of all donations for chosen entity
    # to all donations for all entities and all time period
    perc_r_V_pop = (
        (unique_dona_r / unique_dona_pop) * 100
        if unique_dona_pop > 0 else 0
        )
    # Percent of all donations for all entities in time period
    # to all donations for all entities and all time period
    perc_d_V_pop = (
        (unique_dona_d / unique_dona_pop) * 100
        if unique_dona_pop > 0 else 0
        )
    # Percent of target donations in time period
    # to all donations for all entity in time period
    perc_c_d_V_d = (
        (unique_dona_c_d / unique_dona_d) * 100
        if unique_dona_d > 0 else 0
        )
    # Percent of all donations for chosen entity in time period
    # to all donations for all entities in time period
    perc_r_d_V_c = (
        (unique_dona_r_d / unique_dona_d) * 100
        if unique_dona_d > 0 else 0
        )
    # Percent of target donations in time period for chosen entity
    # to target donations for all entities and all time period
    perc_c_r_d_V_c = (
        (unique_dona_c_r_d / unique_dona_c) * 100
        if unique_dona_c > 0 else 0
        )



    # Percent of all donations for chosen entity in time period
    # to all donations for chosen entities in time period
    
    
    # Percent value share of time period donations
    # to all donations for all entities and all time period
    perc_value_share_pop = (
        (total_value_d / total_value_pop) * 100
        if total_value_pop > 0 else 0
    )
    # Percent Value of target donations in time period 
    # to all donations for all entities and all time period
    perc_value_share_c_d = (
        (total_value_c_d / total_value_pop) * 100
        if total_value_pop > 0 else 0
        )
    # Percent Value of target donations for entity all time 
    # to target donations for all entities and all time period
    perc_value_share_c_r = (
        (total_value_c_r / total_value_pop) * 100
        if total_value_pop > 0 else 0
        )

    # Percent of target donations in time period for chosen entity
    # to all donations for all entities and targetted time period
    perc_dona_c_r = (unique_dona_c_r_d / unique_dona_d) * 100\
        if unique_dona_d > 0 else 0
    # Percent of target donations in time period for chosen entity
    # to target donations for all entities and all time period    
    perc_dona_d = (unique_dona_d / unique_dona_pop) * 100\
        if unique_dona_d > 0 else 0
    
    
    # Format selected dates for inclusion in text
    min_date_df = start_date.date()
    max_date_df = end_date.date()

    st.write(f"## Topline Figures for Cash Donations to {selected_entity_name}"
             f" between {min_date_df} and {max_date_df}")
    st.write(f"* During the period between {min_date_df} and {max_date_df}, "
             f"there were {unique_dona_c_d:,.0f} cash donations made to "
             f"{selected_entity_name}.  These had an average value of "
             f"£{ppcalc.format_number(mean_value_c_d)} "
             f"and were made by {ppcalc.format_number(unique_dono_c_d)} "
             "unique donors. These donations totalled "
             f"£{ppcalc.format_number(total_value_c_d)}"
             f" and represented {perc_target_dona_c_d:.2f}% of"
             f" all donations made "
             f" to {selected_entity_name}"
             " during the period selected.")
    
    if unique_dona_c_d < unique_dona_r_d:
             st.write("* During the period they received a total of"
                      f" {unique_dona_r_d:,.0f} donations with a total value of"
                      f" £{ppcalc.format_number(total_value_r_d)} and an"
                      " average value of "
                      f"£{ppcalc.format_number(mean_value_r_d)}"
                      f" from {unique_dono_r_d:,.0f} unique donors.")
             
    # Compare percentage of cash donations to chosen entity vs avergage
    # percentage cash donations for all entities
    perc_targ_d >target_donations_pop:
        st.write("* The percentage of cash donations made"
                 f" to {selected_entity_name} "
                 f" targ_d:.is "
                 "higher than the average"
                 "percentage of cash donations made to all entities"
                 f" ({perc_target_donations_pop:.2f}%)")
    eltarg_d <target_donations_pop:
        st.write("* The percentage of cash donations made "
                 f"to {selected_entity_name} "
                 ftarg_d:.is lower than the"
                 " average percentage of cash donations made to all entities"
                 f" ({perc_target_donations_pop:.2f}%)")
    else:
        st.write("* The percentage of cash donations made to "
                 f"{selected_entity_name} "
                 ftarg_d:.is "
                 "the same as the average"
                 " percentage of cash donations made to all entities"
                 f" ({perc_target_donations_pop:.2f}%)")
    # Compare value share of cash donations to value of all chosen entity
    # donations vs avergage value share of cash donations for all entities
    if perc_value_share_c_d > perc_value_share_pop:
        st.write("* The value of cash donations "
                 " as a percentage of all donations made to "
                 f"{selected_entity_name} "
                 f"({perc_value_share_c_d:.2f}%) is higher than the average"
                 " value of cash donations made to all entities"
                 f" ({perc_value_share_pop:.2f}%)")
    elif perc_value_share_c_d < perc_value_share_pop:
        st.write("* The value of cash donations made to"
                 f"{selected_entity_name} "
                 f"({perc_value_share_c_d:.2f}%) is lower than the average"
                 " value of cash donations made to all entities"
                 f" ({perc_value_share_pop:.2f}%)")
    else:
        st.write("* The value of cash donations made "
                 f"to {selected_entity_name} "
                 f"({perc_value_share_c_d:.2f}%) is the same as the average"
                 f" value of cash donations made to all entities"
                 f" ({perc_value_share_pop:.2f}%)")
    # Compare number of donors to chosen entity vs
    # avergage number of donors for all entities
    if unique_donors_c_d > unique_donors_pop:
        st.write(f"* The number of unique donors to {selected_entity_name} "
                 f"({ppcalc.format_number(unique_donors_c_d)}) is higher than"
                 f" the average number of unique donors to all entities"
                 f" ({ppcalc.format_number(unique_donors_pop)})")
    elif unique_donors_c_d < unique_donors_pop:
        st.write(f"* The number of unique donors to {selected_entity_name} "
                 f"({ppcalc.format_number(unique_donors_c_d)}) is lower than"
                 f"the average number of unique donors to all entities"
                 f" ({ppcalc.format_number(unique_donors_pop)})")
    else:
        st.write(f"* The number of unique donors to {selected_entity_name} "
                 f"({ppcalc.format_number(unique_donors_c_d)}) is the same"
                 f" as the average number of unique donors to all entities"
                 f" ({ppcalc.format_number(unique_donors_pop)})")
    # Compare average value of donations to chosen entity vs
    # avergage average value of donations for all entities
    if mean_value_donations_c_d > mean_value_pop:
        st.write(f"* The average value of donations to {selected_entity_name} "
                 f"(£{ppcalc.format_number(mean_value_donations_c_d)}) is"
                 f" higher than the average average value of donations to"
                 f" all entities (£{ppcalc.format_number(mean_value_pop)})")
    elif mean_value_donations_c_d < mean_value_pop:
        st.write(f"* The average value of donations to {selected_entity_name} "
                 f"(£{ppcalc.format_number(mean_value_donations_c_d)}) is"
                 f" lower than the average average value of donations to all "
                 f"entities (£{ppcalc.format_number(mean_value_pop)})")
    else:
        st.write(f"* The average value of donations to {selected_entity_name} "
                 f"(£{ppcalc.format_number(mean_value_donations_c_d)}) is the"
                 f" same as the average average value of donations to all"
                 f" entities (£{ppcalc.format_number(mean_value_pop)})")
    if min_date_df != min_date or max_date_df != max_date:
        # Compare percentage of cash donations to chosen entity vs
        # percentage of all donations
        st.write("---")
        st.write(f"#### Comparison of activity between {min_date_df} and"
                 f" {max_date_df} to activity between {min_date} and {max_date}")
        st.write("---")
        st.write(f"* The percentage of cash donations to {selected_entity_name} "
                ftarg_d:.compared to the"
                " percentage of all donations "
                f"({perc_donations_d:.2f}%) during the selected date range.")

        # Compare value share of cash donations to chosen entity vs
        # value share of all donations
        st.write(f"* The value share of cash donations to {selected_entity_name} "
                f"({perc_value_share_c_d:.2f}%) compared to the value"
                " share of all donations "
                f"({perc_value_share_pop:.2f}%) during the selected date range.")

        # Compare number of unique donors to chosen entity vs
        # number of unique donors for all entities
        st.write(f"* The number of unique donors to {selected_entity_name} "
                f"({unique_donors_c_r_d}) compared to the number of "
                "unique donors for all entities "
                f"({unique_donors_pop}) during the selected date range.")

        # Compare average value of donations to chosen entity vs
        # average value of donations for all entities
        st.write(f"* The average value of donations to {selected_entity_name} "
                f"(£{ppcalc.format_number(mean_value_donations_c_r_d)}) compared"
                " to the average value of donations for all entities "
                f"(£{ppcalc.format_number(mean_value_pop)}) during the"
                " selected date range.")
    else:
        "No date range selected."
        st.write("---")

    st.write("### Topline Visuals for Cash Donations"
             f" to {selected_entity_name}"
             f" between {min_date_df} and {max_date_df}")
    st.write("#### Click on any Visualisation to view it full screen.")
    left, right = st.columns(2)
    with left:
        # visualisation of donations by party over time

        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            vis.plot_bar_line_by_year(cleaned_c_d_df,
                                      XValues="YearReceived",
                                      YValue="EventCount",
                                      GGroup="RegulatedEntityType",
                                      XLabel="Year", YLabel="Donations",
                                      Title="Donations by Year and Entity "
                                      "Type",
                                      CalcType='sum',
                                      widget_key="cash_dons_by_party")
        st.write('As can  be seen from the chart to the left'
                 'most cash donations are made to Political Parties.'
                 'This is not surprising as this is true for all '
                 'donations.')
    with right:
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            vis.plot_bar_line_by_year(cleaned_c_d_df,
                                      XValues="YearReceived",
                                      YValue="Value",
                                      GGroup="RegEntity_Group",
                                      XLabel="Year",
                                      YLabel="Value of Donations £",
                                      Title="Value of Donations by Year "
                                      "and Entity",
                                      CalcType='count',
                                      use_custom_colors=True,
                                      widget_key="cash_dons_by_reg_entity")
        # write code to return analysis of the graph above highlighting
        # interesting factors that will refresh when the input changes.

        st.write("### description")
    left, right = st.columns(2)
    with left:
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            vis.plot_bar_line_by_year(cleaned_c_d_df,
                                      XValues="YearReceived",
                                      YValue="Value",
                                      GGroup="DonationType",
                                      XLabel="Year",
                                      YLabel="Total Value (£)",
                                      Title="Value of Donations Types "
                                      "by Year",
                                      CalcType='sum',
                                      widget_key="cash_dons_by_type")
    with right:
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            "analysis of the graph above highlighting interesting factors"
            "that will refresh when the input changes."
