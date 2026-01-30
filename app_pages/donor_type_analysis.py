import streamlit as st
from components.modular_page_blocks import load_and_filter_data
from Visualisations.plot_stacked_bar_chart import plot_stacked_bar_chart
from utils.logger import log_function_call
from data.data_file_defs import normalize_string_columns_for_streamlit


@log_function_call
def mod_donor_type():
    """
    Page showing stacked chart of donations by party_group and donor_type
    with filtering options for:
    - Actual vs Percentage view
    - Value of donations vs Count of donations
    - Parliamentary sitting (multiselect)
    """
    st.title("Donations by Party Group and Donor Type")

    # Load and filter data
    cleaned_df, filtered_df = load_and_filter_data(
        filter_key=None,
        pagereflabel="donor_type_analysis"
    )

    if cleaned_df is None or filtered_df is None:
        st.error("Failed to load data")
        return

    # Create columns for filters
    col1, col2, col3 = st.columns(3)

    with col1:
        view_type = st.selectbox(
            "View Type",
            options=["Actual", "Percentage"],
            key="view_type_donor_type",
            help="Show actual values or percentages"
        )

    with col2:
        metric_type = st.selectbox(
            "Metric",
            options=["Value of Donations", "Count of Donations"],
            key="metric_type_donor_type",
            help="Show total donation value or count of donations"
        )

    with col3:
        # Get unique parliamentary sittings and sort them
        available_sittings = sorted(
            filtered_df['parliamentary_sitting'].unique()
        )
        selected_sittings = st.multiselect(
            "Parliamentary Sitting",
            options=available_sittings,
            default=available_sittings,
            key="sitting_select_donor_type",
            help="Select one or more parliamentary periods"
        )

    # Filter data by selected parliamentary sittings
    if selected_sittings:
        working_df = filtered_df[
            filtered_df['parliamentary_sitting'].isin(selected_sittings)
        ].copy()
    else:
        st.warning("Please select at least one parliamentary sitting")
        return

    # Prepare data for stacked chart
    if metric_type == "Value of Donations":
        agg_func = "sum"
    else:
        agg_func = "count"

    # Create aggregated dataset for chart
    if agg_func == "count":
        chart_data = (
            working_df.groupby(
                ['Party_Group', 'DonorStatus'],
                observed=True
            ).size().reset_index(name='Value')
        )
    else:
        chart_data = (
            working_df.groupby(
                ['Party_Group', 'DonorStatus'],
                observed=True
            ).agg({'Value': 'sum'}).reset_index()
        )

    if chart_data.empty:
        st.warning("No data available for selected criteria")
        return

    # Determine chart title and metric display label
    subtitle = f"{view_type} - {metric_type}"
    metric_display = (
        "Value of Donations"
        if metric_type == "Value of Donations"
        else "Count"
    )

    # Use standardized stacked bar chart visualization
    fig = plot_stacked_bar_chart(
        data=working_df,
        x_column='Party_Group',
        group_column='DonorStatus',
        values_column='Value' if agg_func == "sum" else 'DonorStatus',
        title=(
            "Donations by Party Group and Donor Type"
            f"<br><sub>{subtitle}</sub>"
        ),
        x_label='Party Group',
        y_label='Donor Type',
        agg_func=agg_func,
        view_type=view_type,
        metric_display=metric_display,
        height=600,
        use_custom_colors=True,
        sort_by_total=True,
        widget_key="donor_type_chart",
    )

    if fig is None:
        st.error("Failed to generate chart")
        return

    st.plotly_chart(fig, use_container_width=True)

    # Display summary statistics
    st.write("---")
    st.subheader("Summary Statistics")

    col1, col2, col3 = st.columns(3)

    # Get unique values for summary stats
    unique_donor_types = working_df['DonorStatus'].nunique()
    unique_party_groups = working_df['Party_Group'].nunique()

    with col1:
        st.metric(
            "Total Donor Types",
            unique_donor_types
        )

    with col2:
        st.metric(
            "Party Groups",
            unique_party_groups
        )

    with col3:
        if metric_type == "Value of Donations":
            total_value = working_df['Value'].sum()
            st.metric("Total Value", f"£{total_value:,.0f}")
        else:
            total_count = len(working_df)
            st.metric("Total Donations", f"{total_count:,}")

    # Display detailed table
    st.write("---")
    st.subheader("Detailed Breakdown")

    # Reshape data for display (recreate grouped_data for summary table)
    if agg_func == "count":
        grouped_data = (
            working_df.groupby(
                ['Party_Group', 'DonorStatus'],
                observed=True
            ).size().reset_index(name='Value')
        )
    else:
        grouped_data = (
            working_df.groupby(
                ['Party_Group', 'DonorStatus'],
                observed=True
            ).agg({'Value': 'sum'}).reset_index()
        )

    # Convert to percentage if requested
    if view_type == "Percentage":
        grouped_data['Value'] = (
            grouped_data.groupby('Party_Group')['Value'].transform(
                lambda x: (x / x.sum() * 100) if x.sum() > 0 else 0
            )
        )
        grouped_data = grouped_data.sort_values(
            ['Party_Group', 'Value'],
            ascending=[True, False]
        )
        grouped_data['Value'] = grouped_data['Value'].apply(
            lambda x: f"{x:.1f}%"
        )
    else:
        grouped_data = grouped_data.sort_values(
            ['Party_Group', 'Value'],
            ascending=[True, False]
        )
        if metric_type == "Value of Donations":
            grouped_data['Value'] = grouped_data['Value'].apply(
                lambda x: f"£{x:,.0f}"
            )
        else:
            grouped_data['Value'] = grouped_data['Value'].apply(
                lambda x: f"{x:,.0f}"
            )

    grouped_data = normalize_string_columns_for_streamlit(grouped_data)
    st.dataframe(
        grouped_data,
        use_container_width=True
    )
