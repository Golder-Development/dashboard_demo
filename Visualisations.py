import streamlit as st
# import seaborn as sns
# import calculations as ppcalc
# import pandas as pd
import plotly.express as px
# import plotly.subplots as sp


def plot_bar_line_by_year(
                Data,
                XValues='YearReceived',
                YValue='Value',
                GGroup='RegEntity_Group',
                XLabel='Year',
                YLabel='Total Value (£)',
                Title='Donations by Year and Entity Type',
                LegendTitle='Regulated Entity Group',
                CalcType='sum',
                ChartType='Bar',
                x_scale='linear',
                y_scale='linear',
                use_custom_colors=False,
                use_container_width=True,
                widget_key="graph1"
                ):
    """
    Interactive Plotly stacked bar or line chart of donations by year
    and entity type.

    Parameters:
    - Data (pd.DataFrame): The input data frame containing the data to plot.
    - XValues (str): The column name for the x-axis values.
            Default is 'YearReceived'.
    - YValue (str): The column name for the y-axis values. Default is 'Value'.
    - GGroup (str): The column name for the grouping variable.
            Default is 'RegEntity_Group'.
    - XLabel (str): The label for the x-axis. Default is 'Year'.
    - YLabel (str): The label for the y-axis. Default is 'Total Value (£)'.
    - Title (str): The title of the chart. Default is 'Donations by Year and
            Entity Type'.
    - CalcType (str): The type of aggregation to apply ('sum', 'avg', 'count',
            etc.). Default is 'sum'.
    - ChartType (str): The type of chart to plot ('Bar' or 'Line').
            Default is 'Bar'.
    - x_scale (str): The scale type for the x-axis ('linear' or 'log').
            Default is 'linear'.
    - y_scale (str): The scale type for the y-axis ('linear' or 'log').
            Default is 'linear'.
    - use_custom_colors (bool): Whether to use custom colors for the entities.
            Default is False.
    - use_container_width (bool): Use the container width for the chart.
            Default is True.
    - widget_key (str): The key for the Streamlit widgets to avoid conflicts.
            Default is "graph1".
    Returns:
    - None: The function directly plots the chart using Streamlit.
    """
    if Data is None or Data.empty:
        st.warning("No data available to plot.")
        return

    aggregation_methods = {
        'sum': 'sum', 'avg': 'mean', 'count': 'count', 'median': 'median',
        'max': 'max', 'min': 'min', 'std': 'std', 'var': 'var', 'sem': 'sem',
        'skew': 'skew', 'kurt': 'kurt'
    }

    color_mapping = {
        "Conservative and Unionist Party": "#0087DC",
        "Labour Party": "#DC241F",
        "Liberal Democrats": "#FDBB30",
        "Green Party": "#78B943",
        "Scottish National Party (SNP)": "#FFFF00",
        "Plaid Cymru": "#3F8428",
        "Reform UK": "#12B6CF",
        "UK Independence Party (UKIP)": "#70147A",
        "Democratic Unionist Party (DUP)": "#D50000",
        "Sinn Féin": "#326760",
        "Ulster Unionist Party (UUP)": "#48A5EE",
        "Social Democratic and Labour Party (SDLP)": "#99D700",
        "Alliance Party of Northern Ireland": "#FFD700",
        "Other": "#7f7f7f",
        "Large Entity": "#9467bd",
        "Medium Entity": "#8c564b",
        "Small Entity": "#e377c2",
        "Very Small Entity": "#bcbd22",
        "Single Donation Entity": "#7f7f7f"
    }

    if CalcType not in aggregation_methods:
        CalcType = 'sum'

    grouped_data = (
        Data.groupby([XValues, GGroup])[YValue]
            .agg(aggregation_methods[CalcType])
            .reset_index()
    )
    with st.expander("🔍 Filter Data", expanded=True):
        year_options = sorted(grouped_data[XValues].unique())
        selected_years = st.slider(
            "Select Year Range",
            min(year_options),
            max(year_options),
            (min(year_options),
             max(year_options)),
            key=f"year_slider_{widget_key}")

        entity_options = grouped_data[GGroup].unique()
        selected_entities = st.multiselect(
            "Select Entity Types",
            entity_options,
            default=entity_options,
            key=f"entity_multiselect_{widget_key}"
        )

        ChartType = st.radio(
            "Select Chart Type",
            ["Bar", "Line"],
            index=0 if ChartType == "Bar" else 1,
            key=f"chart_type_{widget_key}")

    filtered_data = grouped_data[
        (grouped_data[XValues].between(*selected_years)) &
        (grouped_data[GGroup].isin(selected_entities))
    ]

    if use_custom_colors:
        color_map = {entity: color_mapping.get(entity, "#7f7f7f")
                     for entity in entity_options}
    else:
        color_palette = px.colors.qualitative.Set1
        color_map = {entity: color_palette[i % len(color_palette)] for i,
                     entity in enumerate(entity_options)}

    if ChartType == "Bar":
        fig = px.bar(
            filtered_data, x=XValues, y=YValue, color=GGroup,
            labels={XValues: XLabel, YValue: YLabel}, title=Title,
            barmode="stack", text_auto=True, color_discrete_map=color_map
        )
    else:
        fig = px.line(
            filtered_data, x=XValues, y=YValue, color=GGroup,
            labels={XValues: XLabel, YValue: YLabel}, title=Title,
            markers=True, color_discrete_map=color_map
        )

    fig.update_layout(
        xaxis_title=XLabel,
        yaxis_title=YLabel,
        xaxis={'type': x_scale},
        yaxis={'type': y_scale},
        legend_title=LegendTitle,
        hovermode="x unified",
        legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.1,
                xanchor="center",
                x=0.5
            ),
        title=dict(
            xanchor='center',
            yanchor='top',
            x=0.5
        ),
    )

    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{y:,.0f}GBP<br>%{legendgroup}"
    )

    st.plotly_chart(fig, use_container_width=use_container_width)


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
    x_scale='log',
    y_scale='log',
    use_custom_colors=False,
    legend_title=None,
    show_trendline=True,  # New: Option to enable regression trendline
    use_container_width=True
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

    # Validate Data
    if sum_df is None or x_column not in sum_df or y_column not in sum_df:
        st.error("Data is missing or incorrect column names provided.")
        return

    # Assign size dynamically
    size_arg = size_column if size_column in sum_df else None

    # Create Scatter Plot
    fig = px.scatter(
        sum_df,
        x=x_column,
        y=y_column,
        size=size_arg,
        color=color_column,  # New: Optional color differentiation
        labels={x_column: x_label, y_column: y_label, size_column: size_label},
        title=title,
        log_x=(x_scale == 'log'),
        log_y=(y_scale == 'log'),
        size_max=dot_size
    )

    # Optional Trendline
    if show_trendline:
        trend_fig = px.scatter(
            sum_df,
            x=x_column,
            y=y_column,
            trendline="ols",
            log_x=(x_scale == 'log'),
            log_y=(y_scale == 'log')
        )
        trend_trace = trend_fig.data[1]
        fig.add_trace(trend_trace)

    # Improve Layout & Hover Info
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        legend_title=(color_column if color_column 
                      else "Legend" 
                      if legend_title is None 
                      else legend_title),
        hovermode="closest",
        legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.1,
                xanchor="center",
                x=0.5
            ),
        title=dict(
            xanchor='center',
            yanchor='top',
            x=0.5
        )  # Centered title
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=use_container_width)


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
        use_container_width=True
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
    color_mapping = {
        # Official Tory blue
        "Conservative and Unionist Party": "#0087DC",
        # Official Labour red
        "Labour Party": "#DC241F",
        # Official Lib Dem yellow-orange
        "Liberal Democrats": "#FDBB30",
        # Official Green Party green
        "Green Party": "#78B943",
        # SNP uses bright yellow
        "Scottish National Party (SNP)": "#FFFF00",
        # Plaid Cymru green
        "Plaid Cymru": "#3F8428",
        # Reform UK blue-cyan
        "Reform UK": "#12B6CF",
        # UKIP purple
        "UK Independence Party (UKIP)": "#70147A",
        # DUP red
        "Democratic Unionist Party (DUP)": "#D50000",
        # Sinn Féin dark green
        "Sinn Féin": "#326760",
        # UUP light blue
        "Ulster Unionist Party (UUP)": "#48A5EE",
        # SDLP green-yellow
        "Social Democratic and Labour Party (SDLP)": "#99D700",
        # Alliance gold
        "Alliance Party of Northern Ireland": "#FFD700",
        # Neutral gray for unclassified entities
        "Other": "#7f7f7f",

        # Categories for entity sizes
        "Large Entity": "#9467bd",  # Purple
        "Medium Entity": "#8c564b",  # Brown
        "Small Entity": "#e377c2",  # Pink
        "Very Small Entity": "#bcbd22",  # Olive green
        "Single Donation Entity": "#7f7f7f"  # Gray
    }

    # Determine aggregation method
    if value_column:
        data = df.groupby(category_column, as_index=False)[value_column].sum()
    else:
        data = df[category_column].value_counts().reset_index()
        data.columns = [category_column, "count"]
        value_column = "count"

    # Custom labels for tooltips
    labels = {
        category_column: category_label,
        value_column: value_label
    }

    if color_column:
        labels[color_column] = color_label

    # Determine color mapping
    if use_custom_colors:
        color_discrete_map = {
            cat: color_mapping.get(cat, "#636efa")
            for cat in data[category_column]
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
        color_discrete_map=color_discrete_map
    )

    # Improve layout
    fig.update_layout(
        title=dict(
            xanchor='center',
            yanchor='top',
            x=0.5
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="center",
            x=0.5
        ),
        legend_title=(category_label if category_label
                else "Legend" 
                if legend_title is None 
                else legend_title)
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=use_container_width)


