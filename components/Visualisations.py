import streamlit as st
import plotly.express as px
import components.ColorMaps as cm
from utils.logger import logger
from utils.logger import log_function_call  # Import decorator

@log_function_call
def plot_bar_line_by_year(
    Data,
    XValues="YearReceived",
    YValue="Value",
    GGroup="RegEntity_Group",
    XLabel="Year",
    YLabel="Total Value (£)",
    Title="Donations by Year and Entity Type",
    LegendTitle="Regulated Entity Group",
    CalcType="sum",
    ChartType="Bar",
    x_scale="linear",
    y_scale="linear",
    use_custom_colors=False,
    use_container_width=True,
    percentbars=False,
    widget_key="graph1",
    show_filter_box=False,
):

    if Data is None or Data.empty:
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
        Data.groupby([XValues, GGroup], observed=True)[YValue]
        .agg(aggregation_methods[CalcType])
        .reset_index()
    )

    if show_filter_box:
        with st.expander("🔍 Filter Data", expanded=True):
            year_options = sorted(grouped_data[XValues].unique())
            selected_years = st.slider(
                "Select Year Range",
                min(year_options),
                max(year_options),
                (min(year_options), max(year_options)),
                key=f"year_slider_{widget_key}",
            )

            entity_options = grouped_data[GGroup].unique()
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
        entity_options = grouped_data[GGroup].unique()
        selected_entities = entity_options
        show_as_percentage = percentbars

    # Filter data based on selections
    filtered_data = grouped_data[
        (grouped_data[XValues].between(*selected_years))
        & (grouped_data[GGroup].isin(selected_entities))
    ]

    if show_as_percentage and ChartType == "Bar":
        # Normalize each year's values to sum to 100%
        filtered_data[YValue] = filtered_data.groupby(XValues)[YValue].transform(
            lambda x: (x / x.sum()) * 100
        )
        YLabel = "Percentage of Total (%)"

    # Define colors
    color_mapping = cm.color_mapping
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
            y=YValue,
            color=GGroup,
            labels={XValues: XLabel, YValue: YLabel},
            title=Title,
            barmode="stack",
            text_auto=True,
            color_discrete_map=color_map,
        )
    else:
        fig = px.line(
            filtered_data,
            x=XValues,
            y=YValue,
            color=GGroup,
            labels={XValues: XLabel, YValue: YLabel},
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
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5),
        title=dict(xanchor="center", yanchor="top", x=0.5),
    )

    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>%{y:.2f}%<br>%{legendgroup}"
            if show_as_percentage
            else "<b>%{x}</b><br>%{y:,.0f}<br>%{legendgroup}"
        )
    )

    st.plotly_chart(fig, use_container_width=use_container_width)

