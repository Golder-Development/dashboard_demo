import streamlit as st
import datetime as dt
from components.filters import filter_by_date, apply_filters
from components.calculations import (
    compute_summary_statistics,
    get_mindate,
    get_maxdate,
    calculate_percentage,
    format_number,
)
from Visualisations import ( 
    plot_bar_line,
    plot_pie_chart,
    plot_bar_chart,
    plot_regressionplot
    )
from components.text_management import (
    load_page_text,
    save_text,
    )
from utils.logger import streamlit_logger as logger, log_functioncall


@log_function_call("StreamlitApp")
def load_and_filter_data(filter_key, pagereflabel):
    """Loads and filters dataset based on filter_key from session state."""
    cleaned_df = st.session_state.data_clean
    if cleaned_df is None:
        st.error("No data found. Please upload a dataset.")
        return None, None

    if "min_date" in st.session_state and "max_date" in st.session_state:
        min_date = st.session_state.min_date
        max_date = st.session_state.max_date
    else:
        min_date = cleaned_df["ReceivedDate"].min().date()
        max_date = cleaned_df["ReceivedDate"].max().date()
        st.session_state.min_date = min_date
        st.session_state.max_date = max_date

    # Convert selected dates to datetime
    start_date, end_date = (
        dt.datetime.combine(min_date, dt.datetime.min.time()),
        dt.datetime.combine(max_date, dt.datetime.max.time()),
    )

    # Apply filters
    current_target = st.session_state["filter_def"].get(filter_key)
    cleaned_d_df = filter_by_date(cleaned_df, start_date, end_date)
    filtered_df = apply_filters(cleaned_d_df,
                                current_target,
                                logical_operator="or")

    return cleaned_df, filtered_df


@log_function_call("StreamlitApp")
def display_summary_statistics(filtered_df, overall_df, target_label,
                               pageref_label):
    """Displays summary statistics for the given dataset."""
    if filtered_df is None or filtered_df.empty:
        if logger.level <= 20:
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
        (f"Total {target_label}",
         f"£{format_number(tstats['total_value'])}"),
        (f"{target_label} % of Total Donations",
         f"{perc_target:.0f}%"),
        (f"{target_label} Donations",
         f"{format_number(tstats['unique_donations'])}"),
        (f"Mean {target_label} Value",
         f"£{format_number(tstats['mean_value'])}"),
        (f"Total {target_label} Entities",
         f"{format_number(tstats['unique_reg_entities'])}"),
        (f"Total {target_label} Donors",
         f"{format_number(tstats['unique_donors'])}"),
    ]
    for col, (label, value) in zip(cols, stats_map):
        col.metric(label=label, value=value)

    return min_date_df, max_date_df, tstats, ostats, perc_target