def plot_custom_bar_chart(
        df,
        x_column,
        y_column,
        group_column=None,
        agg_func='count',
        title="Custom Bar Chart",
        x_label=None,
        y_label=None,
        orientation='v',
        barmode='group',
        color_palette='Set1',
        key=None,
        x_scale='linear',
        y_scale='linear',
        legend_title=None,
        use_container_width=True
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
        use_container_width (bool): Whether to use full width in Streamlit.

    Returns:
        None (Displays the chart in Streamlit)
    """

    if df is None or x_column not in df or y_column not in df:
        st.error("Data is missing or incorrect column names provided.")
        return

    # Aggregate Data
    if agg_func == 'sum':
        df_agg = (
            df.groupby([x_column] + ([group_column] if group_column else []))
            .agg({y_column: 'sum'})
            .reset_index()
            )
    elif agg_func == 'avg':
        df_agg = (
            df.groupby([x_column] + ([group_column] if group_column else []))
            .agg({y_column: 'mean'})
            .reset_index()
        )
    elif agg_func == 'count':
        df_agg = (
            df.groupby([x_column] + ([group_column] if group_column else []))
            .agg({y_column: 'count'})
            .reset_index()
        )
    elif agg_func == 'max':
        df_agg = (
            df.groupby([x_column] + ([group_column] if group_column else []))
            .agg({y_column: 'max'})
            .reset_index()
        )
    elif agg_func == 'min':
        df_agg = (
            df.groupby([x_column] + ([group_column] if group_column else []))
            .agg({y_column: 'min'})
            .reset_index()
        )

    # Generate Bar Chart
    fig = px.bar(
        df_agg,
        x=x_column if orientation == "v" else y_column,
        y=y_column if orientation == "v" else x_column,
        color=group_column if group_column else None,
        barmode=barmode,
        title=title,
        labels={x_column: x_label or x_column, y_column: y_label or y_column},
        color_discrete_sequence=px.colors.qualitative.__dict__.get(
            color_palette, px.colors.qualitative.Set1),
        orientation=orientation
    )

    # Update layout with axis scale options
    fig.update_layout(
        xaxis={'type': x_scale},
        yaxis={'type': y_scale},
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="center",
            x=0.5
            ),
        legend_title=(legend_title if legend_title
                else group_column 
                if group_column
                else "legend"),
        title=dict(
            xanchor='center',
            yanchor='top',
            x=0.5
        )     
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=use_container_width)
