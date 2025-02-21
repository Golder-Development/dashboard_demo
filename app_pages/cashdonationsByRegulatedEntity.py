def cashdonationsregentity_body():
    """
    Displays the content of the Cash Donations to Political Party page.
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
    unique_reg_ent_pop = (
        ppcalc.get_regentity_ct(cleaned_df, filters)
        )
    unique_dono_pop = ppcalc.get_donors_ct(cleaned_df, filters)
    unique_dona_pop = ppcalc.get_donations_ct(cleaned_df, filters)
    total_val_pop = ppcalc.get_value_total(cleaned_df, filters)
    mean_val_pop = ppcalc.get_value_mean(cleaned_df, filters)
    # calculate average number of donations per regulated entity
    avg_dona_pop = (
        cleaned_df.groupby('RegulatedEntityId').size().mean()
    )
    # calculate average value of donations per regulated entity
    avg_val_pop = (
        cleaned_df.groupby('RegulatedEntityId')['Value'].mean().mean()
    )
    # calculate average number of donors per regulated entity
    avg_dono_pop = (
        cleaned_df.groupby('RegulatedEntityId')['DonorId'].nunique().mean()
    )
    # stdev of average number of donations per regulated entity
    std_dona_pop = (
        cleaned_df.groupby('RegulatedEntityId').size().std()
    )
    # stdev of average value of donations per regulated entity
    std_val_pop = (
        cleaned_df.groupby('RegulatedEntityId')['Value'].mean().std()
    )
    # stdev of average number of donors per regulated entity
    std_dono_pop = (
        cleaned_df.groupby('RegulatedEntityId')['DonorId'].nunique().std()
    )

    # Values for all entities, chosen date range and all donations
    unique_reg_ent_d = (
        ppcalc.get_regentity_ct(cleaned_d_df, filters)
        )
    unique_dono_d = ppcalc.get_donors_ct(cleaned_d_df, filters)
    unique_dona_d = ppcalc.get_donations_ct(cleaned_d_df, filters)
    total_val_d = ppcalc.get_value_total(cleaned_d_df, filters)
    mean_val_d = ppcalc.get_value_mean(cleaned_d_df, filters)
    avg_dona_pop_d = cleaned_d_df.groupby('RegulatedEntityId').size().mean()
    avg_val_pop_d = (
        cleaned_d_df.groupby('RegulatedEntityId')['Value'].mean().mean()
    )
    avg_dono_pop_d = (
        cleaned_d_df.groupby('RegulatedEntityId')['DonorId'].nunique().mean()
    )
    std_dona_pop_d = (
        cleaned_d_df.groupby('RegulatedEntityId').size().std()
    )
    std_val_pop_d = (
        cleaned_d_df.groupby('RegulatedEntityId')['Value'].mean().std()
    )
    std_dono_pop_d = (
        cleaned_d_df.groupby('RegulatedEntityId')['DonorId'].nunique().std()
    )
    # Values for all entities, all date range and target
    unique_reg_ent_c = (
        ppcalc.get_regentity_ct(cleaned_c_df, filters)
        )
    unique_dono_c = ppcalc.get_donors_ct(cleaned_c_df, filters)
    unique_dona_c = ppcalc.get_donations_ct(cleaned_c_df, filters)
    total_val_c = ppcalc.get_value_total(cleaned_c_df, filters)
    mean_val_c = ppcalc.get_value_mean(cleaned_c_df, filters)
    avg_dona_pop_c = cleaned_c_df.groupby('RegulatedEntityId').size().mean()
    avg_val_pop_c = (
        cleaned_c_df.groupby('RegulatedEntityId')['Value'].mean().mean()
    )
    avg_dono_pop_c = (
        cleaned_c_df.groupby('RegulatedEntityId')['DonorId'].nunique().mean()
    )
    std_dona_pop_c = cleaned_c_df.groupby('RegulatedEntityId').size().std()
    std_val_pop_c = (
        cleaned_c_df.groupby('RegulatedEntityId')['Value'].mean().std()
    )
    std_dono_pop_c = (
        cleaned_c_df.groupby('RegulatedEntityId')['DonorId'].nunique().std()
    )
    # Values for chosen entity, all date range and all Donations
    unique_reg_ent_r = (
        ppcalc.get_regentity_ct(cleaned_r_df, filters)
        )
    unique_dono_r = ppcalc.get_donors_ct(cleaned_r_df, filters)
    unique_dona_r = ppcalc.get_donations_ct(cleaned_r_df, filters)
    total_val_r = ppcalc.get_value_total(cleaned_r_df, filters)
    mean_val_r = ppcalc.get_value_mean(cleaned_r_df, filters)
    avg_dona_pop_r = cleaned_r_df.groupby('RegulatedEntityId').size().mean()
    avg_val_pop_r = (
        cleaned_r_df.groupby('RegulatedEntityId')['Value'].mean().mean()
    )
    avg_dono_pop_r = (
        cleaned_r_df.groupby('RegulatedEntityId')['DonorId'].nunique().mean()
    )
    std_dona_pop_r = (
        cleaned_r_df.groupby('RegulatedEntityId').size().std()
    )
    std_val_pop_r = (
        cleaned_r_df.groupby('RegulatedEntityId')['Value'].mean().std()
    )
    std_dono_pop_r = (
        cleaned_r_df.groupby('RegulatedEntityId')['DonorId'].nunique().std()
    )
    # Values for all entities, chosen date range and current target
    unique_reg_ent_c_d = (
        ppcalc.get_regentity_ct(cleaned_c_d_df, filters)
        )
    unique_dono_c_d = ppcalc.get_donors_ct(cleaned_c_d_df, filters)
    unique_dona_c_d = ppcalc.get_donations_ct(cleaned_c_d_df, filters)
    total_val_c_d = ppcalc.get_value_total(cleaned_c_d_df, filters)
    mean_val_c_d = ppcalc.get_value_mean(cleaned_c_d_df, filters)
    avg_dona_pop_c_d = (
        cleaned_c_d_df.groupby('RegulatedEntityId').size().mean()
    )
    avg_val_pop_c_d = (
        cleaned_c_d_df.groupby('RegulatedEntityId')['Value'].mean().mean())
    avg_dono_pop_c_d = (
        cleaned_c_d_df.groupby('RegulatedEntityId')['DonorId'].nunique().mean())
    std_dona_pop_c_d = (
        cleaned_c_d_df.groupby('RegulatedEntityId').size().std())
    std_val_pop_c_d = (
        cleaned_c_d_df.groupby('RegulatedEntityId')['Value'].mean().std())
    std_dono_pop_c_d = (
        cleaned_c_d_df.groupby('RegulatedEntityId')['DonorId'].nunique().std())
    # Values for chosen entity, date range and all donations
    unique_reg_ent_r_d = (
        ppcalc.get_regentity_ct(cleaned_r_d_df, filters)
        )
    unique_dono_r_d = ppcalc.get_donors_ct(cleaned_r_d_df, filters)
    unique_dona_r_d = ppcalc.get_donations_ct(cleaned_r_d_df, filters)
    total_val_r_d = ppcalc.get_value_total(cleaned_r_d_df, filters)
    mean_val_r_d = ppcalc.get_value_mean(cleaned_r_d_df, filters)
    avg_dona_pop_r_d = (
        cleaned_r_d_df.groupby('RegulatedEntityId').size().mean())
    avg_val_pop_r_d = (
        cleaned_r_d_df.groupby('RegulatedEntityId')['Value'].mean().mean())
    avg_dono_pop_r_d = (
        cleaned_r_d_df.groupby('RegulatedEntityId')['DonorId'].nunique().mean())
    std_dona_pop_r_d = (
        cleaned_r_d_df.groupby('RegulatedEntityId').size().std())
    std_val_pop_r_d = (
        cleaned_r_d_df.groupby('RegulatedEntityId')['Value'].mean().std())
    std_dono_pop_r_d = (
        cleaned_r_d_df.groupby('RegulatedEntityId')['DonorId'].nunique().std())
    # Values for chosen entity, date range and all donations
    unique_reg_ent_c_r = (
        ppcalc.get_regentity_ct(cleaned_c_r_df, filters)
        )
    unique_dono_c_r = ppcalc.get_donors_ct(cleaned_c_r_df, filters)
    unique_dona_c_r = ppcalc.get_donations_ct(cleaned_c_r_df, filters)
    total_val_c_r = ppcalc.get_value_total(cleaned_c_r_df, filters)
    mean_val_c_r = ppcalc.get_value_mean(cleaned_c_r_df, filters)
    avg_dona_pop_c_r = (
        cleaned_c_r_df.groupby('RegulatedEntityId').size().mean()
    )
    avg_val_pop_c_r = (
        cleaned_c_r_df.groupby('RegulatedEntityId')['Value'].mean().mean()
    )
    avg_dono_pop_c_r = (
        cleaned_c_r_df.groupby('RegulatedEntityId')['DonorId'].nunique().mean()
    )
    std_dona_pop_c_r = (
        cleaned_c_r_df.groupby('RegulatedEntityId').size().std()
    )
    std_val_pop_c_r = (
        cleaned_c_r_df.groupby('RegulatedEntityId')['Value'].mean().std()
    )
    std_dono_pop_c_r = (
        cleaned_c_r_df.groupby('RegulatedEntityId')['DonorId'].nunique().std()
    )
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
    avg_dona_pop_c_r_d = (
        cleaned_c_r_d_df.groupby('RegulatedEntityId').size().mean()
    )
    avg_val_pop_c_r_d = (
        cleaned_c_r_d_df.groupby('RegulatedEntityId')['Value'].mean().mean()
    )
    avg_dono_pop_c_r_d = (
        cleaned_c_r_d_df.groupby('RegulatedEntityId')['DonorId'].nunique().mean()
    )
    std_dona_pop_c_r_d = (
        cleaned_c_r_d_df.groupby('RegulatedEntityId').size().std()
    )
    std_val_pop_c_r_d = (
        cleaned_c_r_d_df.groupby('RegulatedEntityId')['Value'].mean().std()
    )
    std_dono_pop_c_r_d = (
        cleaned_c_r_d_df.groupby('RegulatedEntityId')['DonorId'].nunique().std()
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
            (unique_dona_r / unique_dona_pop) 
            if unique_dona_pop > 0 else 0
            )
        # Percent of all donations for chosen entity
        # to all donations for all entities and all time period
        perc_dona_r_V_pop = (
            (unique_dona_r / unique_dona_pop)
            if unique_dona_pop > 0 else 0
            )
        # Percent of all donations for all entities in time period
        # to all donations for all entities and all time period
        perc_dona_d_V_pop = (
            (unique_dona_d / unique_dona_pop)
            if unique_dona_pop > 0 else 0
            )
        # Percent of target donations for chosen entity all time period
        # to all donations for all entity all time period
        perc_dona_c_r_V_pop = (
            (unique_dona_c_d / unique_dona_pop)
            if unique_dona_pop > 0 else 0
            )
        # Percent of target donations for chosen entity all time period
        # to all donations for all entity all time period
        perc_dona_c_d_V_pop = (
            (unique_dona_c_d / unique_dona_pop)
            if unique_dona_pop > 0 else 0
            )
        # Percent of target donations for chosen entity all time period
        # to all donations for all entity all time period
        perc_dona_r_d_V_pop = (
            (unique_dona_r_d / unique_dona_pop)
            if unique_dona_pop > 0 else 0
            )
        # Percent of target donations for chosen entity all time period
        # to all donations for all entity all time period
        perc_dona_c_r_d_V_pop = (
            (unique_dona_c_r_d / unique_dona_pop)
            if unique_dona_pop > 0 else 0
            )
        # Percent of target donations in time period
        # to all donations for all entity in time period
        perc_dona_c_d_V_d = (
            (unique_dona_c_d / unique_dona_d)
            if unique_dona_d > 0 else 0
            )
        # Percent of all donations in time period for chosen entity
        # to all donations for all entity in time period
        perc_dona_r_d_V_d = (
            (unique_dona_r_d / unique_dona_d)
            if unique_dona_d > 0 else 0
            )
        # Percent of all donations for chosen entity in time period
        # to all donations for chosen entity all time period
        perc_dona_r_d_V_r = (
            (unique_dona_r_d / unique_dona_r)
            if unique_dona_r > 0 else 0
            )
        # Percent of targets for chosen entity all time
        # to all donations for chosen entity all time period
        perc_dona_c_r_V_r = (
            (unique_dona_c_r / unique_dona_r)
            if unique_dona_r > 0 else 0
            )
        # Percent of target donations in time period for chosen entity
        # to target donations for all entities and all time period
        perc_dona_c_r_d_V_c = (
            (unique_dona_c_r_d / unique_dona_c)
            if unique_dona_c > 0 else 0
            )
        # Percent of target donations in time period for chosen entity
        # to all donations for all entities and targetted time period
        perc_dona_c_r_d_V_d = (
            (unique_dona_c_r_d / unique_dona_d)
            if unique_dona_d > 0 else 0
            )
        # Percent of target donations in time period for chosen entity
        # to all donations for chosen entity and all time period
        perc_dona_c_r_d_V_r = (
            (unique_dona_c_r_d / unique_dona_r)
            if unique_dona_r > 0 else 0
            )
        # Percent of target donations in time period for chosen entity
        # to all donations for chosen entity and targetted time period
        perc_dona_c_r_d_V_r_d = (
            (unique_dona_c_r_d / unique_dona_r_d)
            if unique_dona_r_d > 0 else 0
            )
        # Percent of target donations in time period for chosen entity
        # to target donations for all entities and targetted time period
        perc_dona_c_r_d_V_c_d = (
            (unique_dona_c_r_d / unique_dona_c_d)
            if unique_dona_c_d > 0 else 0
            )
        # Percent of target donations in time period for chosen entity
        # to all donations for chosen entities and all time period
        perc_dona_c_r_d_V_c_r = (
            (unique_dona_c_r_d / unique_dona_c_r)
            if unique_dona_c_r > 0 else 0
            )

    # Value comparisons
    if create_value_comparisons:
        # percent of value of target donations for all entities
        # and all time period
        # to all donations for all entries and all time period
        perc_val_c_V_pop = (
            (total_val_c / total_val_pop)
            if total_val_pop > 0 else 0
            )
        # Percent of value of all donations for chosen entity
        # to all donations for all entities and all time period
        perc_val_r_V_pop = (
            (total_val_r / total_val_pop)
            if total_val_pop > 0 else 0
            )
        # Percent of value of all donations for all entities in time period
        # to all donations for all entities and all time period
        perc_val_d_V_pop = (
            (total_val_d / total_val_pop)
            if total_val_pop > 0 else 0
            )
        # Percent of value of target donations for chosen entity
        # all time period
        # to all donations for all entity all time period
        perc_val_c_r_V_pop = (
            (total_val_c_d / total_val_pop)
            if total_val_pop > 0 else 0
            )
        # Percent of value of target donations for chosen entity
        # all time period
        # to all donations for all entity all time period
        perc_val_c_d_V_pop = (
            (total_val_c_d / total_val_pop)
            if total_val_pop > 0 else 0
            )
        # Percent of value of target donations for chosen entity
        # all time period
        # to all donations for all entity all time period
        perc_val_r_d_V_pop = (
            (total_val_r_d / total_val_pop)
            if total_val_pop > 0 else 0
            )
        # Percent of value of target donations for chosen entity
        # all time period
        # to all donations for all entity all time period
        perc_val_c_r_d_V_pop = (
            (total_val_c_r_d / total_val_pop)
            if total_val_pop > 0 else 0
            )
        # Percent of value of target donations in time period
        # to all donations for all entity in time period
        perc_val_c_d_V_d = (
            (total_val_c_d / total_val_d)
            if total_val_d > 0 else 0
            )
        # Percent of value of all donations in time period for chosen entity
        # to all donations for all entity in time period
        perc_val_r_d_V_d = (
            (total_val_r_d / total_val_d)
            if total_val_d > 0 else 0
            )
        # Percent of value of all donations for chosen entity in time period
        # to all donations for chosen entity all time period
        perc_val_r_d_V_r = (
            (total_val_r_d / total_val_r)
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
            (total_val_c_r_d / total_val_c)
            if total_val_c > 0 else 0
            )
        # Percent of value of target donations in time period for chosen entity
        # to all donations for all entities and targetted time period
        perc_val_c_r_d_V_d = (
            (total_val_c_r_d / total_val_d)
            if total_val_d > 0 else 0
            )
        # Percent of value of target donations in time period for chosen entity
        # to all donations for chosen entity and all time period
        perc_val_c_r_d_V_r = (
            (total_val_c_r_d / total_val_r)
            if total_val_r > 0 else 0
            )
        # Percent of value of target donations in time period for chosen entity
        # to all donations for chosen entity and targetted time period
        perc_val_c_r_d_V_r_d = (
            (total_val_c_r_d / total_val_r_d)
            if total_val_r_d > 0 else 0
            )
        # Percent of value of target donations in time period for chosen entity
        # to target donations for all entities and targetted time period
        perc_val_c_r_d_V_c_d = (
            (total_val_c_r_d / total_val_c_d)
            if total_val_c_d > 0 else 0
            )
        # Percent of value of target donations in time period for chosen entity
        # to all donations for chosen entities and all time period
        perc_val_c_r_d_V_c_r = (
            (total_val_c_r_d / total_val_c_r)
            if total_val_c_r > 0 else 0
            )

    # Donor comparisons
    if create_donor_comparisons:
        # percent of donors of target donations for all entities
        # and all time period
        # to all donations for all entries and all time period
        perc_dono_c_V_pop = (
            (unique_dono_r / unique_dono_pop)
            if unique_dono_pop > 0 else 0
            )
        # Percent of donors of all donations for chosen entity
        # to all donations for all entities and all time period
        perc_dono_r_V_pop = (
            (unique_dono_r / unique_dono_pop)
            if unique_dono_pop > 0 else 0
            )
        # Percent of donors of all donations for all entities in time period
        # to all donations for all entities and all time period
        perc_dono_d_V_pop = (
            (unique_dono_d / unique_dono_pop)
            if unique_dono_pop > 0 else 0
            )
        # Percent of donors of target donations for chosen entity
        # all time period
        # to all donations for all entity all time period
        perc_dono_c_r_V_pop = (
            (unique_dono_c_d / unique_dono_pop)
            if unique_dono_pop > 0 else 0
            )
        # Percent of donors of target donations for chosen entity
        # all time period
        # to all donations for all entity all time period
        perc_dono_c_d_V_pop = (
            (unique_dono_c_d / unique_dono_pop)
            if unique_dono_pop > 0 else 0
            )
        # Percent of donors of target donations for chosen entity
        # all time period
        # to all donations for all entity all time period
        perc_dono_r_d_V_pop = (
            (unique_dono_r_d / unique_dono_pop)
            if unique_dono_pop > 0 else 0
            )
        # Percent of donors of target donations for chosen entity
        # all time period
        # to all donations for all entity all time period
        perc_dono_c_r_d_V_pop = (
            (unique_dono_c_r_d / unique_dono_pop)
            if unique_dono_pop > 0 else 0
            )
        # Percent of donors of target donations in time period
        # to all donations for all entity in time period
        perc_dono_c_d_V_d = (
            (unique_dono_c_d / unique_dono_d)
            if unique_dono_d > 0 else 0
            )
        # Percent of donors of all donations in time period for chosen entity
        # to all donations for all entity in time period
        perc_dono_r_d_V_d = (
            (unique_dono_r_d / unique_dono_d)
            if unique_dono_d > 0 else 0
            )
        # Percent of donors of all donations for chosen entity in time period
        # to all donations for chosen entity all time period
        perc_dono_r_d_V_r = (
            (unique_dono_r_d / unique_dono_r)
            if unique_dono_r > 0 else 0
            )
        # Percent of donors of targets for chosen entity all time
        # to all donations for chosen entity all time period
        perc_dono_c_r_V_r = (
            (unique_dono_c_r / unique_dono_r)
            if unique_dono_r > 0 else 0
            )
        # Percent of donors of target donations in time period for
        # chosen entity
        # to target donations for all entities and all time period
        perc_dono_c_r_d_V_c = (
            (unique_dono_c_r_d / unique_dono_c)
            if unique_dono_c > 0 else 0
            )
        # Percent of donors of target donations in time period for
        # chosen entity
        # to all donations for all entities and targetted time period
        perc_dono_c_r_d_V_d = (
            (unique_dono_c_r_d / unique_dono_d)
            if unique_dono_d > 0 else 0
            )
        # Percent of donors of target donations in time period for
        # chosen entity
        # to all donations for chosen entity and all time period
        perc_dono_c_r_d_V_r = (
            (unique_dono_c_r_d / unique_dono_r)
            if unique_dono_r > 0 else 0
            )
        # Percent of donors of target donations in time period for
        # chosen entity
        # to all donations for chosen entity and targetted time period
        perc_dono_c_r_d_V_r_d = (
            (unique_dono_c_r_d / unique_dono_r_d)
            if unique_dono_r_d > 0 else 0
            )
        # Percent of donors of target donations in time period for
        # chosen entity
        # to target donations for all entities and targetted time period
        perc_dono_c_r_d_V_c_d = (
            (unique_dono_c_r_d / unique_dono_c_d)
            if unique_dono_c_d > 0 else 0
            )
        # Percent of donors of target donations in time period for
        # chosen entity
        # to all donations for chosen entities and all time period
        perc_dono_c_r_d_V_c_r = (
            (unique_dono_c_r_d / unique_dono_c_r)
            if unique_dono_c_r > 0 else 0
            )

    # Regulated Entity comparisons
    if create_reg_entity_comparisons:
        # percent of regulated entitied of target donations for
        # all entities and all time period
        # to all donations for all entries and all time period
        perc_reg_ent_c_V_pop = (
            (unique_reg_ent_c / unique_reg_ent_pop)
            if unique_reg_ent_pop > 0 else 0
            )
        # Percent of regulated entitied of all donations for chosen entity
        # to all donations for all entities and all time period
        perc_reg_ent_r_V_pop = (
            (unique_reg_ent_r / unique_reg_ent_pop)
            if unique_reg_ent_pop > 0 else 0
            )
        # Percent of regulated entitied of all donations for
        # all entities in time period
        # to all donations for all entities and all time period
        perc_reg_ent_d_V_pop = (
            (unique_reg_ent_d / unique_reg_ent_pop)
            if unique_reg_ent_pop > 0 else 0
            )
        # Percent of regulated entitied of target donations for
        # chosen entity all time period
        # to all donations for all entity all time period
        perc_reg_ent_c_r_V_pop = (
            (unique_reg_ent_c_d / unique_reg_ent_pop)
            if unique_reg_ent_pop > 0 else 0
            )
        # Percent of regulated entitied of target donations for
        # chosen entity all time period
        # to all donations for all entity all time period
        perc_reg_ent_c_d_V_pop = (
            (unique_reg_ent_c_d / unique_reg_ent_pop)
            if unique_reg_ent_pop > 0 else 0
            )
        # Percent of regulated entitied of target donations for
        # chosen entity all time period
        # to all donations for all entity all time period
        perc_reg_ent_r_d_V_pop = (
            (unique_reg_ent_r_d / unique_reg_ent_pop)
            if unique_reg_ent_pop > 0 else 0
            )
        # Percent of regulated entitied of target donations for
        # chosen entity all time period
        # to all donations for all entity all time period
        perc_reg_ent_c_r_d_V_pop = (
            (unique_reg_ent_c_r_d / unique_reg_ent_pop)
            if unique_reg_ent_pop > 0 else 0
            )
        # Percent of regulated entitied of target donations in time period
        # to all donations for all entity in time period
        perc_reg_ent_c_d_V_d = (
            (unique_reg_ent_c_d / unique_reg_ent_d)
            if unique_reg_ent_d > 0 else 0
            )
        # Percent of regulated entitied of all donations in
        # time period for chosen entity
        # to all donations for all entity in time period
        perc_reg_ent_r_d_V_d = (
            (unique_reg_ent_r_d / unique_reg_ent_d)
            if unique_reg_ent_d > 0 else 0
            )
        # Percent of regulated entitied of all donations for
        # chosen entity in time period
        # to all donations for chosen entity all time period
        perc_reg_ent_r_d_V_r = (
            (unique_reg_ent_r_d / unique_reg_ent_r)
            if unique_reg_ent_r > 0 else 0
            )
        # Percent of regulated entitied of targets for chosen entity all time
        # to all donations for chosen entity all time period
        perc_reg_ent_c_r_V_r = (
            (unique_reg_ent_c_r / unique_reg_ent_r)
            if unique_reg_ent_r > 0 else 0
            )
        # Percent of regulated entitied of target donations
        # in time period for chosen entity
        # to target donations for all entities and all time period
        perc_reg_ent_c_r_d_V_c = (
            (unique_reg_ent_c_r_d / unique_reg_ent_c)
            if unique_reg_ent_c > 0 else 0
            )
        # Percent of regulated entitied of target donations in
        # time period for chosen entity
        # to all donations for all entities and targetted time period
        perc_reg_ent_c_r_d_V_d = (
            (unique_reg_ent_c_r_d / unique_reg_ent_d)
            if unique_reg_ent_d > 0 else 0
            )
        # Percent of regulated entitied of target donations in
        # time period for chosen entity
        # to all donations for chosen entity and all time period
        perc_reg_ent_c_r_d_V_r = (
            (unique_reg_ent_c_r_d / unique_reg_ent_r)
            if unique_reg_ent_r > 0 else 0
            )
        # Percent of regulated entitied of target donations in
        # time period for chosen entity
        # to all donations for chosen entity and targetted time period
        perc_reg_ent_c_r_d_V_r_d = (
            (unique_reg_ent_c_r_d / unique_reg_ent_r_d)
            if unique_reg_ent_r_d > 0 else 0
            )
        # Percent of regulated entitied of target donations in
        # time period for chosen entity
        # to target donations for all entities and targetted time period
        perc_reg_ent_c_r_d_V_c_d = (
            (unique_reg_ent_c_r_d / unique_reg_ent_c_d)
            if unique_reg_ent_c_d > 0 else 0
            )
        # Percent of regulated entitied of target donations in
        # time period for chosen entity
        # to all donations for chosen entities and all time period
        perc_reg_ent_c_r_d_V_c_r = (
            (unique_reg_ent_c_r_d / unique_reg_ent_c_r)
            if unique_reg_ent_c_r > 0 else 0
            )

    # Format selected dates for inclusion in text
    min_date_df = start_date.date()
    max_date_df = end_date.date()

    # Create a table of the results
    st.write("### Comparison Table")
    comparison_data = {
        "Metric": [
            "Unique Regulated Entities",
            "Unique Donors",
            "Unique Donations",
            "Total Value",
            "Mean Value",
            "Avg Donations per Entity",
            "Avg Value per Entity",
            "Avg Donors per Entity",
            "Std Dev Donations per Entity",
            "Std Dev Value per Entity",
            "Std Dev Donors per Entity"
        ],
        f"All Donations:\n{min_date} to {max_date}": [
            unique_reg_ent_pop, unique_dono_pop, unique_dona_pop,
            total_val_pop,
            mean_val_pop,
            avg_dona_pop,
            avg_val_pop,
            avg_dono_pop,
            std_dona_pop,
            std_val_pop,
            std_dono_pop
        ],
        f"{target_label}s:\n{min_date} to {max_date}": [
            unique_reg_ent_c, unique_dono_c, unique_dona_c,
            total_val_c,
            mean_val_c,
            avg_dona_pop_c,
            avg_val_pop_c,
            avg_dono_pop_c,
            std_dona_pop_c,
            std_val_pop_c,
            std_dono_pop_c
        ],
        f"{selected_entity_name}:\n{min_date} to {max_date}": [
            unique_reg_ent_r, unique_dono_r, unique_dona_r,
            total_val_r,
            mean_val_r,
            avg_dona_pop_r,
            avg_val_pop_r,
            avg_dono_pop_r,
            std_dona_pop_r,
            std_val_pop_r,
            std_dono_pop_r
        ],
        f"{selected_entity_name},\n{target_label}s:\n{min_date} to {max_date}": [
            unique_reg_ent_c_r, unique_dono_c_r, unique_dona_c_r,
            total_val_c_r,
            mean_val_c_r,
            avg_dona_pop_c_r,
            avg_val_pop_c_r,
            avg_dono_pop_c_r,
            std_dona_pop_c_r,
            std_val_pop_c_r,
            std_dono_pop_c_r
        ],
        f"All donations:\n{min_date_df} to {max_date_df}": [
            unique_reg_ent_d, unique_dono_d, unique_dona_d,
            total_val_d,
            mean_val_d,
            avg_dona_pop_d,
            avg_val_pop_d,
            avg_dono_pop_d,
            std_dona_pop_d,
            std_val_pop_d,
            std_dono_pop_d
        ],
        f"{target_label}s:\n{min_date_df} to {max_date_df}": [
            unique_reg_ent_c_d, unique_dono_c_d, unique_dona_c_d,
            total_val_c_d,
            mean_val_c_d,
            avg_dona_pop_c_d,
            avg_val_pop_c_d,
            avg_dono_pop_c_d,
            std_dona_pop_c_d,
            std_val_pop_c_d,
            std_dono_pop_c_d
        ],
        f"{selected_entity_name}:\n{min_date_df} to {max_date_df}": [
            unique_reg_ent_r_d, unique_dono_r_d, unique_dona_r_d,
            total_val_r_d,
            mean_val_r_d,
            avg_dona_pop_r_d,
            avg_val_pop_r_d,
            avg_dono_pop_r_d,
            std_dona_pop_r_d,
            std_val_pop_r_d,
            std_dono_pop_r_d
        ],
        f"{selected_entity_name},\n{target_label}s:\n{min_date_df} to {max_date_df}": [
            unique_reg_ent_c_r_d, unique_dono_c_r_d, unique_dona_c_r_d,
            total_val_c_r_d,
            mean_val_c_r_d,
            avg_dona_pop_c_r_d,
            avg_val_pop_c_r_d,
            avg_dono_pop_c_r_d,
            std_dona_pop_c_r_d,
            std_val_pop_c_r_d,
            std_dono_pop_c_r_d
        ]
    }

    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(
        comparison_df.style
        .format(
            {
                f"All Donations: {min_date} to {max_date}": "{:.2f}",
                f"{target_label}s: {min_date} to {max_date}": "{:.2f}",
                f"{selected_entity_name}: {min_date} to {max_date}": "{:.2f}",
                f"{selected_entity_name}, {target_label}s: {min_date} to {max_date}": "{:.2f}",
                f"All Donations: {min_date_df} to {max_date_df}": "{:.2f}",
                f"{target_label}s: {min_date_df} to {max_date_df}": "{:.2f}",
                f"{selected_entity_name}: {min_date_df} to {max_date_df}": "{:.2f}",
                f"{selected_entity_name}, {target_label}s: {min_date_df} to {max_date_df}": "{:.2f}",
                "Total Value": "£{:.2f}",
                "Mean Value": "£{:.2f}",
                "Avg Value per Entity": "£{:.2f}",
                "Std Dev Value per Entity": "£{:.2f}",
            }
        )
        .set_properties(**{"width": "150px"})
    )

    # Create a table of percentage comparisons
    st.write("### Percentage Comparison Table")

    # Define percentage comparison data
    percentage_comparison_data = {
        "Metric": [
            f"{target_label}s vs All Donations: {min_date} to {max_date}",
            f"{selected_entity_name} vs All Donations: {min_date} to {max_date}",
            f"All Donations: {min_date_df} to {max_date_df} vs {min_date} to {max_date}",
            f"{selected_entity_name} {target_label}s vs All Donations: {min_date} to {max_date}",
            f"{target_label}: {min_date_df} to {max_date_df} vs All Donations: {min_date} to {max_date}",
            f"{selected_entity_name}: {min_date_df} to {max_date_df} vs All Donations: {min_date} to {max_date}",
            f"{selected_entity_name} {target_label}s: {min_date_df} to {max_date_df} vs All Donations: {min_date} to {max_date}",
        ],
        "Percentage Of Donations": [
            perc_dona_c_V_pop,
            perc_dona_r_V_pop,
            perc_dona_d_V_pop,
            perc_dona_c_r_V_pop,
            perc_dona_c_d_V_pop,
            perc_dona_r_d_V_pop,
            perc_dona_c_r_d_V_pop
        ],
        "Percentage Of Value": [
            perc_val_c_V_pop,
            perc_val_r_V_pop,
            perc_val_d_V_pop,
            perc_val_c_r_V_pop,
            perc_val_c_d_V_pop,
            perc_val_r_d_V_pop,
            perc_val_c_r_d_V_pop
        ],
        "Percentage Of Donors": [
            perc_dono_c_V_pop,
            perc_dono_r_V_pop,
            perc_dono_d_V_pop,
            perc_dono_c_r_V_pop,
            perc_dono_c_d_V_pop,
            perc_dono_r_d_V_pop,
            perc_dono_c_r_d_V_pop
        ],
        "Percentage Of Entities": [
            perc_reg_ent_c_V_pop,
            perc_reg_ent_r_V_pop,
            perc_reg_ent_d_V_pop,
            perc_reg_ent_c_r_V_pop,
            perc_reg_ent_c_d_V_pop,
            perc_reg_ent_r_d_V_pop,
            perc_reg_ent_c_r_d_V_pop
        ]
    }

    # Convert data to DataFrame
    percentage_comparison_df = pd.DataFrame(percentage_comparison_data)

    # Format percentage columns to display as percentages
    st.dataframe(
        percentage_comparison_df.style
        .format({
            "Percentage Of Donations": "{:.2%}",
            "Percentage Of Value": "{:.2%}",
            "Percentage Of Donors": "{:.2%}",
            "Percentage Of Entities": "{:.2%}",
        })
        .set_properties(**{"width": "150px"})
    )

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