@log_function_call
def plot_regressionplot(
    sum_df,
    x_column="DonationEvents",
    y_column="DonationsValue",
    size_column=None,
    color_column=None,  # New: Allows color differentiation (e.g., by category)
    x_label="Number of Donations",
    y_label="Value of Donations (£)",
    title="Number of Donations vs. Value of Donations by Regulated Entity",
    size_label="Regulated Entities",
    size_scale=1,  # Adjusted default for better scaling
    dot_size=50,
    x_scale="log",
    y_scale="log",
    use_custom_colors=False,
    legend_title=None,
    show_trendline=True,  # New: Option to enable regression trendline
    use_container_width=True,
):
    """
    Creates an interactive scatter plot with optional regression trendline.

    Features:
    - Fully utilizes Plotly Express for better performance.
    - Supports log scaling and dynamic dot sizes.
    - Adds optional color encoding and trendline.

    Parameters:
        sum_df (pd.DataFrame): DataFrame containing data for visualization.
        x_column (str): Column name for x-axis values.
        y_column (str): Column name for y-axis values.
        size_column (str, optional): Column name for dot sizes.
        color_column (str, optional): Column name for dot colors.
        x_label (str): Label for the x-axis.
        y_label (str): Label for the y-axis.
        title (str): Title of the chart.
        size_label (str): Label for the dot sizes.
        size_scale (float): Scale factor for dot sizes.
        dot_size (int): Default size of dots if size_column is None.
        x_scale (str): Scale for the x-axis ('linear' or 'log').
        y_scale (str): Scale for the y-axis ('linear' or 'log').
        show_trendline (bool): Whether to show a regression trendline.

    Returns:
        None (displays the chart in Streamlit)
    """

    color_mapping = cm.color_mapping

    # Validate Data
    if sum_df is None or x_column not in sum_df or y_column not in sum_df:
        st.error("Data is missing or incorrect column names provided.")
        return

    # Assign size dynamically
    size_arg = size_column if size_column in sum_df else None

    # Determine color mapping
    if use_custom_colors and color_column:
        color_discrete_map = {
            cat: color_mapping.get(cat, "#636efa")
            for cat in sum_df[color_column].unique()
        }
    else:
        color_discrete_map = None

    # Create Scatter Plot
    fig = px.scatter(
        sum_df,
        x=x_column,
        y=y_column,
        size=size_arg,
        color=color_column if use_custom_colors else None,
        labels={x_column: x_label, y_column: y_label, size_column: size_label},
        title=title,
        log_x=(x_scale == "log"),
        log_y=(y_scale == "log"),
        size_max=dot_size,
        color_discrete_map=color_discrete_map,
    )

    # Optional Trendline
    if show_trendline:
        trend_fig = px.scatter(
            sum_df,
            x=x_column,
            y=y_column,
            trendline="ols",
            log_x=(x_scale == "log"),
            log_y=(y_scale == "log"),
        )
        trend_trace = trend_fig.data[1]
        fig.add_trace(trend_trace)

    # Improve Layout & Hover Info
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        legend_title=(
            color_column
            if color_column
            else "Legend" if legend_title is None else legend_title
        ),
        hovermode="closest",
        legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5),
        title=dict(xanchor="center", yanchor="top", x=0.5),  # Centered title
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=use_container_width)

@log_function_call
def plot_pie_chart(
    df,
    category_column,
    value_column=None,
    title="Pie Chart",
    category_label="Category",
    value_label="Value",
    color_label="Group",
    color_column=None,
    use_custom_colors=False,  # Flag to enable color mapping
    hole=0.4,
    widget_key=None,
    legend_title=None,
    use_container_width=True,
):
    """
    Creates an interactive pie chart in Streamlit using Plotly Express.

    Features:
    - Aggregates data by count or sum.
    - Supports optional color grouping.
    - Allows color mapping based on a dictionary when enabled.
    - Uses an interactive donut-style chart by default.
    - Allows full label customization for better readability.
    - Supports multiple charts on a single Streamlit page using unique `key`.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        category_column (str): Column used for grouping (categorical variable).
        value_column (str, optional): Column for summing values.
            If None, counts instances.
        title (str): Title of the pie chart.
        category_label (str): Custom label for category column in tooltips.
        value_label (str): Custom label for the values.
        color_label (str): Custom label for the color column (if used).
        color_column (str, optional): Column for color differentiation.
        use_custom_colors (bool): Whether to apply custom colors from a
            dictionary.
        hole (float): Size of the hole in the middle (0 for full pie,
            >0 for donut).
        key (str, optional): Unique key for Streamlit widgets to allow
            multiple charts on the same page.
        use_container_width (bool): Whether to use full width in Streamlit.

    Returns:
        None (Displays the chart in Streamlit)
    """
    if df is None or category_column not in df:
        st.error("Data is missing or incorrect column name provided.")
        return

    # Define custom color mapping (Adjust colors as needed)
    color_mapping = cm.color_mapping

    # Determine aggregation method
    if value_column:
        data = df.groupby(category_column, observed=True, as_index=False)[
            value_column
        ].sum()
    else:
        data = df[category_column].value_counts().reset_index()
        data.columns = [category_column, "count"]
        value_column = "count"

    # Custom labels for tooltips
    labels = {category_column: category_label, value_column: value_label}

    if color_column:
        labels[color_column] = color_label

    # Determine color mapping
    if use_custom_colors:
        color_discrete_map = {
            cat: color_mapping.get(cat, "#636efa") for cat in data[category_column]
        }
    else:
        color_discrete_map = None

    # Create Pie Chart
    fig = px.pie(
        data,
        names=category_column,
        values=value_column,
        color=category_column if use_custom_colors else None,
        title=title,
        hole=hole,
        labels=labels,
        color_discrete_map=color_discrete_map,
    )

    # Improve layout
    fig.update_layout(
        title=dict(xanchor="center", yanchor="top", x=0.5),
        legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5),
        legend_title=(
            category_label
            if category_label
            else "Legend" if legend_title is None else legend_title
        ),
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=use_container_width)

