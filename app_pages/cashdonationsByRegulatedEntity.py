def cashdonationsregentity_body():
    """
    Displays the content of the Cash Donations to Political Party page.
    """
    import streamlit as st
    import components.calculations as ppcalc
    import components.Visualisations as vis
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
    target_label = "Cash Donation"
    filters = None
    # Apply filters
    entity_filter = (
        {"RegulatedEntityId": selected_entity_id}
        if selected_entity_name != "All" else {}
                    )
    # # Filter by date range
    date_filter = (
        cleaned_df["ReceivedDate"] >= start_date) & (cleaned_df
                                                     ["ReceivedDate"]
                                                     <= end_date)
    # Create dataframe for chosen date range and all entities
    if date_filter is not None:
        cleaned_d_df = cleaned_df[date_filter]
    else:
        cleaned_d_df = cleaned_df
    # Create dataframe for chosen target all date range and all entities
    if current_target:
        cleaned_c_df = cleaned_df.query(current_target)
    else:
        cleaned_c_df = cleaned_df
    # Create dataframe for chosen entity all date range and all entities
    if entity_filter:
        cleaned_r_df = (
            cleaned_df[
                cleaned_df["RegulatedEntityId"]
                == entity_filter["RegulatedEntityId"]
                if entity_filter else True  # If no filters, return all rows
                      ]
                       )
    else:
        cleaned_r_df = cleaned_df
    # Create dataframe for chosen entity and date range all measures
    cleaned_r_d_df = (
        cleaned_r_df[date_filter] if date_filter.any() else cleaned_r_df
        )
    # Create dataframe for chosen target and date range all entities
    cleaned_c_d_df = cleaned_d_df.query(current_target)
    # Create dataframe for chosen target and entity all dates
    cleaned_c_r_df = cleaned_r_df.query(current_target)
    # Create dataframe for chosen target, entity and date range
    cleaned_c_r_d_df = cleaned_r_d_df.query(current_target)

    # Values for all entities, all time and all donations
    unique_reg_ent_pop = ppcalc.get_regentity_ct(cleaned_df, filters)
    unique_dono_pop = ppcalc.get_donors_ct(cleaned_df, filters)
    unique_dona_pop = ppcalc.get_donations_ct(cleaned_df, filters)
    total_val_pop = ppcalc.get_value_total(cleaned_df, filters)
    mean_val_pop = ppcalc.get_value_mean(cleaned_df, filters)
    avg_dona_pop = ppcalc.get_avg_donations_per_entity(cleaned_df, filters)
    avg_val_pop = ppcalc.get_avg_value_per_entity(cleaned_df, filters)
    avg_dono_pop = ppcalc.get_avg_donors_per_entity(cleaned_df, filters)
    std_dona_pop = ppcalc.get_donors_stdev(cleaned_df, filters)
    std_val_pop = ppcalc.get_value_stdev(cleaned_df, filters)
    std_dono_pop = ppcalc.get_noofdonors_per_ent_stdev(cleaned_df, filters)

    # Values for all entities, chosen date range and all donations
    unique_reg_ent_d = ppcalc.get_regentity_ct(cleaned_d_df, filters)
    unique_dono_d = ppcalc.get_donors_ct(cleaned_d_df, filters)
    unique_dona_d = ppcalc.get_donations_ct(cleaned_d_df, filters)
    total_val_d = ppcalc.get_value_total(cleaned_d_df, filters)
    mean_val_d = ppcalc.get_value_mean(cleaned_d_df, filters)
    avg_dona_pop_d = ppcalc.get_avg_donations_per_entity(cleaned_d_df, filters)
    avg_val_pop_d = ppcalc.get_avg_value_per_entity(cleaned_d_df, filters)
    avg_dono_pop_d = ppcalc.get_avg_donors_per_entity(cleaned_d_df, filters)
    std_dona_pop_d = ppcalc.get_donors_stdev(cleaned_d_df, filters)
    std_val_pop_d = ppcalc.get_value_stdev(cleaned_d_df, filters)
    std_dono_pop_d = ppcalc.get_noofdonors_per_ent_stdev(cleaned_d_df, filters)

    # Values for all entities, all date range and target
    unique_reg_ent_c = ppcalc.get_regentity_ct(cleaned_c_df, filters)
    unique_dono_c = ppcalc.get_donors_ct(cleaned_c_df, filters)
    unique_dona_c = ppcalc.get_donations_ct(cleaned_c_df, filters)
    total_val_c = ppcalc.get_value_total(cleaned_c_df, filters)
    mean_val_c = ppcalc.get_value_mean(cleaned_c_df, filters)
    avg_dona_pop_c = ppcalc.get_avg_donations_per_entity(cleaned_c_df, filters)
    avg_val_pop_c = ppcalc.get_avg_value_per_entity(cleaned_c_df, filters)
    avg_dono_pop_c = ppcalc.get_avg_donors_per_entity(cleaned_c_df, filters)
    std_dona_pop_c = ppcalc.get_donors_stdev(cleaned_c_df, filters)
    std_val_pop_c = ppcalc.get_value_stdev(cleaned_c_df, filters)
    std_dono_pop_c = ppcalc.get_noofdonors_per_ent_stdev(cleaned_c_df, filters)

    # Values for chosen entity, all date range and all Donations
    unique_reg_ent_r = ppcalc.get_regentity_ct(cleaned_r_df, filters)
    unique_dono_r = ppcalc.get_donors_ct(cleaned_r_df, filters)
    unique_dona_r = ppcalc.get_donations_ct(cleaned_r_df, filters)
    total_val_r = ppcalc.get_value_total(cleaned_r_df, filters)
    mean_val_r = ppcalc.get_value_mean(cleaned_r_df, filters)
    avg_dona_pop_r = ppcalc.get_avg_donations_per_entity(cleaned_r_df, filters)
    avg_val_pop_r = ppcalc.get_avg_value_per_entity(cleaned_r_df, filters)
    avg_dono_pop_r = ppcalc.get_avg_donors_per_entity(cleaned_r_df, filters)
    std_dona_pop_r = ppcalc.get_donors_stdev(cleaned_r_df, filters)
    std_val_pop_r = ppcalc.get_value_stdev(cleaned_r_df, filters)
    std_dono_pop_r = ppcalc.get_noofdonors_per_ent_stdev(cleaned_r_df, filters)

    # Values for all entities, chosen date range and current target
    unique_reg_ent_c_d = ppcalc.get_regentity_ct(cleaned_c_d_df, filters)
    unique_dono_c_d = ppcalc.get_donors_ct(cleaned_c_d_df, filters)
    unique_dona_c_d = ppcalc.get_donations_ct(cleaned_c_d_df, filters)
    total_val_c_d = ppcalc.get_value_total(cleaned_c_d_df, filters)
    mean_val_c_d = ppcalc.get_value_mean(cleaned_c_d_df, filters)
    avg_dona_pop_c_d = ppcalc.get_avg_donations_per_entity(cleaned_c_d_df,
                                                           filters)
    avg_val_pop_c_d = ppcalc.get_avg_value_per_entity(cleaned_c_d_df, filters)
    avg_dono_pop_c_d = ppcalc.get_avg_donors_per_entity(cleaned_c_d_df,
                                                        filters)
    std_dona_pop_c_d = ppcalc.get_donors_stdev(cleaned_c_d_df, filters)
    std_val_pop_c_d = ppcalc.get_value_stdev(cleaned_c_d_df, filters)
    std_dono_pop_c_d = ppcalc.get_noofdonors_per_ent_stdev(cleaned_c_d_df,
                                                           filters)

    # Values for chosen entity, date range and all donations
    unique_reg_ent_r_d = ppcalc.get_regentity_ct(cleaned_r_d_df, filters)
    unique_dono_r_d = ppcalc.get_donors_ct(cleaned_r_d_df, filters)
    unique_dona_r_d = ppcalc.get_donations_ct(cleaned_r_d_df, filters)
    total_val_r_d = ppcalc.get_value_total(cleaned_r_d_df, filters)
    mean_val_r_d = ppcalc.get_value_mean(cleaned_r_d_df, filters)
    avg_dona_pop_r_d = ppcalc.get_avg_donations_per_entity(cleaned_r_d_df,
                                                           filters)
    avg_val_pop_r_d = ppcalc.get_avg_value_per_entity(cleaned_r_d_df, filters)
    avg_dono_pop_r_d = ppcalc.get_avg_donors_per_entity(cleaned_r_d_df,
                                                        filters)
    std_dona_pop_r_d = ppcalc.get_donors_stdev(cleaned_r_d_df, filters)
    std_val_pop_r_d = ppcalc.get_value_stdev(cleaned_r_d_df, filters)
    std_dono_pop_r_d = ppcalc.get_noofdonors_per_ent_stdev(cleaned_r_d_df,
                                                           filters)

    # Values for chosen entity, date range and current target
    unique_reg_ent_c_r = ppcalc.get_regentity_ct(cleaned_c_r_df, filters)
    unique_dono_c_r = ppcalc.get_donors_ct(cleaned_c_r_df, filters)
    unique_dona_c_r = ppcalc.get_donations_ct(cleaned_c_r_df, filters)
    total_val_c_r = ppcalc.get_value_total(cleaned_c_r_df, filters)
    mean_val_c_r = ppcalc.get_value_mean(cleaned_c_r_df, filters)
    avg_dona_pop_c_r = ppcalc.get_avg_donations_per_entity(cleaned_c_r_df,
                                                           filters)
    avg_val_pop_c_r = ppcalc.get_avg_value_per_entity(cleaned_c_r_df, filters)
    avg_dono_pop_c_r = ppcalc.get_avg_donors_per_entity(cleaned_c_r_df,
                                                        filters)
    std_dona_pop_c_r = ppcalc.get_donors_stdev(cleaned_c_r_df, filters)
    std_val_pop_c_r = ppcalc.get_value_stdev(cleaned_c_r_df, filters)
    std_dono_pop_c_r = ppcalc.get_noofdonors_per_ent_stdev(cleaned_c_r_df,
                                                           filters)

    # Values for chosen entity, date range and current target
    unique_reg_ent_c_r_d = ppcalc.get_regentity_ct(cleaned_c_r_d_df, filters)
    unique_dono_c_r_d = ppcalc.get_donors_ct(cleaned_c_r_d_df, filters)
    unique_dona_c_r_d = ppcalc.get_donations_ct(cleaned_c_r_d_df, filters)
    total_val_c_r_d = ppcalc.get_value_total(cleaned_c_r_d_df, filters)
    mean_val_c_r_d = ppcalc.get_value_mean(cleaned_c_r_d_df, filters)
    avg_dona_pop_c_r_d = ppcalc.get_avg_donations_per_entity(cleaned_c_r_d_df,
                                                             filters)
    avg_val_pop_c_r_d = ppcalc.get_avg_value_per_entity(cleaned_c_r_d_df,
                                                        filters)
    avg_dono_pop_c_r_d = ppcalc.get_avg_donors_per_entity(cleaned_c_r_d_df,
                                                          filters)
    std_dona_pop_c_r_d = ppcalc.get_donors_stdev(cleaned_c_r_d_df, filters)
    std_val_pop_c_r_d = ppcalc.get_value_stdev(cleaned_c_r_d_df, filters)
    std_dono_pop_c_r_d = ppcalc.get_noofdonors_per_ent_stdev(cleaned_c_r_d_df,
                                                             filters)

    # Relative relationship calculations
    create_donation_comparisons = True
    create_value_comparisons = True
    create_donor_comparisons = True
    create_reg_entity_comparisons = True
    # Donation comparisons
    if create_donation_comparisons:
        perc_dona_c_V_pop = ppcalc.calculate_percentage(unique_dona_r,
                                                        unique_dona_pop)
        perc_dona_r_V_pop = ppcalc.calculate_percentage(unique_dona_r,
                                                        unique_dona_pop)
        perc_dona_d_V_pop = ppcalc.calculate_percentage(unique_dona_d,
                                                        unique_dona_pop)
        perc_dona_c_r_V_pop = ppcalc.calculate_percentage(unique_dona_c_d,
                                                          unique_dona_pop)
        perc_dona_c_d_V_pop = ppcalc.calculate_percentage(unique_dona_c_d,
                                                          unique_dona_pop)
        perc_dona_r_d_V_pop = ppcalc.calculate_percentage(unique_dona_r_d,
                                                          unique_dona_pop)
        perc_dona_c_r_d_V_pop = ppcalc.calculate_percentage(unique_dona_c_r_d,
                                                            unique_dona_pop)
        perc_dona_c_d_V_d = ppcalc.calculate_percentage(unique_dona_c_d,
                                                        unique_dona_d)
        perc_dona_r_d_V_d = ppcalc.calculate_percentage(unique_dona_r_d,
                                                        unique_dona_d)
        perc_dona_r_d_V_r = ppcalc.calculate_percentage(unique_dona_r_d,
                                                        unique_dona_r)
        perc_dona_c_r_V_r = ppcalc.calculate_percentage(unique_dona_c_r,
                                                        unique_dona_r)
        perc_dona_c_r_d_V_c = ppcalc.calculate_percentage(unique_dona_c_r_d,
                                                          unique_dona_c)
        perc_dona_c_r_d_V_d = ppcalc.calculate_percentage(unique_dona_c_r_d,
                                                          unique_dona_d)
        perc_dona_c_r_d_V_r = ppcalc.calculate_percentage(unique_dona_c_r_d,
                                                          unique_dona_r)
        perc_dona_c_r_d_V_r_d = ppcalc.calculate_percentage(unique_dona_c_r_d,
                                                            unique_dona_r_d)
        perc_dona_c_r_d_V_c_d = ppcalc.calculate_percentage(unique_dona_c_r_d,
                                                            unique_dona_c_d)
        perc_dona_c_r_d_V_c_r = ppcalc.calculate_percentage(unique_dona_c_r_d,
                                                            unique_dona_c_r)

    # Value comparisons
    if create_value_comparisons:
        perc_val_c_V_pop = ppcalc.calculate_percentage(total_val_c,
                                                       total_val_pop)
        perc_val_r_V_pop = ppcalc.calculate_percentage(total_val_r,
                                                       total_val_pop)
        perc_val_d_V_pop = ppcalc.calculate_percentage(total_val_d,
                                                       total_val_pop)
        perc_val_c_r_V_pop = ppcalc.calculate_percentage(total_val_c_d,
                                                         total_val_pop)
        perc_val_c_d_V_pop = ppcalc.calculate_percentage(total_val_c_d,
                                                         total_val_pop)
        perc_val_r_d_V_pop = ppcalc.calculate_percentage(total_val_r_d,
                                                         total_val_pop)
        perc_val_c_r_d_V_pop = ppcalc.calculate_percentage(total_val_c_r_d,
                                                           total_val_pop)
        perc_val_c_d_V_d = ppcalc.calculate_percentage(total_val_c_d,
                                                       total_val_d)
        perc_val_r_d_V_d = ppcalc.calculate_percentage(total_val_r_d,
                                                       total_val_d)
        perc_val_r_d_V_r = ppcalc.calculate_percentage(total_val_r_d,
                                                       total_val_r)
        perc_val_c_r_V_r = ppcalc.calculate_percentage(total_val_c_r,
                                                       total_val_r)
        perc_val_c_r_d_V_c = ppcalc.calculate_percentage(total_val_c_r_d,
                                                         total_val_c)
        perc_val_c_r_d_V_d = ppcalc.calculate_percentage(total_val_c_r_d,
                                                         total_val_d)
        perc_val_c_r_d_V_r = ppcalc.calculate_percentage(total_val_c_r_d,
                                                         total_val_r)
        perc_val_c_r_d_V_r_d = ppcalc.calculate_percentage(total_val_c_r_d,
                                                           total_val_r_d)
        perc_val_c_r_d_V_c_d = ppcalc.calculate_percentage(total_val_c_r_d,
                                                           total_val_c_d)
        perc_val_c_r_d_V_c_r = ppcalc.calculate_percentage(total_val_c_r_d,
                                                           total_val_c_r)

    # Donor comparisons
    if create_donor_comparisons:
        perc_dono_c_V_pop = ppcalc.calculate_percentage(unique_dono_r,
                                                        unique_dono_pop)
        perc_dono_r_V_pop = ppcalc.calculate_percentage(unique_dono_r,
                                                        unique_dono_pop)
        perc_dono_d_V_pop = ppcalc.calculate_percentage(unique_dono_d,
                                                        unique_dono_pop)
        perc_dono_c_r_V_pop = ppcalc.calculate_percentage(unique_dono_c_d,
                                                          unique_dono_pop)
        perc_dono_c_d_V_pop = ppcalc.calculate_percentage(unique_dono_c_d,
                                                          unique_dono_pop)
        perc_dono_r_d_V_pop = ppcalc.calculate_percentage(unique_dono_r_d,
                                                          unique_dono_pop)
        perc_dono_c_r_d_V_pop = ppcalc.calculate_percentage(unique_dono_c_r_d,
                                                            unique_dono_pop)
        perc_dono_c_d_V_d = ppcalc.calculate_percentage(unique_dono_c_d,
                                                        unique_dono_d)
        perc_dono_r_d_V_d = ppcalc.calculate_percentage(unique_dono_r_d,
                                                        unique_dono_d)
        perc_dono_r_d_V_r = ppcalc.calculate_percentage(unique_dono_r_d,
                                                        unique_dono_r)
        perc_dono_c_r_V_r = ppcalc.calculate_percentage(unique_dono_c_r,
                                                        unique_dono_r)
        perc_dono_c_r_d_V_c = ppcalc.calculate_percentage(unique_dono_c_r_d,
                                                          unique_dono_c)
        perc_dono_c_r_d_V_d = ppcalc.calculate_percentage(unique_dono_c_r_d,
                                                          unique_dono_d)
        perc_dono_c_r_d_V_r = ppcalc.calculate_percentage(unique_dono_c_r_d,
                                                          unique_dono_r)
        perc_dono_c_r_d_V_r_d = ppcalc.calculate_percentage(unique_dono_c_r_d,
                                                            unique_dono_r_d)
        perc_dono_c_r_d_V_c_d = ppcalc.calculate_percentage(unique_dono_c_r_d,
                                                            unique_dono_c_d)
        perc_dono_c_r_d_V_c_r = ppcalc.calculate_percentage(unique_dono_c_r_d,
                                                            unique_dono_c_r)

    # Regulated Entity comparisons
    if create_reg_entity_comparisons:
        perc_reg_ent_c_V_pop = ppcalc.calculate_percentage(unique_reg_ent_c,
                                                           unique_reg_ent_pop)
        perc_reg_ent_r_V_pop = ppcalc.calculate_percentage(unique_reg_ent_r,
                                                           unique_reg_ent_pop)
        perc_reg_ent_d_V_pop = ppcalc.calculate_percentage(unique_reg_ent_d,
                                                           unique_reg_ent_pop)
        perc_reg_ent_c_r_V_pop = ppcalc.calculate_percentage(
            unique_reg_ent_c_d, unique_reg_ent_pop)
        perc_reg_ent_c_d_V_pop = ppcalc.calculate_percentage(
            unique_reg_ent_c_d, unique_reg_ent_pop)
        perc_reg_ent_r_d_V_pop = ppcalc.calculate_percentage(
            unique_reg_ent_r_d, unique_reg_ent_pop)
        perc_reg_ent_c_r_d_V_pop = ppcalc.calculate_percentage(
            unique_reg_ent_c_r_d, unique_reg_ent_pop)
        perc_reg_ent_c_d_V_d = ppcalc.calculate_percentage(unique_reg_ent_c_d,
                                                           unique_reg_ent_d)
        perc_reg_ent_r_d_V_d = ppcalc.calculate_percentage(unique_reg_ent_r_d,
                                                           unique_reg_ent_d)
        perc_reg_ent_r_d_V_r = ppcalc.calculate_percentage(unique_reg_ent_r_d,
                                                           unique_reg_ent_r)
        perc_reg_ent_c_r_V_r = ppcalc.calculate_percentage(unique_reg_ent_c_r,
                                                           unique_reg_ent_r)
        perc_reg_ent_c_r_d_V_c = ppcalc.calculate_percentage(
            unique_reg_ent_c_r_d, unique_reg_ent_c)
        perc_reg_ent_c_r_d_V_d = ppcalc.calculate_percentage(
            unique_reg_ent_c_r_d, unique_reg_ent_d)
        perc_reg_ent_c_r_d_V_r = ppcalc.calculate_percentage(
            unique_reg_ent_c_r_d, unique_reg_ent_r)
        perc_reg_ent_c_r_d_V_r_d = ppcalc.calculate_percentage(
            unique_reg_ent_c_r_d, unique_reg_ent_r_d)
        perc_reg_ent_c_r_d_V_c_d = ppcalc.calculate_percentage(
            unique_reg_ent_c_r_d, unique_reg_ent_c_d)
        perc_reg_ent_c_r_d_V_c_r = ppcalc.calculate_percentage(
            unique_reg_ent_c_r_d, unique_reg_ent_c_r)

    # Format selected dates for inclusion in text
    min_date_df = start_date.date()
    max_date_df = end_date.date()

    # Text Discription and visuals
    st.write("---")
    st.write(f"## Topline Figures for {target_label} to {selected_entity_name}"
             f" between {min_date_df} and {max_date_df}")
    st.write("---")
    st.write(f"* During the period between {min_date_df} and {max_date_df}, "
             f"there were {unique_dona_c_d:,.0f} {target_label}s made to "
             f"{selected_entity_name}.  These had an average value of "
             f"£{ppcalc.format_number(mean_val_c_d)} "
             f"and were made by {ppcalc.format_number(unique_dono_c_d)} "
             "unique donors. These donations totalled "
             f"£{ppcalc.format_number(total_val_c_d)}"
             f" and represented {perc_dona_c_r_d_V_r_d:.2f}% of"
             f" all donations made "
             f" to {selected_entity_name}"
             " during the period selected.")
    if unique_dona_c_d < unique_dona_r_d:
        st.write(" During the period they received a total of"
                 f" {unique_dona_r_d:,.0f} donations"
                 " with a total value of"
                 f" £{ppcalc.format_number(total_val_r_d)} and an"
                 " average value of "
                 f"£{ppcalc.format_number(mean_val_r_d)}"
                 f" from {unique_dono_r_d:,.0f} unique donors.")

    # Compare percentage of target donations to chosen entity vs avergage
    # percentage cash donations for all entities
    if perc_dona_c_V_pop > 0:
        if perc_dona_c_r_V_pop > perc_dona_c_V_pop:
            changetext = "higher than"
        elif perc_dona_c_r_V_pop < perc_dona_c_V_pop:
            changetext = "lower than"
        else:
            changetext = "the same as"
        st.write(f"* The percentage of {target_label}s made "
                 f"to {selected_entity_name} "
                 f"was {perc_dona_c_r_V_pop:.2f}% and is {changetext} "
                 "the average "
                 f"percentage of {target_label}s made to all entities"
                 f" ({perc_dona_c_V_pop:.2f}%)")
    # Compare total value share of {target_label}s to value
    # of all chosen entity
    # donations vs total value share of {target_label}s for all entities
    if perc_val_c_V_pop > 0:
        if perc_val_c_r_V_pop > perc_val_c_V_pop:
            changetext = "higher than"
        elif perc_val_c_r_V_pop < perc_val_c_V_pop:
            changetext = "lower than"
        else:
            changetext = "the same as"
        st.write(f"* The value of {target_label}s "
                 " as a percentage of all donations made to "
                 f"{selected_entity_name} "
                 f"({perc_val_c_r_V_pop:.2f}%) is {changetext} the average"
                 f" value of {target_label}s made to all entities"
                 f" ({perc_val_c_V_pop:.2f}%)")
    # Compare number of donors to chosen entity vs
    # avergage number of donors for all entities
    if perc_val_c_V_pop > 0:
        if perc_val_c_r_V_pop > perc_val_c_V_pop:
            changetext = "higher than"
        elif perc_val_c_r_V_pop < perc_val_c_V_pop:
            changetext = "lower than"
        else:
            changetext = "the same as"
        st.write(f"* The value of {target_label}s "
                 " as a percentage of all donations made to "
                 f"{selected_entity_name} "
                 f"({perc_val_c_r_V_pop:.2f}%) is {changetext} the average"
                 " value of {target_label}s made to all entities"
                 f" ({perc_val_c_V_pop:.2f}%)")
    if min_date_df != min_date or max_date_df != max_date:
        if perc_val_c_d_V_pop > 0:
            if perc_val_c_r_d_V_pop > perc_val_c_d_V_pop:
                changetext = "higher than"
            elif perc_val_c_r_d_V_pop < perc_val_c_d_V_pop:
                changetext = "lower than"
            else:
                changetext = "the same as"
            st.write(f"* The value of {target_label}s "
                     " as a percentage of all donations made to "
                     f"{selected_entity_name} "
                     f"({perc_val_c_r_d_V_pop:.2f}%) "
                     f"is {changetext} the average"
                     " value of {target_label}s made to all entities"
                     f" ({perc_val_c_d_V_pop:.2f}%)")
    else:
        "No date range selected."
    st.write("---")
    st.write(f"### Topline Visuals for {target_label}"
             f" to {selected_entity_name}"
             f" between {min_date_df} and {max_date_df}")
    st.write("#### Click on any Visualisation to view it full screen.")
    st.write("---")
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
    st.write("---")
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
    st.write("---")
    # Create a table of the results
    st.write(f"### Comparison Table: Donation Values"
             f"({min_date} to {max_date})")
    # Set variables to contain column names
    column_names = ["Total Value",
                    "Mean Value",
                    "Avg Value per Entity",
                    "Std Dev Value per Entity"]
    # Metrics
    metrics = [
        f"All Donations: \n{min_date} to {max_date}",
        f"{target_label}s: \n{min_date} to {max_date}",
        f"{selected_entity_name}: \n{min_date} to {max_date}",
        f"{selected_entity_name},\n{target_label}s:"
        f" {min_date} to {max_date}",
        f"All donations: \n{min_date_df} to {max_date_df}",
        f"{target_label}s: \n{min_date_df} to {max_date_df}",
        f"{selected_entity_name}: \n{min_date_df} to {max_date_df}",
        f"{selected_entity_name},\n{target_label}s:"
        f" {min_date_df} to {max_date_df}"
    ]
    # Corresponding data values for each column
    comparison_data_a = {
        "Metric": metrics,
        column_names[0]: [total_val_pop, total_val_c, total_val_r,
                          total_val_c_r, total_val_d, total_val_c_d,
                          total_val_r_d, total_val_c_r_d],
        column_names[1]: [mean_val_pop, mean_val_c, mean_val_r, mean_val_c_r,
                          mean_val_d, mean_val_c_d, mean_val_r_d,
                          mean_val_c_r_d],
        column_names[2]: [avg_val_pop, avg_val_pop_c, avg_val_pop_r,
                          avg_val_pop_c_r, avg_val_pop_d, avg_val_pop_c_d,
                          avg_val_pop_r_d, avg_val_pop_c_r_d],
        column_names[3]: [std_val_pop, std_val_pop_c, std_val_pop_r,
                          std_val_pop_c_r, std_val_pop_d, std_val_pop_c_d,
                          std_val_pop_r_d, std_val_pop_c_r_d]
    }
    comparison_df_a = pd.DataFrame(comparison_data_a)
    # Display in Streamlit
    st.dataframe(
        comparison_df_a,
        column_config={col: st.column_config.NumberColumn(format="£ %.0f")
                       for col in column_names},
        hide_index=True,
        use_container_width=False
    )
    # table 2
    st.write("### Comparison Table: of Donations and Donors")
    # set variable to contain column names
    column_names2 = [
            "Regulated Entities",
            "Donors",
            "Donations",
            "Avg. Donations per Entity",
            "Avg. Donors per Entity",
            "S.Dev Donations per Entity",
            "S.Dev Donors per Entity"
            ]

    # Metrics
    metrics = [
        f"All Donations: \n{min_date} to {max_date}",
        f"{target_label}s: \n{min_date} to {max_date}",
        f"{selected_entity_name}: \n{min_date} to {max_date}",
        f"{selected_entity_name},\n{target_label}s:"
        f" {min_date} to {max_date}",
        f"All donations: \n{min_date_df} to {max_date_df}",
        f"{target_label}s: \n{min_date_df} to {max_date_df}",
        f"{selected_entity_name}: \n{min_date_df} to {max_date_df}",
        f"{selected_entity_name},\n{target_label}s:"
        f" {min_date_df} to {max_date_df}"
    ]
    # Corresponding data values for each column
    comparison_data2 = {
        "Metric": metrics,
        column_names2[0]: [unique_reg_ent_pop, unique_reg_ent_c,
                           unique_reg_ent_r, unique_reg_ent_c_r,
                           unique_reg_ent_d, unique_reg_ent_c_d,
                           unique_reg_ent_r_d, unique_reg_ent_c_r_d],
        column_names2[1]: [unique_dono_pop, unique_dono_c, unique_dono_r,
                           unique_dono_c_r, unique_dono_d, unique_dono_c_d,
                           unique_dono_r_d, unique_dono_c_r_d],
        column_names2[2]: [unique_dona_pop, unique_dona_c, unique_dona_r,
                           unique_dona_c_r, unique_dona_d, unique_dona_c_d,
                           unique_dona_r_d, unique_dona_c_r_d],
        column_names2[3]: [avg_dona_pop, avg_dona_pop_c, avg_dona_pop_r,
                           avg_dona_pop_c_r, avg_dona_pop_d, avg_dona_pop_c_d,
                           avg_dona_pop_r_d, avg_dona_pop_c_r_d],
        column_names2[4]: [avg_dono_pop, avg_dono_pop_c, avg_dono_pop_r,
                           avg_dono_pop_c_r, avg_dono_pop_d, avg_dono_pop_c_d,
                           avg_dono_pop_r_d, avg_dono_pop_c_r_d],
        column_names2[5]: [std_dona_pop, std_dona_pop_c, std_dona_pop_r,
                           std_dona_pop_c_r, std_dona_pop_d, std_dona_pop_c_d,
                           std_dona_pop_r_d, std_dona_pop_c_r_d],
        column_names2[6]: [std_dono_pop, std_dono_pop_c, std_dono_pop_r,
                           std_dono_pop_c_r, std_dono_pop_d, std_dono_pop_c_d,
                           std_dono_pop_r_d, std_dono_pop_c_r_d]
    }
    # Create a table of the results
    comparison_df2_2 = pd.DataFrame(comparison_data2)
    # Display in Streamlit
    st.dataframe(
        comparison_df2_2,
        column_config={col: st.column_config.NumberColumn(format="%.0f")
                       for col in column_names2},
        hide_index=True,
        use_container_width=False
    )

    # Table 3: Percentage Comparison vs All Donations
    # (Between min_date and max_date)
    st.write(f"### Percentage Comparison Table: vs All Donations"
             f" Activity between {min_date} and {max_date}")
    # Define row names
    metrics3 = [
        f"{target_label}s vs All Donations: {min_date} to {max_date}",
        f"{selected_entity_name} vs All Donations:"
        f" {min_date} to {max_date}",
        f"All Donations: {min_date_df} to {max_date_df} vs"
        f" {min_date} to {max_date}",
        f"{selected_entity_name} {target_label}s vs All Donations:"
        f" {min_date} to {max_date}",
        f"{target_label}: {min_date_df} to {max_date_df} vs All Donations:"
        f" {min_date} to {max_date}",
        f"{selected_entity_name}: {min_date_df} to {max_date_df} vs"
        f" All Donations: {min_date} to {max_date}",
        f"{selected_entity_name} {target_label}s: {min_date_df}"
        f" to {max_date_df} vs All Donations: {min_date} to {max_date}",
    ]
    # Define column names
    column_names3 = ["Percentage Of Donations", "Percentage Of Value",
                     "Percentage Of Donors", "Percentage Of Entities"]
    # Data for percentage comparisons
    percentage_comparison_data3 = {
        "Metric": metrics3,  # Keeping metrics as the first column
        column_names3[0]: [perc_dona_c_V_pop, perc_dona_r_V_pop,
                           perc_dona_d_V_pop, perc_dona_c_r_V_pop,
                           perc_dona_c_d_V_pop, perc_dona_r_d_V_pop,
                           perc_dona_c_r_d_V_pop
                           ],
        column_names3[1]: [perc_val_c_V_pop,
                           perc_val_r_V_pop, perc_val_d_V_pop,
                           perc_val_c_r_V_pop, perc_val_c_d_V_pop,
                           perc_val_r_d_V_pop, perc_val_c_r_d_V_pop],
        column_names3[2]: [perc_dono_c_V_pop,
                           perc_dono_r_V_pop, perc_dono_d_V_pop,
                           perc_dono_c_r_V_pop, perc_dono_c_d_V_pop,
                           perc_dono_r_d_V_pop, perc_dono_c_r_d_V_pop],
        column_names3[3]: [perc_reg_ent_c_V_pop,
                           perc_reg_ent_r_V_pop, perc_reg_ent_d_V_pop,
                           perc_reg_ent_c_r_V_pop, perc_reg_ent_c_d_V_pop,
                           perc_reg_ent_r_d_V_pop, perc_reg_ent_c_r_d_V_pop]
    }

    # Create DataFrame
    percentage_comparison_df_3 = pd.DataFrame(percentage_comparison_data3)
    # Display formatted percentage comparison table in Streamlit
    st.dataframe(
        percentage_comparison_df_3,
        column_config={col: st.column_config.NumberColumn(format="%.2f%%")
                       for col in column_names3},
        hide_index=True,
        use_container_width=False
    )

    # Table 4: Percentage Comparison vs All Donations
    # (Between min_date_df and max_date_df)
    st.write(f"### Percentage Comparison Table: vs All Donations"
             f" Activity between {min_date_df} and {max_date_df}")
    # Define row names
    metrics4 = [
        f"{target_label}s: {min_date_df} to {max_date_df} vs All Donations:"
        f" {min_date_df} to {max_date_df}",
        f"{selected_entity_name}: {min_date_df} to {max_date_df} vs"
        " All Donations:"
        f" {min_date_df} to {max_date_df}",
        f"{selected_entity_name} {target_label}s: {min_date_df} to"
        f" {max_date_df} vs All Donations:"
        f" {min_date_df} to {max_date_df}",
        f"{selected_entity_name} {target_label}s: {min_date_df} to"
        f" {max_date_df} vs All {target_label}:"
        f" {min_date_df} to {max_date_df}",
        f"{selected_entity_name} {target_label}s: {min_date_df} to"
        f" {max_date_df} vs {selected_entity_name} all Donations:"
        f" {min_date_df} to {max_date_df}"
    ]
    # Data for percentage comparisons
    percentage_comparison_data4 = {
        "Metric": metrics4,  # Keeping metrics as the first column
        column_names3[0]: [perc_dona_c_d_V_d,
                           perc_dona_r_d_V_d,
                           perc_dona_c_r_d_V_d,
                           perc_dona_c_r_d_V_c_d,
                           perc_dona_c_r_d_V_r_d
                           ],
        column_names3[1]: [perc_val_c_d_V_d, perc_val_r_d_V_d,
                           perc_val_c_r_d_V_d, perc_val_c_r_d_V_c_d,
                           perc_val_c_r_d_V_r_d
                           ],
        column_names3[2]: [perc_dono_c_d_V_d,
                           perc_dono_r_d_V_d,
                           perc_dono_c_r_d_V_d,
                           perc_dono_c_r_d_V_c_d,
                           perc_dono_c_r_d_V_r_d
                           ],
        column_names3[3]: [perc_reg_ent_c_d_V_d,
                           perc_reg_ent_r_d_V_d,
                           perc_reg_ent_c_r_d_V_d,
                           perc_reg_ent_c_r_d_V_c_d,
                           perc_reg_ent_c_r_d_V_r_d
                           ]
    }
    # Create DataFrame
    percentage_comparison_df4 = pd.DataFrame(percentage_comparison_data4)
    # Display formatted percentage comparison table in Streamlit
    st.dataframe(
        percentage_comparison_df4,
        column_config={col: st.column_config.NumberColumn(format="%.2f%%")
                       for col in column_names3},
        hide_index=True,
        use_container_width=False
    )

    # table 5
    # Data for percentage comparisons (structured without transposing)
    # Define row names
    metrics5 = [
        f"{target_label}s: {min_date_df} to {max_date_df} vs All"
        f" {selected_entity_name} Donations:"
        f" {min_date} to {max_date}",
        f"{selected_entity_name} {target_label}s: {min_date} to {max_date} vs"
        f" All {selected_entity_name} Donations:"
        f" {min_date} to {max_date}",
        f"{selected_entity_name} {target_label}s: {min_date_df}"
        f" to {max_date_df} vs All {selected_entity_name} Donations:"
        f" {min_date} to {max_date}",
        f"{selected_entity_name} {target_label}s: {min_date_df}"
        f" to {max_date_df} vs All {target_label}:"
        f" {min_date} to {max_date}",
        f"{selected_entity_name} {target_label}s: {min_date_df}"
        f" to {max_date_df} vs {selected_entity_name} {target_label}s:"
        f" {min_date} to {max_date}"
        f" to {max_date_df} vs all {target_label} Donations:"
        f" {min_date} to {max_date}"
    ]
    # Data for percentage comparisons
    percentage_comparison_data5 = {
        "Metric": metrics5,  # Keeping metrics as the first column
        column_names3[0]: [perc_dona_r_d_V_r,
                           perc_dona_c_r_V_r,
                           perc_dona_c_r_d_V_r,
                           perc_dona_c_r_d_V_c_r,
                           perc_dona_c_r_d_V_c
                           ],
        column_names3[1]: [perc_val_r_d_V_r,
                           perc_val_c_r_V_r,
                           perc_val_c_r_d_V_r,
                           perc_val_c_r_d_V_c_r,
                           perc_val_c_r_d_V_c
                           ],
        column_names3[2]: [perc_dono_r_d_V_r,
                           perc_dono_c_r_V_r,
                           perc_dono_c_r_d_V_r,
                           perc_dono_c_r_d_V_c_r,
                           perc_dono_c_r_d_V_c
                           ],
        column_names3[3]: [perc_reg_ent_r_d_V_r,
                           perc_reg_ent_c_r_V_r,
                           perc_reg_ent_c_r_d_V_r,
                           perc_reg_ent_c_r_d_V_c_r,
                           perc_reg_ent_c_r_d_V_c
                           ]
    }
    # Create DataFrame
    percentage_comparison_df_5 = pd.DataFrame(percentage_comparison_data5)
    # Display formatted percentage comparison table in Streamlit
    st.write(f"### Percentage Comparison Table: vs {selected_entity_name}"
             " Donor Activity")
    st.dataframe(
        percentage_comparison_df_5,
        column_config={col: st.column_config.NumberColumn(format="%.2f%%")
                       for col in column_names3},
        hide_index=True,
        use_container_width=False
    )
    st.write("---")
