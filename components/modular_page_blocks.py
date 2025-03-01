import streamlit as st
import datetime as dt
from data.data_loader import load_cleaned_data
from components.filters import filter_by_date, apply_filters
from components.calculations import (
    compute_summary_statistics,
    get_mindate,
    get_maxdate,
    calculate_percentage,
    format_number,
)
from components.Visualisations import plot_custom_bar_chart, plot_bar_line_by_year
from components.text_management import (
    load_page_text,
    check_password,
    save_text,
    toggle_soft_delete,
    permanent_delete,
)
from utils.logger import logger
from utils.logger import log_function_call  # Import decorator

@log_function_call
def load_and_filter_data(filter_key, pagereflabel):
    """Loads and filters dataset based on filter_key from session state."""
    cleaned_df = st.session_state["data_clean"]
    if cleaned_df is None:
        st.error("No data found. Please upload a dataset.")
        return None, None

    min_date = get_mindate(cleaned_df).date()
    max_date = get_maxdate(cleaned_df).date()

    # Convert selected dates to datetime
    start_date, end_date = (
        dt.datetime.combine(min_date, dt.datetime.min.time()),
        dt.datetime.combine(max_date, dt.datetime.max.time()),
    )

    # Apply filters
    current_target = st.session_state["filter_def"].get(filter_key)
    cleaned_d_df = filter_by_date(cleaned_df, start_date, end_date)
    filtered_df = apply_filters(cleaned_d_df, current_target, logical_operator="or")

    return cleaned_df, filtered_df


@log_function_call
def display_summary_statistics(filtered_df, overall_df, target_label, pageref_label):
    """Displays summary statistics for the given dataset."""
    pageref_label_dss = pageref_label + "_dss"
    if filtered_df is None or filtered_df.empty:
        st.warning(f"No {target_label}s found for the selected filters.")
        return

    min_date_df = get_mindate(filtered_df).date()
    max_date_df = get_maxdate(filtered_df).date()
    tstats = compute_summary_statistics(filtered_df, {})
    ostats = compute_summary_statistics(overall_df, {})
    perc_target = calculate_percentage(
        tstats["unique_donations"], ostats["unique_donations"]
    )

    st.write(
        f"## Summary Statistics for {target_label}s, "
        f"from {min_date_df} to {max_date_df}"
    )

    cols = st.columns(6)
    stats_map = [
        (f"Total {target_label}", f"£{format_number(tstats['total_value'])}"),
        (f"{target_label} % of Total Donations", f"{perc_target:.0f}%"),
        (f"{target_label} Donations", f"{format_number(tstats['unique_donations'])}"),
        (f"Mean {target_label} Value", f"£{format_number(tstats['mean_value'])}"),
        (f"Total {target_label} Entities", f"{format_number(tstats['unique_reg_entities'])}"),
        (f"Total {target_label} Donors", f"{format_number(tstats['unique_donors'])}"),
    ]
    for col, (label, value) in zip(cols, stats_map):
        col.metric(label=label, value=value)

    return min_date_df, max_date_df, tstats, ostats, perc_target


@log_function_call
def display_visualizations(graph_df, target_label, pageref_label):
    pageref_label_vis = pageref_label + "_vis"
    """Displays charts for the given dataset."""
    if graph_df.empty:
        st.warning(f"No data available for {target_label}s.")
        return

    left_column, right_column = st.columns(2)

    with left_column:
        left_widget_graph_key = "left" + pageref_label_vis
        plot_bar_line_by_year(
            graph_df,
            XValues="YearReceived",
            YValues="Value",
            GroupData="RegulatedEntityType",
            XLabel="Year",
            YLabel="Value of Donations £",
            Title=f"Value of {target_label}s by" " Year and Entity",
            CalcType="sum",
            use_custom_colors=False,
            widget_key=left_widget_graph_key,
            ChartType="Bar",
            LegendTitle="Political Entity Type",
            percentbars=True,
            y_scale="linear",
        )
        right_widget_graph_key = "right" + pageref_label_vis
    with right_column:
        plot_bar_line_by_year(
            graph_df,
            XValues="YearReceived",
            YValues="EventCount",
            GroupData="RegEntity_Group",
            XLabel="Year",
            YLabel="Donations",
            Title=f"Donations of {target_label}s by Year and Entity",
            CalcType="sum",
            use_custom_colors=True,
            percentbars=False,
            LegendTitle="Political Entity",
            ChartType="line",
            y_scale="linear",
            widget_key=right_widget_graph_key,
        )


