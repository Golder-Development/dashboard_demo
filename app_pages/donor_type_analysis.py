import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from components.modular_page_blocks import load_and_filter_data
from components.ColorMaps import political_colors
from utils.logger import log_function_call, logger


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
        agg_column = "Value"
        agg_func = "sum"
    else:
        agg_column = "Value"  # We'll count rows instead
        agg_func = "count"

    # Group by Party_Group and DonorStatus
    if agg_func == "count":
        grouped_data = (
            working_df.groupby(
                ['Party_Group', 'DonorStatus'],
                observed=True
            ).size().reset_index(name='count')
        )
        grouped_data = grouped_data.rename(columns={'count': 'Value'})
    else:
        grouped_data = (
            working_df.groupby(
                ['Party_Group', 'DonorStatus'],
                observed=True
            ).agg({agg_column: agg_func}).reset_index()
        )

    if grouped_data.empty:
        st.warning("No data available for selected criteria")
        return

    # Convert to percentage if requested
    if view_type == "Percentage":
        # Calculate percentage within each Party_Group
        grouped_data['Value'] = (
            grouped_data.groupby('Party_Group')['Value'].transform(
                lambda x: (x / x.sum() * 100) if x.sum() > 0 else 0
            )
        )

    # Pivot for stacked bar chart
    pivot_data = grouped_data.pivot_table(
        index='Party_Group',
        columns='DonorStatus',
        values='Value',
        aggfunc='sum',
        fill_value=0
    )

    # Sort by total value (descending)
    pivot_data['total'] = pivot_data.sum(axis=1)
    pivot_data = pivot_data.sort_values('total', ascending=False)
    pivot_data = pivot_data.drop('total', axis=1)

    # Create stacked bar chart
    fig = go.Figure()

    # Get unique donor types and assign colors
    donor_types = pivot_data.columns.tolist()
    colors = [
        'rgb(228, 26, 28)',    # Red
        'rgb(55, 126, 184)',   # Blue
        'rgb(77, 175, 74)',    # Green
        'rgb(255, 127, 0)',    # Orange
        'rgb(152, 78, 163)',   # Purple
        'rgb(166, 86, 40)',    # Brown
        'rgb(247, 129, 191)',  # Pink
        'rgb(153, 153, 153)',  # Grey
        'rgb(255, 255, 51)',   # Yellow
        'rgb(166, 206, 227)',  # Light Blue
        'rgb(178, 223, 138)',  # Light Green
        'rgb(251, 154, 153)',  # Light Red
        'rgb(227, 26, 28)',    # Dark Red
    ]

    # Ensure we have enough colors for all donor types
    while len(colors) < len(donor_types):
        colors.extend(colors)
    colors = colors[:len(donor_types)]

    # Add traces for each donor type
    for i, donor_type in enumerate(donor_types):
        values = pivot_data[donor_type].values.tolist()

        # Format hover text based on view type
        if view_type == "Percentage":
            hover_text = [
                f"<b>{party_group}</b><br>"
                f"Donor Type: {donor_type}<br>"
                f"Percentage: {val:.1f}%"
                for party_group, val in zip(
                    pivot_data.index, values
                )
            ]
        else:
            if metric_type == "Value of Donations":
                hover_text = [
                    f"<b>{party_group}</b><br>"
                    f"Donor Type: {donor_type}<br>"
                    f"Value: £{val:,.0f}"
                    for party_group, val in zip(
                        pivot_data.index, values
                    )
                ]
            else:
                hover_text = [
                    f"<b>{party_group}</b><br>"
                    f"Donor Type: {donor_type}<br>"
                    f"Count: {val:,.0f}"
                    for party_group, val in zip(
                        pivot_data.index, values
                    )
                ]

        fig.add_trace(go.Bar(
            x=pivot_data.index,
            y=values,
            name=donor_type,
            marker=dict(color=colors[i]),
            hovertext=hover_text,
            hoverinfo='text',
        ))

    # Update layout
    y_axis_title = (
        "Percentage (%)"
        if view_type == "Percentage"
        else (
            "Value (£)" if metric_type == "Value of Donations"
            else "Count"
        )
    )

    fig.update_layout(
        title=dict(
            text=(
                f"Donations by Party Group and Donor Type<br>"
                f"<sub>{view_type} - {metric_type}</sub>"
            ),
            font=dict(size=16),
            x=0.5,
            xanchor='center'
        ),
        barmode='stack',
        xaxis_title='Party Group',
        yaxis_title=y_axis_title,
        hovermode='x unified',
        height=600,
        legend=dict(
            title='Donor Type',
            orientation='v',
            yanchor='top',
            y=0.99,
            xanchor='left',
            x=1.01
        ),
        plot_bgcolor='rgba(240,240,240,0.5)',
        xaxis=dict(
            showgrid=False,
            showline=True,
            linewidth=1,
            linecolor='gray'
        ),
        yaxis=dict(
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # Display summary statistics
    st.write("---")
    st.subheader("Summary Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Donor Types",
            len(donor_types)
        )

    with col2:
        st.metric(
            "Party Groups",
            len(pivot_data.index)
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

    # Reshape data for display
    display_df = grouped_data.copy()
    display_df = display_df.sort_values(
        ['Party_Group', 'Value'],
        ascending=[True, False]
    )

    if metric_type == "Value of Donations":
        display_df['Value'] = display_df['Value'].apply(
            lambda x: f"£{x:,.0f}"
        )
    else:
        display_df['Value'] = display_df['Value'].apply(
            lambda x: f"{x:,.0f}"
        )

    if view_type == "Percentage":
        # Recalculate for display as percentage
        grouped_data_pct = grouped_data.copy()
        grouped_data_pct['Value'] = (
            grouped_data_pct.groupby('Party_Group')['Value'].transform(
                lambda x: (x / x.sum() * 100) if x.sum() > 0 else 0
            )
        )
        grouped_data_pct = grouped_data_pct.sort_values(
            ['Party_Group', 'Value'],
            ascending=[True, False]
        )
        grouped_data_pct['Value'] = grouped_data_pct['Value'].apply(
            lambda x: f"{x:.1f}%"
        )
        st.dataframe(
            grouped_data_pct,
            use_container_width=True
        )
    else:
        st.dataframe(
            display_df,
            use_container_width=True
        )
