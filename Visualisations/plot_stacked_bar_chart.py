"""
Standardized stacked bar chart visualization for categorical data grouping.
Used for multi-level categorical analysis (e.g., Party Group by Donor Status).
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from components.ColorMaps import political_colors


def plot_stacked_bar_chart(
    data,
    x_column,
    group_column,
    values_column,
    title="Stacked Bar Chart",
    x_label="Category",
    y_label="Value",
    agg_func="sum",
    view_type="Count",  # 'Count', 'Value', 'Percentage'
    metric_display="Count",  # For hover text customization
    width='stretch',
    height=600,
    show_legend=True,
    use_custom_colors=True,
    color_map=None,
    orientation="v",  # 'v' for vertical, 'h' for horizontal
    sort_by_total=True,
    widget_key="stacked_bar",
):
    """
    Create a standardized stacked bar chart for categorical multi-level data.
    
    Parameters:
    -----------
    data : pd.DataFrame
        Input data for visualization
    x_column : str
        Column name for X-axis (main categories)
    group_column : str
        Column name for grouping (stacked values)
    values_column : str
        Column name for aggregation values
    title : str
        Chart title
    x_label : str
        X-axis label
    y_label : str
        Y-axis label
    agg_func : str
        Aggregation function ('sum', 'count', 'mean', 'median', 'max', 'min')
    view_type : str
        Display mode ('Count', 'Value', 'Percentage')
    metric_display : str
        Label for hover text (e.g., 'Count', 'Value of Donations')
    width : str
        Chart width ('stretch' or pixel value)
    height : int
        Chart height in pixels
    show_legend : bool
        Whether to display legend
    use_custom_colors : bool
        Whether to use political_colors mapping
    color_map : dict
        Custom color mapping {category: color}
    orientation : str
        'v' for vertical bars, 'h' for horizontal bars
    sort_by_total : bool
        Sort X categories by total value (descending)
    widget_key : str
        Unique identifier for widget state
    
    Returns:
    --------
    plotly.graph_objects.Figure or None
        Plotly figure object or None if data is invalid
    """
    
    if data is None or data.empty:
        st.warning("No data available to plot.")
        return None

    required_columns = [x_column, group_column, values_column]
    missing_columns = [
        col for col in required_columns if col not in data.columns
    ]
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
        return None

    working_df = data.copy()
    
    # Ensure numeric values for aggregation
    working_df[values_column] = pd.to_numeric(
        working_df[values_column], errors="coerce"
    )
    working_df = working_df.dropna(
        subset=[x_column, group_column, values_column]
    )
    
    if working_df.empty:
        st.warning("No valid data available after cleaning.")
        return None

    # Aggregation
    if agg_func == "count":
        grouped_data = (
            working_df.groupby([x_column, group_column], observed=True)
            .size()
            .reset_index(name='Value')
        )
    else:
        agg_methods = {
            "sum": "sum",
            "mean": "mean",
            "median": "median",
            "max": "max",
            "min": "min",
            "count": "count",
        }
        agg_method = agg_methods.get(agg_func, "sum")
        grouped_data = (
            working_df.groupby([x_column, group_column], observed=True)
            .agg({values_column: agg_method})
            .reset_index()
            .rename(columns={values_column: 'Value'})
        )

    # Convert to percentage if requested
    if view_type == "Percentage":
        grouped_data['Value'] = (
            grouped_data.groupby(x_column)['Value'].transform(
                lambda x: (x / x.sum() * 100) if x.sum() > 0 else 0
            )
        )

    # Pivot for stacked bar chart
    pivot_data = grouped_data.pivot_table(
        index=x_column,
        columns=group_column,
        values='Value',
        aggfunc='sum',
        fill_value=0
    )

    # Sort by total value if requested
    if sort_by_total:
        pivot_data['total'] = pivot_data.sum(axis=1)
        pivot_data = pivot_data.sort_values('total', ascending=False)
        pivot_data = pivot_data.drop('total', axis=1)

    # Define colors
    group_categories = pivot_data.columns.tolist()
    
    if color_map is None:
        if use_custom_colors:
            color_map = {
                cat: political_colors.get(cat, None)
                for cat in group_categories
            }
            # Fill missing colors with defaults
            colors_list = [
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
            for i, cat in enumerate(group_categories):
                if color_map[cat] is None:
                    color_map[cat] = colors_list[i % len(colors_list)]
        else:
            # Use default colors
            colors_list = [
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
            color_map = {
                cat: colors_list[i % len(colors_list)]
                for i, cat in enumerate(group_categories)
            }

    # Create figure
    fig = go.Figure()

    # Add traces for each group
    for group_category in group_categories:
        values = pivot_data[group_category].values.tolist()

        # Format hover text based on view type
        if view_type == "Percentage":
            hovertext = [
                f"<b>{x_val}</b><br>"
                f"{group_column}: {group_category}<br>"
                f"Percentage: {val:.1f}%"
                for x_val, val in zip(pivot_data.index, values)
            ]
        else:
            if metric_display == "Value of Donations":
                hovertext = [
                    f"<b>{x_val}</b><br>"
                    f"{group_column}: {group_category}<br>"
                    f"Value: £{val:,.0f}"
                    for x_val, val in zip(pivot_data.index, values)
                ]
            else:
                hovertext = [
                    f"<b>{x_val}</b><br>"
                    f"{group_column}: {group_category}<br>"
                    f"Count: {val:,.0f}"
                    for x_val, val in zip(pivot_data.index, values)
                ]

        if orientation == "h":
            fig.add_trace(go.Bar(
                y=pivot_data.index,
                x=values,
                name=str(group_category),
                marker=dict(color=color_map.get(group_category, '#636efa')),
                hovertext=hovertext,
                hoverinfo='text',
                orientation='h',
            ))
        else:
            fig.add_trace(go.Bar(
                x=pivot_data.index,
                y=values,
                name=str(group_category),
                marker=dict(color=color_map.get(group_category, '#636efa')),
                hovertext=hovertext,
                hoverinfo='text',
            ))

    # Update layout
    y_axis_title = y_label
    if view_type == "Percentage":
        y_axis_title = "Percentage (%)"
    elif metric_display == "Value of Donations":
        y_axis_title = "Value (£)"
    elif metric_display == "Count":
        y_axis_title = "Count"

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16),
            x=0.5,
            xanchor='center'
        ),
        barmode='stack',
        xaxis_title=x_label if orientation == "v" else y_axis_title,
        yaxis_title=y_axis_title if orientation == "v" else x_label,
        hovermode='x unified' if orientation == "v" else 'y unified',
        height=height,
        showlegend=show_legend,
        legend=dict(
            title=group_column,
            orientation='v',
            yanchor='top',
            y=0.99,
            xanchor='left',
            x=1.01,
        ) if show_legend else dict(visible=False),
        margin=dict(l=60, r=200 if show_legend else 60, t=80, b=60),
    )

    return fig