@log_function_call
def display_textual_insights(
    pageref_label, target_label, min_date, max_date, tstats, ostats, perc_target
):
    """Displays insights and explanations."""
    pageref_label_ti = pageref_label + "_ti"
    page_texts = load_page_text(pageref_label_ti)

    # Admin Section - Manage multiple text elements
    if st.session_state.security["is_admin"]:
        st.subheader(f"Manage Text for {pageref_label_ti}")

        # Existing text elements
        if page_texts:
            for text_key, text_data in page_texts.items():
                is_deleted = text_data["is_deleted"]
                text_value = text_data["text"]

                if is_deleted:
                    st.markdown(f"⚠️ **(Deleted)** {text_key}:")
                else:
                    st.text_area(
                        f"Edit {text_key}:", value=text_value, key=f"edit_{text_key}"
                    )

                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                with col1:
                    if not is_deleted and st.button(
                        f"Save {text_key}", key=f"save_{text_key}"
                    ):
                        new_value = st.session_state[f"edit_{text_key}"]
                        save_text(pageref_label, text_key, new_value)
                        st.success(f"Updated {text_key}!")

                with col2:
                    if not is_deleted and st.button(
                        f"Soft Delete {text_key}", key=f"delete_{text_key}"
                    ):
                        toggle_soft_delete(pageref_label, text_key, True)
                        st.warning(f"Soft Deleted {text_key}!")
                        st.rerun()

                with col3:
                    if is_deleted and st.button(
                        f"Restore {text_key}", key=f"restore_{text_key}"
                    ):
                        toggle_soft_delete(pageref_label, text_key, False)
                        st.success(f"Restored {text_key}!")
                        st.rerun()

                with col4:
                    if st.button(f"🗑️ Delete {text_key}", key=f"perm_delete_{text_key}"):
                        permanent_delete(pageref_label, text_key)
                        st.error(f"Permanently Deleted {text_key}!")
                        st.rerun()

        # Add new text element
        st.subheader("Add a New Text Element")
        new_key = st.text_input("New Text Element Name:")
        new_value = st.text_area("Text Content:")

        if st.button("Add Text Element"):
            if new_key.strip() == "":
                st.error("Text Element Name cannot be empty.")
            elif new_key in page_texts:
                st.error("A text element with this name already exists.")
            else:
                save_text(pageref_label_ti, new_key, new_value)
                st.success(f"Added {new_key}!")
                st.experimental_rerun()

    # Display all visible (not deleted) text elements for the page
    st.subheader(f"Explanations for {target_label}")
    for text_key, text_data in page_texts.items():
        if not text_data["is_deleted"]:
            st.write(f"**{text_key}:** {text_data['text']}")

    # Logout button
    if st.session_state.security["is_admin"]:
        if st.button("Logout"):
            st.session_state.security["is_admin"] = False
            st.experimental_rerun()

    st.write("---")
    left, right = st.columns(2)

    with left:
        st.write("## Explanation")
        st.write(
            f"* {target_label}s are recorded forms of"
            " support for political entities."
        )
        st.write(
            f"* Between {min_date} and {max_date},"
            f" {format_number(tstats['unique_donations'])} {target_label}s "
            f"were made to {format_number(tstats['unique_reg_entities'])}"
            " regulated entities."
        )
        st.write(
            "* These had a mean value of "
            f"£{format_number(tstats['mean_value'])} "
            f"and were made by {format_number(tstats['unique_donors'])}"
            " unique donors."
        )
        st.write(
            f"* {target_label}s accounted for {perc_target:.0f}% of"
            " all political donations."
        )

    with right:
        st.write("### Key Observations")
        st.write(
            "* Political donations fluctuate significantly over time,"
            " especially during elections."
        )
        st.write("* Funding sources and types of" " donors impact donation trends.")