@log_function_call("StreamlitApp")
def display_visualizations(graph_df, target_label, pageref_label):
    pageref_label_vis = pageref_label + "_vis"
    """Displays charts for the given dataset."""
    if graph_df.empty:
        if logger.level <= 20:
            st.warning(f"No data available for {target_label}s.")
        return

    left_column, right_column = st.columns(2)

    with left_column:
        left_widget_graph_key = "left" + pageref_label_vis
        plot_bar_line.plot_bar_line_by_year(
            graph_df,
            XValues="YearReceived",
            YValues="Value",
            GroupData="Party_Group",
            XLabel="Year",
            YLabel="Value of Donations £",
            Title=f"Value of {target_label}s by" " Year and Entity",
            CalcType="sum",
            use_custom_colors=True,
            widget_key=left_widget_graph_key,
            ChartType="Bar",
            LegendTitle="Political Entity Type",
            percentbars=True,
            y_scale="linear",
        )
    with right_column:
        right_widget_graph_key = "right" + pageref_label_vis
        plot_bar_line.plot_bar_line_by_year(
            graph_df,
            XValues="YearReceived",
            YValues="EventCount",
            GroupData="Party_Group",
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


@log_function_call("StreamlitApp")
def display_textual_insights_predefined(pageref_label, target_label, min_date,
                             max_date, tstats, ostats, perc_target):
    """Displays predefined text elements for a given page."""
    st.write("## Observations")
    st.write(f"* {target_label}s are recorded forms of support for political entities.")
    st.write(f"* Between {min_date} and {max_date}, {format_number(tstats['unique_donations'])} {target_label}s "
             f"were made to {format_number(tstats['unique_reg_entities'])} regulated entities."
             f" These had a mean value of £{format_number(tstats['mean_value'])} "
             f"and were made by {format_number(tstats['unique_donors'])} unique donors.")
    st.write(f"* The most active donor of {target_label} was {tstats['most_common_donor'][0]}. "
             f"They made {format_number(tstats['most_common_donor'][1])} donations.")
    st.write(f"* The most generous donor of {target_label} was {tstats['most_valuable_donor'][0]}, "
             f"who donated £{format_number(tstats['most_valuable_donor'][1])}.")
    st.write(f"* The most common recipient of {target_label}s was {tstats['most_common_entity'][0]}, "
             f"they received {format_number(tstats['most_common_entity'][1])} donations.")
    st.write(f"* {tstats['most_valuable_entity'][0]} received £{format_number(tstats['most_valuable_entity'][1])} "
             f" of {target_label}s.")


def display_textual_insights_custom(pageref_label, target_label):
    """Displays stored text elements for a given page. Allows edits only if admin is logged in."""
    page_texts = load_page_text(pageref_label)

    st.subheader(f"Explanations for {target_label}")

    if not page_texts:
        st.info("No text available for this section.")
        return  # ✅ Stop execution if no text exists

    for text_key, text_data in page_texts.items():
        is_deleted = text_data.get("is_deleted", False)
        text_value = text_data.get("text", "")

        if is_deleted:
            continue  # ✅ Skip deleted texts

        # Display text for all users
        st.write(f"**{text_key}:** {text_value}")

        # ✅ Check admin status safely
        is_admin = st.session_state.get("security", {}).get("is_admin", False)

        if is_admin:
            new_value = st.text_area(
                f"Edit {text_key}:", value=text_value, key=f"edit_{pageref_label}_{text_key}"
            )

            if st.button(f"Save {text_key}", key=f"save_{pageref_label}_{text_key}"):
                save_text(pageref_label, text_key, new_value)
                st.success(f"Updated {text_key}!")
                st.rerun()


def load_and_filter_pergroup(group_entity, filter_key, pageref_label):
    """Loads and filters dataset based on filter_key from session state."""
    cleaned_df = st.session_state["data_clean"]
    if cleaned_df is None:
        st.error(f"No data found. Please upload a dataset. {__name__}")
        logger.error(f"No data found. Please upload a dataset. {__name__}")
        return None, None

    # Get min and max dates from the dataset
    min_date = dt.datetime.combine(get_mindate(cleaned_df),
                                   dt.datetime.min.time())
    max_date = dt.datetime.combine(get_maxdate(cleaned_df),
                                   dt.datetime.min.time())

    # Date range slider
    date_range2 = st.slider(
        "Select Date Range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD",
    )

    start_date, end_date = date_range2
    start_date = dt.datetime.combine(start_date, dt.datetime.min.time())
    end_date = dt.datetime.combine(end_date, dt.datetime.max.time())

    # Dictionary to hold friendly titles and relevant numeric reference fields
    group_entity_options = {
        "Donor": ("DonorName", "DonorId"),
        "Donor Classification": ("DonorStatus", "DonorStatusInt"),
        "Regulated Entity": ("RegulatedEntityName", "RegulatedEntityId"),
        "Recipients Classification": ("RegulatedDoneeType", None),
        "Nature of Donation": ("NatureOfDonation", "NatureOfDonationInt"),
        "Reporting Period": ("ReportingPeriodName", None),
        "Party Affiliation": ("PartyName", None),
        "Regulated Entity Group": ("Party_Group", None),
    }

    prev_selected_group = st.session_state.get("selected_group_entity", None)

    selected_group_entity = st.selectbox(
        "Select Group Entity",
        options=list(group_entity_options.keys()),
        format_func=lambda x: group_entity_options[x][0],
        key="selected_group_entity"
    )

    # Reset section dropdown when group entity changes
    if prev_selected_group is not None and prev_selected_group != selected_group_entity:
        st.session_state["selected_entity_name"] = "All"

    # Get corresponding column names
    group_entity_col, group_entity_id_col = group_entity_options[selected_group_entity]

    # Apply initial filtering
    date_filter = (cleaned_df["ReceivedDate"] >= start_date) & (cleaned_df["ReceivedDate"] <= end_date)
    filtered_df = cleaned_df[date_filter]

    # Create mapping for dropdown based on filtered data
    entity_mapping = dict(zip(filtered_df[group_entity_col],
                              filtered_df[group_entity_id_col])
                          ) if group_entity_id_col else None

    available_entities = sorted(filtered_df[group_entity_col].unique().tolist())

    selected_entity_name = st.selectbox(
        f"Filter by {group_entity_col}",
        ["All"] + available_entities,
        key="selected_entity_name"
    )

    selected_entity_id = entity_mapping.get(selected_entity_name, None) if entity_mapping else None

    # Apply filters
    current_target = st.session_state["filter_def"].get(filter_key)
    
    entity_filter = (
        {group_entity_id_col: selected_entity_id} if selected_entity_id is not None
        else {group_entity_col: selected_entity_name} if selected_entity_name != "All"
        else {}
    )

    cleaned_d_df = filtered_df
    cleaned_c_df = apply_filters(cleaned_df, current_target) if current_target else cleaned_df
    cleaned_r_df = apply_filters(cleaned_df, entity_filter) if entity_filter else cleaned_df
    cleaned_r_d_df = cleaned_r_df[date_filter] if date_filter.any() else cleaned_r_df
    cleaned_c_d_df = apply_filters(cleaned_d_df, current_target)
    cleaned_c_r_df = apply_filters(cleaned_r_df, current_target)
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


@log_function_call("StreamlitApp")
def topline_summary_block(target_label,
                          min_date_df,
                          max_date_df,
                          tstats,
                          perc_cash_donations_d):
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
