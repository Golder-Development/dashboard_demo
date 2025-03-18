import streamlit as st
import plotly.express as px
from components.ColorMaps import political_colors
from utils.logger import log_function_call  # Import decorator


@log_function_call("StreamlitApp")
def plot_bar_line_by_year(
    graph_df=st.session_state.get("data_clean"),
    XValues="YearReceived",
    YValues="Value",
    GroupData="RegEntity_Group",
    XLabel="Year",
    YLabel="Total Value",
    Title="Donations by Year and Entity Type",
    LegendTitle="Regulated Entity Group",
    # sum, avg, count, median, max, min, std, var, sem, skew, kurt
    CalcType="sum",
    ChartType="Bar",  # Bar or Line
    x_scale="linear",
    y_scale="linear",
    use_custom_colors=False,
    use_container_width=True,
    percentbars=False,  # Show as percentage of total
    orientation="v",    # 'v' for vertical, 'h' for horizontal bars
    widget_key="graph1",
    show_filter_box=False,
    show_data_values=True,  # Show data values on bars
    barmode="stack",  # Bar chart only - stack or group
    show_legend=True,  # Show legend
    color_map=None,  # Custom color mapping
        ):

    if graph_df is None or graph_df.empty:
        st.warning("No data available to plot.")
        return

    aggregation_methods = {
        "sum": "sum",
        "avg": "mean",
        "count": "count",
        "median": "median",
        "max": "max",
        "min": "min",
        "std": "std",
        "var": "var",
        "sem": "sem",
        "skew": "skew",
        "kurt": "kurt",
    }

    if CalcType not in aggregation_methods:
        CalcType = "sum"

    grouped_data = (
        graph_df.groupby([XValues, GroupData], observed=True)[YValues]
        .agg(aggregation_methods[CalcType])
        .reset_index()
    )

    if show_filter_box:
        with st.expander("Filter Data", expanded=True):
            year_options = sorted(grouped_data[XValues].unique())
            selected_years = st.slider(
                "Select Year Range",
                min(year_options),
                max(year_options),
                (min(year_options), max(year_options)),
                key=f"year_slider_{widget_key}",
            )

            entity_options = grouped_data[GroupData].unique()
            selected_entities = st.multiselect(
                "Select Entity Types",
                entity_options,
                default=entity_options,
                key=f"entity_multiselect_{widget_key}",
            )

            ChartType = st.radio(
                "Select Chart Type",
                ["Bar", "Line"],
                index=0 if ChartType == "Bar" else 1,
                key=f"chart_type_{widget_key}",
            )

            show_as_percentage = st.checkbox(
                "Show as 100% stacked (percentage of total)",
                value=percentbars,
                key=f"percent_checkbox_{widget_key}",
            )
    else:
        year_options = []
        year_options = sorted(grouped_data[XValues].unique())
        selected_years = (min(year_options), max(year_options))
        entity_options = grouped_data[GroupData].unique()
        selected_entities = entity_options
        show_as_percentage = percentbars

    # Filter data based on selections
    filtered_data = grouped_data[
        (grouped_data[XValues].between(*selected_years))
        & (grouped_data[GroupData].isin(selected_entities))
    ]

    if show_as_percentage and ChartType == "Bar":
        # Normalize each year's values to sum to 100%
        filtered_data[YValues] = (
            filtered_data.groupby(XValues)[YValues].transform(
                lambda x: (x / x.sum()) * 100
            ))
        YLabel = "Percentage of Total (%)"

    # Define colors
    color_mapping = political_colors
    if use_custom_colors:
        color_map = {
            entity: color_mapping.get(entity, "#636efa") for entity in entity_options
        }
    else:
        color_map = None

    # Plot Bar or Line Chart
    if ChartType == "Bar":
        fig = px.bar(
            filtered_data,
            x=XValues,
            y=YValues,
            color=GroupData,
            labels={XValues: XLabel, YValues: YLabel},
            title=Title,
            barmode="stack",
            text_auto=show_data_values,  # Show data values on bars
            color_discrete_map=color_map,
        )
    else:
        fig = px.line(
            filtered_data,
            x=XValues,
            y=YValues,
            color=GroupData,
            labels={XValues: XLabel, YValues: YLabel},
            title=Title,
            markers=True,
            color_discrete_map=color_map,
        )

    # Update layout
    fig.update_layout(
        xaxis_title=XLabel,
        yaxis_title=YLabel,
        xaxis={"type": x_scale},
        yaxis={"type": y_scale if not show_as_percentage else "linear"},
        legend_title=LegendTitle,
        # Display hover info for all data points at a given x value
        hovermode="x unified",
        showlegend=True,  # Show legend
        legend=dict(orientation="h", yanchor="top", y=-0.1,
                    xanchor="center", x=0.5),
        title=dict(xanchor="center", yanchor="top", x=0.5),
    )

    # fig.update_traces(
    #     hovertemplate=(
    #         "<b>%{x}</b><br>%{y:.2f}%<br>%{legendgroup}"
    #         if show_as_percentage
    #         else "<b>%{x}</b><br>%{y:,.0f}<br>%{legendgroup}"
    #     )
    # )

    st.plotly_chart(fig, use_container_width=use_container_width)