@log_function_call
def load_and_filter_perentity(group_entity, filter_key, pageref_label):
    """Loads and filters dataset based on filter_key from session state."""
    cleaned_df = st.session_state["data_clean"]
    if cleaned_df is None:
        st.error("No data found. Please upload a dataset.")
        return None, None, None, None, None, None, None, None

    # Get min and max dates from the dataset
    min_date = dt.datetime.combine(get_mindate(cleaned_df), dt.datetime.min.time())
    max_date = dt.datetime.combine(get_maxdate(cleaned_df), dt.datetime.min.time())

    # # Add a date range slider to filter by received date
    date_range2 = st.slider(
        "Select Date Range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD",
    )

    # # Extract start and end dates from the slider
    start_date, end_date = date_range2
    start_date = dt.datetime.combine(start_date, dt.datetime.min.time())
    end_date = dt.datetime.combine(end_date, dt.datetime.max.time())

    # --- Dropdown for Regulated Entity ---
    # Create a mapping of RegulatedEntityName -> RegulatedEntityId
    entity_mapping = dict(
        zip(cleaned_df["RegulatedEntityName"], cleaned_df["RegulatedEntityId"])
    )

    # Add "All" as an option and create a dropdown that displays names but
    # returns IDs
    selected_entity_name = st.selectbox(
        "Filter by Regulated Entity", ["All"] + sorted(entity_mapping.keys())
    )

    # Get the corresponding ID for filtering
    selected_entity_id = entity_mapping.get(selected_entity_name, None)

    # Apply filters
    current_target = st.session_state["filter_def"].get(filter_key)

    # Define filter condition
    filters = {}
    # Apply filters
    entity_filter = {}
    entity_filter = (
        {"RegulatedEntityId": selected_entity_id}
        if selected_entity_name != "All"
        else {}
    )
    # # Filter by date range
    date_filter = (cleaned_df["ReceivedDate"] >= start_date) & (
        cleaned_df["ReceivedDate"] <= end_date
    )
    # Create dataframe for chosen date range and all entities
    if date_filter is not None:
        cleaned_d_df = cleaned_df[date_filter]
    else:
        cleaned_d_df = cleaned_df
    # Create dataframe for chosen target all date range and all entities
    if current_target:
        cleaned_c_df = apply_filters(cleaned_df, current_target)
    else:
        cleaned_c_df = cleaned_df
    # Create dataframe for chosen entity all date range and all entities
    if entity_filter:
        cleaned_r_df = apply_filters(cleaned_df, entity_filter)
    else:
        cleaned_r_df = cleaned_df
    # Create dataframe for chosen entity and date range all measures
    cleaned_r_d_df = cleaned_r_df[date_filter] if date_filter.any() else cleaned_r_df
    # Create dataframe for chosen target and date range all entities
    cleaned_c_d_df = apply_filters(cleaned_d_df, current_target)
    # Create dataframe for chosen target and entity all dates
    cleaned_c_r_df = apply_filters(cleaned_r_df, current_target)
    # Create dataframe for chosen target, entity and date range
    cleaned_c_r_d_df = apply_filters(cleaned_r_d_df, current_target)

    return (
        cleaned_df,
        cleaned_d_df,
        cleaned_c_df,
        cleaned_r_df,
        cleaned_r_d_df,
        cleaned_c_d_df,
        cleaned_c_r_df,
        cleaned_c_r_d_df,
    )


