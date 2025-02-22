def visits_body():
    """
    Displays the content of Visit Donations to Political Party page.
    """
    import streamlit as st
    import components.calculations as ppcalc
    import components.Visualisations as vis
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
    current_target = 'DonationType == "Visit" | DonationType == "visit"'
    target_label = "Donated Visit"
    # Apply filters
    filters = ({"RegulatedEntityId": selected_entity_id}
               if selected_entity_name != "All" else {}
               )
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
        cleaned_r_df = (
            cleaned_df[
                cleaned_df["RegulatedEntityId"] == filters["RegulatedEntityId"]
                if filters else True  # If no filters, return all rows
                      ]
                       )
    else:
        cleaned_r_df = cleaned_df
    # Create dataframe for chosen entity and date range
    cleaned_r_d_df = (
        cleaned_r_df[date_filter.reindex(cleaned_r_df.index, fill_value=False)]
        if date_filter.any()
        else cleaned_r_df
    )
    # Create dataframe for chosen target and date range
    cleaned_c_d_df = cleaned_d_df.query(current_target)
    # Create dataframe for chosen target and entity
    cleaned_c_r_df = cleaned_r_df.query(current_target)
    # Create dataframe for chosen target, entity and date range
    cleaned_c_r_d_df = cleaned_r_d_df.query(current_target)

    # Values for all entities, all time and all donations
    unique_reg_ent_pop = (
        ppcalc.get_regentity_ct(cleaned_df, filters)
        )
    unique_dono_pop = ppcalc.get_donors_ct(cleaned_df, filters)
    unique_dona_pop = ppcalc.get_donations_ct(cleaned_df, filters)
    total_val_pop = ppcalc.get_value_total(cleaned_df, filters)
    mean_val_pop = ppcalc.get_value_mean(cleaned_df, filters)
    # Values for all entities, chosen date range and all donations
    unique_reg_ent_d = (
        ppcalc.get_regentity_ct(cleaned_d_df, filters)
        )
    unique_dono_d = ppcalc.get_donors_ct(cleaned_d_df, filters)
    unique_dona_d = ppcalc.get_donations_ct(cleaned_d_df, filters)
    total_val_d = ppcalc.get_value_total(cleaned_d_df, filters)
    mean_val_d = ppcalc.get_value_mean(cleaned_d_df, filters)
    # Values for all entities, all date range and target
    unique_reg_ent_c = (
        ppcalc.get_regentity_ct(cleaned_c_df, filters)
        )
    unique_dono_c = ppcalc.get_donors_ct(cleaned_c_df, filters)
    unique_dona_c = ppcalc.get_donations_ct(cleaned_c_df, filters)
    total_val_c = ppcalc.get_value_total(cleaned_c_df, filters)
    mean_val_c = ppcalc.get_value_mean(cleaned_c_df, filters)
    # Values for chosen entity, all date range and all Donations
    unique_reg_ent_r = (
        ppcalc.get_regentity_ct(cleaned_r_df, filters)
        )
    unique_dono_r = ppcalc.get_donors_ct(cleaned_r_df, filters)
    unique_dona_r = ppcalc.get_donations_ct(cleaned_r_df, filters)
    total_val_r = ppcalc.get_value_total(cleaned_r_df, filters)
    mean_val_r = ppcalc.get_value_mean(cleaned_r_df, filters)
    # Values for all entities, chosen date range and current target
    unique_reg_ent_c_d = (
        ppcalc.get_regentity_ct(cleaned_c_d_df, filters)
        )
    unique_dono_c_d = ppcalc.get_donors_ct(cleaned_c_d_df, filters)
    unique_dona_c_d = ppcalc.get_donations_ct(cleaned_c_d_df, filters)
    total_val_c_d = ppcalc.get_value_total(cleaned_c_d_df, filters)
    mean_val_c_d = ppcalc.get_value_mean(cleaned_c_d_df, filters)
    # Values for chosen entity, date range and all donations
    unique_reg_ent_r_d = (
        ppcalc.get_regentity_ct(cleaned_r_d_df, filters)
        )
    unique_dono_r_d = ppcalc.get_donors_ct(cleaned_r_d_df, filters)
    unique_dona_r_d = ppcalc.get_donations_ct(cleaned_r_d_df, filters)
    total_val_r_d = ppcalc.get_value_total(cleaned_r_d_df, filters)
    mean_val_r_d = ppcalc.get_value_mean(cleaned_r_d_df, filters)
    # Values for chosen entity, date range and all donations
    unique_reg_ent_c_r = (
        ppcalc.get_regentity_ct(cleaned_c_r_df, filters)
        )
    unique_dono_c_r = ppcalc.get_donors_ct(cleaned_c_r_df, filters)
    unique_dona_c_r = ppcalc.get_donations_ct(cleaned_c_r_df, filters)
    total_val_c_r = ppcalc.get_value_total(cleaned_c_r_df, filters)
    mean_val_c_r = ppcalc.get_value_mean(cleaned_c_r_df, filters)
    # Values for chosen entity, date range and current target
    unique_reg_ent_c_r_d = (
        ppcalc.get_regentity_ct(cleaned_c_r_d_df, filters)
        )
    unique_dono_c_r_d = ppcalc.get_donors_ct(cleaned_c_r_d_df, filters)
    unique_dona_c_r_d = ppcalc.get_donations_ct(cleaned_c_r_d_df, filters)
    total_val_c_r_d = (
        ppcalc.get_value_total(cleaned_c_r_d_df, filters)
    )
    mean_val_c_r_d = (
        ppcalc.get_value_mean(cleaned_c_r_d_df, filters)
    )
    # Relative relationship calculations
    create_donation_comparisons = True
    create_value_comparisons = True
    create_donor_comparisons = True
    create_reg_entity_comparisons = True
    # Donation comparisons
    if create_donation_comparisons:
        # percent of target donations for all entities and all time period
        # to all donations for all entries and all time period
        perc_dona_c_V_pop = (
            (unique_dona_c / unique_dona_pop) * 100
            if unique_dona_pop > 0 else 0
            )
        # Percent of all donations for chosen entity
        # to all donations for all entities and all time period
        perc_dona_r_V_pop = (
            (unique_dona_r / unique_dona_pop) * 100
            if unique_dona_pop > 0 else 0
            )
        # Percent of all donations for all entities in time period
        # to all donations for all entities and all time period
        perc_dona_d_V_pop = (
            (unique_dona_d / unique_dona_pop) * 100
            if unique_dona_pop > 0 else 0
            )
        # Percent of target donations for chosen entity all time period
        # to all donations for all entity all time period
        perc_dona_c_r_V_pop = (
            (unique_dona_c_d / unique_dona_pop) * 100
            if unique_dona_pop > 0 else 0
            )
        # Percent of target donations for chosen entity all time period
        # to all donations for all entity all time period
        perc_dona_c_d_V_pop = (
            (unique_dona_c_d / unique_dona_pop) * 100
            if unique_dona_pop > 0 else 0
            )
        # Percent of target donations for chosen entity all time period
        # to all donations for all entity all time period
        perc_dona_r_d_V_pop = (
            (unique_dona_r_d / unique_dona_pop) * 100
            if unique_dona_pop > 0 else 0
            )
        # Percent of target donations for chosen entity all time period
        # to all donations for all entity all time period
        perc_dona_c_r_d_V_pop = (
            (unique_dona_c_r_d / unique_dona_pop) * 100
            if unique_dona_pop > 0 else 0
            )
        # Percent of target donations in time period
        # to all donations for all entity in time period
        perc_dona_c_d_V_d = (
            (unique_dona_c_d / unique_dona_d) * 100
            if unique_dona_d > 0 else 0
            )
        # Percent of all donations in time period for chosen entity
        # to all donations for all entity in time period
        perc_dona_r_d_V_d = (
            (unique_dona_r_d / unique_dona_d) * 100
            if unique_dona_d > 0 else 0
            )
        # Percent of all donations for chosen entity in time period
        # to all donations for chosen entity all time period
        perc_dona_r_d_V_r = (
            (unique_dona_r_d / unique_dona_r) * 100
            if unique_dona_r > 0 else 0
            )
        # Percent of targets for chosen entity all time
        # to all donations for chosen entity all time period
        perc_dona_c_r_V_r = (
            (unique_dona_c_r / unique_dona_r) * 100
            if unique_dona_r > 0 else 0
            )
        # Percent of target donations in time period for chosen entity
        # to target donations for all entities and all time period
        perc_dona_c_r_d_V_c = (
            (unique_dona_c_r_d / unique_dona_c) * 100
            if unique_dona_c > 0 else 0
            )
        # Percent of target donations in time period for chosen entity
        # to all donations for all entities and targetted time period
        perc_dona_c_r_d_V_d = (
            (unique_dona_c_r_d / unique_dona_d) * 100
            if unique_dona_d > 0 else 0
            )
        # Percent of target donations in time period for chosen entity
        # to all donations for chosen entity and all time period
        perc_dona_c_r_d_V_r = (
            (unique_dona_c_r_d / unique_dona_r) * 100
            if unique_dona_r > 0 else 0
            )
        # Percent of target donations in time period for chosen entity
        # to all donations for chosen entity and targetted time period
        perc_dona_c_r_d_V_r_d = (
            (unique_dona_c_r_d / unique_dona_r_d) * 100
            if unique_dona_r_d > 0 else 0
            )
        # Percent of target donations in time period for chosen entity
        # to target donations for all entities and targetted time period
        perc_dona_c_r_d_V_c_d = (
            (unique_dona_c_r_d / unique_dona_c_d) * 100
            if unique_dona_c_d > 0 else 0
            )
        # Percent of target donations in time period for chosen entity
        # to all donations for chosen entities and all time period
        perc_dona_c_r_d_V_c_r = (
            (unique_dona_c_r_d / unique_dona_c_r) * 100
            if unique_dona_c_r > 0 else 0
            )

    # Value comparisons
    if create_value_comparisons:
        # percent of value of target donations for all entities
        # and all time period
        # to all donations for all entries and all time period
        perc_val_c_V_pop = (
            (total_val_c / total_val_pop) * 100
            if total_val_pop > 0 else 0
            )
        # Percent of value of all donations for chosen entity
        # to all donations for all entities and all time period
        perc_val_r_V_pop = (
            (total_val_r / total_val_pop) * 100
            if total_val_pop > 0 else 0
            )
        # Percent of value of all donations for all entities in time period
        # to all donations for all entities and all time period
        perc_val_d_V_pop = (
            (total_val_d / total_val_pop) * 100
            if total_val_pop > 0 else 0
            )
        # Percent of value of target donations for chosen entity
        # all time period
        # to all donations for all entity all time period
        perc_val_c_r_V_pop = (
            (total_val_c_d / total_val_pop) * 100
            if total_val_pop > 0 else 0
            )
        # Percent of value of target donations for chosen entity
        # all time period
        # to all donations for all entity all time period
        perc_val_c_d_V_pop = (
            (total_val_c_d / total_val_pop) * 100
            if total_val_pop > 0 else 0
            )
        # Percent of value of target donations for chosen entity
        # all time period
        # to all donations for all entity all time period
        perc_val_r_d_V_pop = (
            (total_val_r_d / total_val_pop) * 100
            if total_val_pop > 0 else 0
            )
        # Percent of value of target donations for chosen entity
        # all time period
        # to all donations for all entity all time period
        perc_val_c_r_d_V_pop = (
            (total_val_c_r_d / total_val_pop) * 100
            if total_val_pop > 0 else 0
            )
        # Percent of value of target donations in time period
        # to all donations for all entity in time period
        perc_val_c_d_V_d = (
            (total_val_c_d / total_val_d) * 100
            if total_val_d > 0 else 0
            )
        # Percent of value of all donations in time period for chosen entity
        # to all donations for all entity in time period
        perc_val_r_d_V_d = (
            (total_val_r_d / total_val_d) * 100
            if total_val_d > 0 else 0
            )
        # Percent of value of all donations for chosen entity in time period
        # to all donations for chosen entity all time period
        perc_val_r_d_V_r = (
            (total_val_r_d / total_val_r) * 100
            if total_val_r > 0 else 0
            )
        # Percent of value of targets for chosen entity all time
        # to all donations for chosen entity all time period
        perc_val_c_r_V_r = (
            (total_val_c_r / total_val_r) * 100
            if total_val_r > 0 else 0
            )
        # Percent of value of target donations in time period for chosen entity
        # to target donations for all entities and all time period
        perc_val_c_r_d_V_c = (
            (total_val_c_r_d / total_val_c) * 100
            if total_val_c > 0 else 0
            )
        # Percent of value of target donations in time period for chosen entity
        # to all donations for all entities and targetted time period
        perc_val_c_r_d_V_d = (
            (total_val_c_r_d / total_val_d) * 100
            if total_val_d > 0 else 0
            )
        # Percent of value of target donations in time period for chosen entity
        # to all donations for chosen entity and all time period
        perc_val_c_r_d_V_r = (
            (total_val_c_r_d / total_val_r) * 100
            if total_val_r > 0 else 0
            )
        # Percent of value of target donations in time period for chosen entity
        # to all donations for chosen entity and targetted time period
        perc_val_c_r_d_V_r_d = (
            (total_val_c_r_d / total_val_r_d) * 100
            if total_val_r_d > 0 else 0
            )
        # Percent of value of target donations in time period for chosen entity
        # to target donations for all entities and targetted time period
        perc_val_c_r_d_V_c_d = (
            (total_val_c_r_d / total_val_c_d) * 100
            if total_val_c_d > 0 else 0
            )
        # Percent of value of target donations in time period for chosen entity
        # to all donations for chosen entities and all time period
        perc_val_c_r_d_V_c_r = (
            (total_val_c_r_d / total_val_c_r) * 100
            if total_val_c_r > 0 else 0
            )

    # Donor comparisons
    if create_donor_comparisons:
        # percent of donors of target donations for all entities
        # and all time period
        # to all donations for all entries and all time period
        perc_dono_c_V_pop = (
            (total_val_c / unique_dono_pop) * 100
            if unique_dono_pop > 0 else 0
            )
        # Percent of donors of all donations for chosen entity
        # to all donations for all entities and all time period
        perc_dono_r_V_pop = (
            (unique_dono_r / unique_dono_pop) * 100
            if unique_dono_pop > 0 else 0
            )
        # Percent of donors of all donations for all entities in time period
        # to all donations for all entities and all time period
        perc_dono_d_V_pop = (
            (unique_dono_d / unique_dono_pop) * 100
            if unique_dono_pop > 0 else 0
            )
        # Percent of donors of target donations for chosen entity
        # all time period
        # to all donations for all entity all time period
        perc_dono_c_r_V_pop = (
            (unique_dono_c_d / unique_dono_pop) * 100
            if unique_dono_pop > 0 else 0
            )
        # Percent of donors of target donations for chosen entity
        # all time period
        # to all donations for all entity all time period
        perc_dono_c_d_V_pop = (
            (unique_dono_c_d / unique_dono_pop) * 100
            if unique_dono_pop > 0 else 0
            )
        # Percent of donors of target donations for chosen entity
        # all time period
        # to all donations for all entity all time period
        perc_dono_r_d_V_pop = (
            (unique_dono_r_d / unique_dono_pop) * 100
            if unique_dono_pop > 0 else 0
            )
        # Percent of donors of target donations for chosen entity
        # all time period
        # to all donations for all entity all time period
        perc_dono_c_r_d_V_pop = (
            (unique_dono_c_r_d / unique_dono_pop) * 100
            if unique_dono_pop > 0 else 0
            )
        # Percent of donors of target donations in time period
        # to all donations for all entity in time period
        perc_dono_c_d_V_d = (
            (unique_dono_c_d / unique_dono_d) * 100
            if unique_dono_d > 0 else 0
            )
        # Percent of donors of all donations in time period for chosen entity
        # to all donations for all entity in time period
        perc_dono_r_d_V_d = (
            (unique_dono_r_d / unique_dono_d) * 100
            if unique_dono_d > 0 else 0
            )
        # Percent of donors of all donations for chosen entity in time period
        # to all donations for chosen entity all time period
        perc_dono_r_d_V_r = (
            (unique_dono_r_d / unique_dono_r) * 100
            if unique_dono_r > 0 else 0
            )
        # Percent of donors of targets for chosen entity all time
        # to all donations for chosen entity all time period
        perc_dono_c_r_V_r = (
            (unique_dono_c_r / unique_dono_r) * 100
            if unique_dono_r > 0 else 0
            )
        # Percent of donors of target donations in time period for
        # chosen entity
        # to target donations for all entities and all time period
        perc_dono_c_r_d_V_c = (
            (unique_dono_c_r_d / unique_dono_c) * 100
            if unique_dono_c > 0 else 0
            )
        # Percent of donors of target donations in time period for
        # chosen entity
        # to all donations for all entities and targetted time period
        perc_dono_c_r_d_V_d = (
            (unique_dono_c_r_d / unique_dono_d) * 100
            if unique_dono_d > 0 else 0
            )
        # Percent of donors of target donations in time period for
        # chosen entity
        # to all donations for chosen entity and all time period
        perc_dono_c_r_d_V_r = (
            (unique_dono_c_r_d / unique_dono_r) * 100
            if unique_dono_r > 0 else 0
            )
        # Percent of donors of target donations in time period for
        # chosen entity
        # to all donations for chosen entity and targetted time period
        perc_dono_c_r_d_V_r_d = (
            (unique_dono_c_r_d / unique_dono_r_d) * 100
            if unique_dono_r_d > 0 else 0
            )
        # Percent of donors of target donations in time period for
        # chosen entity
        # to target donations for all entities and targetted time period
        perc_dono_c_r_d_V_c_d = (
            (unique_dono_c_r_d / unique_dono_c_d) * 100
            if unique_dono_c_d > 0 else 0
            )
        # Percent of donors of target donations in time period for
        # chosen entity
        # to all donations for chosen entities and all time period
        perc_dono_c_r_d_V_c_r = (
            (unique_dono_c_r_d / unique_dono_c_r) * 100
            if unique_dono_c_r > 0 else 0
            )

    # Regulated Entity comparisons
    if create_reg_entity_comparisons:
        # percent of regulated entitied of target donations for
        # all entities and all time period
        # to all donations for all entries and all time period
        perc_reg_ent_c_V_pop = (
            (unique_reg_ent_c / unique_reg_ent_pop) * 100
            if unique_reg_ent_pop > 0 else 0
            )
        # Percent of regulated entitied of all donations for chosen entity
        # to all donations for all entities and all time period
        perc_reg_ent_r_V_pop = (
            (unique_reg_ent_r / unique_reg_ent_pop) * 100
            if unique_reg_ent_pop > 0 else 0
            )
        # Percent of regulated entitied of all donations for
        # all entities in time period
        # to all donations for all entities and all time period
        perc_reg_ent_d_V_pop = (
            (unique_reg_ent_d / unique_reg_ent_pop) * 100
            if unique_reg_ent_pop > 0 else 0
            )
        # Percent of regulated entitied of target donations for
        # chosen entity all time period
        # to all donations for all entity all time period
        perc_reg_ent_c_r_V_pop = (
            (unique_reg_ent_c_d / unique_reg_ent_pop) * 100
            if unique_reg_ent_pop > 0 else 0
            )
        # Percent of regulated entitied of target donations for
        # chosen entity all time period
        # to all donations for all entity all time period
        perc_reg_ent_c_d_V_pop = (
            (unique_reg_ent_c_d / unique_reg_ent_pop) * 100
            if unique_reg_ent_pop > 0 else 0
            )
        # Percent of regulated entitied of target donations for
        # chosen entity all time period
        # to all donations for all entity all time period
        perc_reg_ent_r_d_V_pop = (
            (unique_reg_ent_r_d / unique_reg_ent_pop) * 100
            if unique_reg_ent_pop > 0 else 0
            )
        # Percent of regulated entitied of target donations for
        # chosen entity all time period
        # to all donations for all entity all time period
        perc_reg_ent_c_r_d_V_pop = (
            (unique_reg_ent_c_r_d / unique_reg_ent_pop) * 100
            if unique_reg_ent_pop > 0 else 0
            )
        # Percent of regulated entitied of target donations in time period
        # to all donations for all entity in time period
        perc_reg_ent_c_d_V_d = (
            (unique_reg_ent_c_d / unique_reg_ent_d) * 100
            if unique_reg_ent_d > 0 else 0
            )
        # Percent of regulated entitied of all donations in
        # time period for chosen entity
        # to all donations for all entity in time period
        perc_reg_ent_r_d_V_d = (
            (unique_reg_ent_r_d / unique_reg_ent_d) * 100
            if unique_reg_ent_d > 0 else 0
            )
        # Percent of regulated entitied of all donations for
        # chosen entity in time period
        # to all donations for chosen entity all time period
        perc_reg_ent_r_d_V_r = (
            (unique_reg_ent_r_d / unique_reg_ent_r) * 100
            if unique_reg_ent_r > 0 else 0
            )
        # Percent of regulated entitied of targets for chosen entity all time
        # to all donations for chosen entity all time period
        perc_reg_ent_c_r_V_r = (
            (unique_reg_ent_c_r / unique_reg_ent_r) * 100
            if unique_reg_ent_r > 0 else 0
            )
        # Percent of regulated entitied of target donations
        # in time period for chosen entity
        # to target donations for all entities and all time period
        perc_reg_ent_c_r_d_V_c = (
            (unique_reg_ent_c_r_d / unique_reg_ent_c) * 100
            if unique_reg_ent_c > 0 else 0
            )
        # Percent of regulated entitied of target donations in
        # time period for chosen entity
        # to all donations for all entities and targetted time period
        perc_reg_ent_c_r_d_V_d = (
            (unique_reg_ent_c_r_d / unique_reg_ent_d) * 100
            if unique_reg_ent_d > 0 else 0
            )
        # Percent of regulated entitied of target donations in
        # time period for chosen entity
        # to all donations for chosen entity and all time period
        perc_reg_ent_c_r_d_V_r = (
            (unique_reg_ent_c_r_d / unique_reg_ent_r) * 100
            if unique_reg_ent_r > 0 else 0
            )
        # Percent of regulated entitied of target donations in
        # time period for chosen entity
        # to all donations for chosen entity and targetted time period
        perc_reg_ent_c_r_d_V_r_d = (
            (unique_reg_ent_c_r_d / unique_reg_ent_r_d) * 100
            if unique_reg_ent_r_d > 0 else 0
            )
        # Percent of regulated entitied of target donations in
        # time period for chosen entity
        # to target donations for all entities and targetted time period
        perc_reg_ent_c_r_d_V_c_d = (
            (unique_reg_ent_c_r_d / unique_reg_ent_c_d) * 100
            if unique_reg_ent_c_d > 0 else 0
            )
        # Percent of regulated entitied of target donations in
        # time period for chosen entity
        # to all donations for chosen entities and all time period
        perc_reg_ent_c_r_d_V_c_r = (
            (unique_reg_ent_c_r_d / unique_reg_ent_c_r) * 100
            if unique_reg_ent_c_r > 0 else 0
            )
    # Format selected dates for inclusion in text
    min_date_df = start_date.date()
    max_date_df = end_date.date()
    st.write("---")
    st.write("# {target_label}: Political Entity and Date Range")
    st.write("---")
    st.write(f"## Topline Figures for {target_label} to {selected_entity_name}"
             f" between {min_date_df} and {max_date_df}")
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
        st.write("* During the period they received a total of"
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
    # Compare total value share of {target_label}s to value of
    # all chosen entity
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
                 f" value of {target_label}s made to all entities"
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
                     f"({perc_val_c_r_V_pop:.2f}%) is {changetext} the average"
                     f" value of {target_label}s made to all entities"
                     f" ({perc_val_c_V_pop:.2f}%)")
    else:
        "No date range selected."
        st.write("---")

    st.write("### Topline Sponsorship Visuals")
    st.write("#### Click on any Visualisation to view it full screen.")
    left, centre, right = st.columns(3)
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
                                      Title="Sponsorships by Year and "
                                      "Entity Type",
                                      CalcType='sum',
                                      widget_key="donations_by_entity",
                                      use_container_width=True)
        # write function to find the top 3 RegulatedEntityTypes and share of
        # donations then update the text below.
        st.write('As can  be seen from the chart to the left'
                 'most cash donations are made to Political Parties.'
                 'This is not surprising as this is true for all '
                 'donations.')
        st.write('In 2016 we see an increase in donations to '
                 'Permitted Participants, this was due to the EU'
                 'Referendum, and the orgnaisations associated.')

    with centre:
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            vis.plot_pie_chart(df=cleaned_c_d_df,
                               category_column="RegEntity_Group",
                               value_column="Value",
                               category_label="RegEntity_Group",
                               value_label="Sponsopship Value £",
                               color_column="RegEntity_Group",
                               use_custom_colors=True,
                               hole=0.3,
                               title="Value of Sponsorships by "
                               "Political Entity",
                               widget_key="donations_by_entity_pie",
                               use_container_width=True)

            # vis.plot_bar_line_by_year(cleaned_c_d_df,
            #                           XValues="YearReceived",
            #                           YValue="Value",
            #                           GGroup="RegEntity_Group",
            #                           XLabel="Year",
            #                           YLabel="Value of Donations £",
            #                           Title="Value of Sponsorships by Year"
            #                                 " and Entity",
            #                           CalcType='sum',
            #                           use_custom_colors=True,
            #                           widget_key="Value_by_entity",
            #                           use_container_width=True)
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            st.write("The visual shows unsurprisingly that most donations are "
                     "made by individuals.")

    with right:
        # write code to find top 3 political entities by value of donations and
        # update the text below
        if cleaned_c_d_df.empty:
            st.write("No data available for the selected filters.")
            return
        else:
            vis.plot_bar_line_by_year(cleaned_c_d_df,
                                      XValues="YearReceived",
                                      YValue="Value",
                                      GGroup="DonorStatus",
                                      XLabel="Year",
                                      YLabel="Total Value (£)",
                                      Title="Value of Donor Types by Year",
                                      CalcType='sum',
                                      ChartType='bar',
                                      percentbars=True,
                                      widget_key="Value by type",
                                      use_container_width=True)
        st.write("The top 3 political entities by value of donations are "
                 "the Conservative Party, the Labour Party and the "
                 "Liberal Democrats. This is not surprising as these are "
                 "the three main political parties in the UK.")
        st.write("This pattern changes in 2016 to coincide with the EU "
                 "Referendum.  Here Medium size political entities such "
                 "as 'Vote Leave' and 'Leave.EU' were very active.")