@log_function_call
def plot_custom_bar_chart(
    df,
    x_column,
    y_column,
    group_column=None,
    agg_func="count",
    title="Custom Bar Chart",
    x_label=None,
    y_label=None,
    orientation="v",
    barmode="group",
    color_palette="Set1",
    widget_key=None,
    x_scale="linear",
    y_scale="linear",
    legend_title=None,
    use_custom_colors=False,  # Added option for custom colors
    use_container_width=True,
):
    """
    Generates an interactive bar chart using Plotly Express
    Parameters:
    df (pd.DataFrame): DataFrame containing the data.
    x_column (str): Column for x-axis (categorical variable).
    y_column (str): Column for y-axis (numerical variable).
    group_column (str, optional): Column for grouping bars.
    agg_func (str): Aggregation function ('sum', 'avg', 'count', etc.).
    title (str): Chart title.
    x_label (str, optional): X-axis label (defaults to column name).
    y_label (str, optional): Y-axis label (defaults to column name).
    orientation (str): 'v' for vertical, 'h' for horizontal bars.
    barmode (str): 'group' (side-by-side) or 'stack' (stacked bars).
    color_palette (str): Plotly color scale.
    key (str, optional): Unique key for Streamlit widgets.
    x_scale (str): Scale for the x-axis ('linear' or 'log').Type:
        enumerated , one of
        ( "-" | "linear" | "log" | "date" | "category" | "multicategory" )
    y_scale (str): Scale for the y-axis ('linear' or 'log').Type:
        enumerated , one of
        ( "-" | "linear" | "log" | "date" | "category" | "multicategory" )
    use_custom_colors (bool): Whether to apply custom colors from a
        dictionary.
    use_container_width (bool): Whether to use full width in Streamlit.

    Returns:
    None (Displays the chart in Streamlit)
    """

    color_mapping = cm.color_mapping

    if df is None or x_column not in df or y_column not in df:
        st.error("Data is missing or incorrect column names provided.")
        return

    # Aggregate Data
    if agg_func == "sum":
        df_agg = (
            df.groupby([x_column] + ([group_column] if group_column else []))
            .agg({y_column: "sum"})
            .reset_index()
        )
    elif agg_func == "avg":
        df_agg = (
            df.groupby([x_column] + ([group_column] if group_column else []))
            .agg({y_column: "mean"})
            .reset_index()
        )
    elif agg_func == "count":
        df_agg = (
            df.groupby([x_column] + ([group_column] if group_column else []))
            .agg({y_column: "count"})
            .reset_index()
        )
    elif agg_func == "max":
        df_agg = (
            df.groupby([x_column] + ([group_column] if group_column else []))
            .agg({y_column: "max"})
            .reset_index()
        )
    elif agg_func == "min":
        df_agg = (
            df.groupby([x_column] + ([group_column] if group_column else []))
            .agg({y_column: "min"})
            .reset_index()
        )

    # Determine color mapping
    if use_custom_colors and group_column:
        color_discrete_map = {
            cat: color_mapping.get(cat, "#636efa") for cat in df_agg[group_column]
        }
    else:
        color_discrete_map = None

    # Generate Bar Chart
    fig = px.bar(
        df_agg,
        x=x_column if orientation == "v" else y_column,
        y=y_column if orientation == "v" else x_column,
        color=group_column if group_column else None,
        barmode=barmode,
        title=title,
        labels={x_column: x_label or x_column, y_column: y_label or y_column},
        color_discrete_map=color_discrete_map,
        color_discrete_sequence=px.colors.qualitative.__dict__.get(
            color_palette, px.colors.qualitative.Set1
        ),
        orientation=orientation,
    )

    # Update layout with axis scale options
    fig.update_layout(
        xaxis={"type": x_scale},
        yaxis={"type": y_scale},
        legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5),
        legend_title=(
            legend_title if legend_title else group_column if group_column else "legend"
        ),
        title=dict(xanchor="center", yanchor="top", x=0.5),
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=use_container_width)