@log_function_call
def load_and_filter_pergroup(group_entity, filter_key, pageref_label):
    """Loads and filters dataset based on filter_key from session state."""
    cleaned_df = st.session_state["data_clean"]
    if cleaned_df is None:
        st.error("No data found. Please upload a dataset.")
        return None, None

    # Get min and max dates from the dataset
    min_date = dt.datetime.combine(get_mindate(cleaned_df), dt.datetime.min.time())
    max_date = dt.datetime.combine(get_maxdate(cleaned_df), dt.datetime.min.time())

    # # Add a date range slider to filter by received date
    date_range2 = st.slider(
        "Select Date Range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD",
    )

    # # Extract start and end dates from the slider
    start_date, end_date = date_range2
    start_date = dt.datetime.combine(start_date, dt.datetime.min.time())
    end_date = dt.datetime.combine(end_date, dt.datetime.max.time())

    # --- Dropdown for chosen grouping ---
    filterentityname = group_entity + "Name"
    filterentityid =group_entity + "Id"
    # check filterentityname and filterentityid are in the dataframe
    if (
        filterentityname not in cleaned_df.columns
        or filterentityid not in cleaned_df.columns
    ):
        st.error(
            f"Error: chosen filter {filterentityname} or"
            f" {filterentityid} not in the dataset."
        )
        return (None, None, None, None, None, None, None, None)

    # Create a mapping of RegulatedEntityName -> RegulatedEntityId
    entity_mapping = dict(zip(cleaned_df[filterentityname], cleaned_df[filterentityid]))

    # Add "All" as an option and create a dropdown that displays names but
    # returns IDs
    selected_entity_name = st.selectbox(
        f"Filter by {group_entity}", ["All"] + sorted(entity_mapping.keys())
    )

    # Get the corresponding ID for filtering
    selected_entity_id = entity_mapping.get(selected_entity_name, None)

    # Apply filters
    current_target = st.session_state["filter_def"].get(filter_key)

    # Define filter condition
    filters = {}
    # Apply filters
    entity_filter = {}
    entity_filter = (
        {filterentityid: selected_entity_id} if selected_entity_name != "All" else {}
    )
    # # Filter by date range
    date_filter = (cleaned_df["ReceivedDate"] >= start_date) & (
        cleaned_df["ReceivedDate"] <= end_date
    )
    # Create dataframe for chosen date range and all entities
    if date_filter is not None:
        cleaned_d_df = cleaned_df[date_filter]
    else:
        cleaned_d_df = cleaned_df
    # Create dataframe for chosen target all date range and all entities
    if current_target:
        cleaned_c_df = apply_filters(cleaned_df, current_target)
    else:
        cleaned_c_df = cleaned_df
    # Create dataframe for chosen entity all date range and all entities
    if entity_filter:
        cleaned_r_df = apply_filters(cleaned_df, entity_filter)
    else:
        cleaned_r_df = cleaned_df
    # Create dataframe for chosen entity and date range all measures
    cleaned_r_d_df = cleaned_r_df[date_filter] if date_filter.any() else cleaned_r_df
    # Create dataframe for chosen target and date range all entities
    cleaned_c_d_df = apply_filters(cleaned_d_df, current_target)
    # Create dataframe for chosen target and entity all dates
    cleaned_c_r_df = apply_filters(cleaned_r_df, current_target)
    # Create dataframe for chosen target, entity and date range
    cleaned_c_r_d_df = apply_filters(cleaned_r_d_df, current_target)

    return (
        cleaned_df,
        cleaned_d_df,
        cleaned_c_df,
        cleaned_r_df,
        cleaned_r_d_df,
        cleaned_c_d_df,
        cleaned_c_r_df,
        cleaned_c_r_d_df,
    )


@log_function_call
def topline_summary_block(target_label, min_date_df, max_date_df, tstats, perc_cash_donations_d):
    st.write(f"## Summary Statistics for {target_label},"
             f" from {min_date_df} to {max_date_df}")
    left, a, b, mid, c, right = st.columns(6)
    with left:
        st.metric(label=f"Total {target_label}",
                  value=f"£{tstats['total_value']:,.0f}")
    with a:
        st.metric(label=f"{target_label} % of Total Donations",
                  value=f"{perc_cash_donations_d:.2f}%")
    with b:
        st.metric(label=f"{target_label} Donations",
                  value=f"{tstats['unique_donations']:,}")
    with mid:
        st.metric(label=f"Mean {target_label} Value",
                  value=f"£{tstats['mean_value']:,.0f}")
    with c:
        st.metric(label=f"Total {target_label} Entities",
                  value=f"{tstats['unique_reg_entities']:,}")
    with right:
        st.metric(label=f"Total {target_label} Donors",
                  value=f"{tstats['unique_donors']:,}")
    st.write("---")