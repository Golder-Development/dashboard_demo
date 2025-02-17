import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
# import seaborn as sns
# import calculations as ppcalc
import math
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.subplots as sp

def plot_donations_by_year(
    Data,  
    XValues='YearReceived',
    YValue='Value',
    GGroup='RegEntity_Group',
    XLabel='Year',
    YLabel='Total Value (£)',
    Title='Donations by Year and Entity Type',
    CalcType='sum',
    ChartType='Bar',  # New: Allows user to select Bar or Line chart
    use_container_width=True,
    widget_key="graph1"  # New: Allows multiple graphs on the same page
):
    """
    Interactive Plotly stacked bar or line chart of donations by year and entity type.

    Features:
    - Dynamic filtering (Year & Entity Type)
    - Toggle chart type (Bar vs. Line)
    - Custom color palette
    - Downloadable CSV
    - Unique widget keys for multiple charts

    Parameters:
        Data (pd.DataFrame): The dataset with filtered donations.
        XValues (str): X-axis column.
        YValue (str): Y-axis column.
        GGroup (str): Grouping column.
        XLabel (str): X-axis label.
        YLabel (str): Y-axis label.
        Title (str): Chart title.
        CalcType (str): Aggregation type ('sum', 'avg', 'count', etc.).
        ChartType (str): 'Bar' or 'Line' (User-selected chart type).
        use_container_width (bool): Adjusts plot width in Streamlit.
        widget_key (str): Unique key for widgets (supports multiple graphs on one page).

    Returns:
        None (Displays the chart in Streamlit)
    """

    if Data is None or Data.empty:
        st.warning("No data available to plot.")
        return

    # Define aggregation methods
    aggregation_methods = {
        'sum': 'sum',
        'avg': 'mean',
        'count': 'count',
        'median': 'median',
        'max': 'max',
        'min': 'min',
        'std': 'std',
        'var': 'var',
        'sem': 'sem',
        'skew': 'skew',
        'kurt': 'kurt'
    }
    
    # Validate CalcType
    if CalcType not in aggregation_methods:
        CalcType = 'sum'

    # Group and aggregate data
    grouped_data = Data.groupby([XValues, GGroup])[YValue].agg(aggregation_methods[CalcType]).reset_index()

    # --- **Interactivity: Filtering Widgets** ---
    with st.expander("🔍 Filter Data", expanded=True):
        # Select Year Range with unique key
        year_options = sorted(grouped_data[XValues].unique())
        selected_years = st.slider(
            "Select Year Range", 
            min(year_options), max(year_options), 
            (min(year_options), max(year_options)), 
            key=f"year_slider_{widget_key}"  # Unique key
        )

        # Select Entity Types with unique key
        entity_options = grouped_data[GGroup].unique()
        selected_entities = st.multiselect(
            "Select Entity Types", entity_options, default=entity_options, 
            key=f"entity_multiselect_{widget_key}"  # Unique key
        )

        # Toggle Chart Type with unique key
        ChartType = st.radio(
            "Select Chart Type", ["Bar", "Line"], 
            index=0, key=f"chart_type_{widget_key}"  # Unique key
        )

    # Apply Filters
    filtered_data = grouped_data[
        (grouped_data[XValues].between(*selected_years)) &
        (grouped_data[GGroup].isin(selected_entities))
    ]

    # --- **Custom Color Palette** ---
    color_palette = px.colors.qualitative.Set1  # Custom color scheme
    color_map = {entity: color_palette[i % len(color_palette)] for i, entity in enumerate(entity_options)}

    # --- **Create Chart Based on User Selection** ---
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
            color_discrete_map=color_map,  # Apply color mapping
        )
    else:
        fig = px.line(
            filtered_data,
            x=XValues,
            y=YValue,
            color=GGroup,
            labels={XValues: XLabel, YValue: YLabel},
            title=Title,
            markers=True,  # Show data points
            color_discrete_map=color_map,  # Apply color mapping
        )

    # Improve layout
    fig.update_layout(
        xaxis_title=XLabel,
        yaxis_title=YLabel,
        legend_title=GGroup,
        hovermode="x unified",
    )

    # Format tooltips for better readability (e.g., currency format)
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{y:,.0f} GBP<br>%{legendgroup}",
    )

    # Display the chart
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
        trend_trace = trend_fig.data[1]  # Extract trendline from the second trace
        fig.add_trace(trend_trace)

    # Improve Layout & Hover Info
    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        legend_title=color_column if color_column else "Legend",
        hovermode="closest",
        title_x=0.5,  # Centered title
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=use_container_width)


import streamlit as st
import plotly.express as px

def plot_pie_chart(
        df,
        category_column,
        value_column=None,
        title="Pie Chart",
        category_label="Category",
        value_label="Value",
        color_label="Group",
        color_column=None,
        hole=0.4,
        key=None,
        use_container_width=True
    ):
    """
    Creates an interactive pie chart in Streamlit using Plotly Express.

    Features:
    - Aggregates data by count or sum.
    - Supports optional color grouping.
    - Uses an interactive donut-style chart by default.
    - Allows full label customization for better readability.
    - Supports multiple charts on a single Streamlit page using unique `key`.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        category_column (str): Column used for grouping (categorical variable).
        value_column (str, optional): Column for summing values. If None, counts instances.
        title (str): Title of the pie chart.
        category_label (str): Custom label for category column in tooltips.
        value_label (str): Custom label for the values.
        color_label (str): Custom label for the color column (if used).
        color_column (str, optional): Column for color differentiation.
        hole (float): Size of the hole in the middle (0 for full pie, >0 for donut).
        key (str, optional): Unique key for Streamlit widgets to allow multiple charts on the same page.
        use_container_width (bool): Whether to use full width in Streamlit.

    Returns:
        None (Displays the chart in Streamlit)
    """
    if df is None or category_column not in df:
        st.error("Data is missing or incorrect column name provided.")
        return

    # Sidebar Controls for Interactivity (Optional Selection)
    with st.expander(f"🔧 Customize {title}", expanded=False):
        category_column = st.selectbox("Select Category Column:", df.columns, index=df.columns.get_loc(category_column), key=f"{key}_category")
        value_column = st.selectbox("Select Value Column (Optional):", [None] + list(df.select_dtypes(include=['number']).columns), key=f"{key}_value")
        color_column = st.selectbox("Select Color Grouping Column (Optional):", [None] + list(df.columns), key=f"{key}_color")
        hole = st.slider("Donut Hole Size:", 0.0, 0.8, hole, step=0.1, key=f"{key}_hole")

    # Determine aggregation method
    if value_column:
        data = df.groupby(category_column, as_index=False)[value_column].sum()
    else:
        data = df[category_column].value_counts().reset_index()
        data.columns = [category_column, "count"]
        value_column = "count"

    # Custom labels for tooltips and axes
    labels = {
        category_column: category_label,
        value_column: value_label
    }
    
    if color_column:
        labels[color_column] = color_label

    # Create Pie Chart
    fig = px.pie(
        data,
        names=category_column,
        values=value_column,
        color=color_column if color_column else None,
        title=title,
        hole=hole,
        labels=labels
    )

    # Improve layout
    fig.update_layout(title_x=0.5, legend_title=category_label)

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=use_container_width)


def generate_boxplots(
        df,
        group_column=None,
        value_column="Value",
        plots_per_row=3,
        row_height=5,
        yscale='log',
        key=None,
        use_container_width=True
    ):
    """
    Generates interactive boxplots for each unique value in the specified column using Plotly.

    Features:
    - Allows users to dynamically select columns for grouping and values.
    - Supports multiple boxplots in a grid layout.
    - Works with multiple charts on a single Streamlit page via `key`.
    - Enables optional logarithmic scaling.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        group_column (str, optional): The column to group by (e.g., 'RegEntity_Group').
        value_column (str): The column to plot values for (e.g., 'Value').
        plots_per_row (int): Number of plots per row in the layout.
        row_height (int): Height of each row in the layout.
        yscale (str): Scale for the y-axis ('log' or 'linear').
        key (str, optional): Unique key for Streamlit widgets to support multiple instances.
        use_container_width (bool): Whether to use full width in Streamlit.

    Returns:
        None (Displays the plots in Streamlit)
    """

    if df is None or value_column not in df:
        st.error("Data is missing or incorrect column names provided.")
        return

    # Sidebar Controls for Interactivity
    with st.expander(f"🔧 Customize Boxplots {key or ''}", expanded=False):
        group_column = st.selectbox("Select Grouping Column (Optional):", [None] + list(df.columns), index=0, key=f"{key}_group")
        value_column = st.selectbox("Select Value Column:", df.select_dtypes(include=['number']).columns, index=list(df.columns).index(value_column), key=f"{key}_value")
        yscale = st.radio("Y-Axis Scale:", ["linear", "log"], index=(0 if yscale == "linear" else 1), key=f"{key}_yscale")

    # Determine unique groups and layout
    if group_column:
        unique_groups = df[group_column].dropna().unique()
        num_rows = math.ceil(len(unique_groups) / plots_per_row)
    else:
        unique_groups = ["All"]
        num_rows = 1

    fig = sp.make_subplots(
        rows=num_rows, 
        cols=plots_per_row, 
        subplot_titles=[f'Boxplot of {value_column} for {group}' for group in unique_groups]
    )

    for idx, group in enumerate(unique_groups):
        group_df = df if group_column is None else df[df[group_column] == group]
        row = idx // plots_per_row + 1
        col = idx % plots_per_row + 1

        box = px.box(
            group_df,
            y=value_column,
            points="all",
            log_y=(yscale == 'log'),
            title=f"{group}" if group_column else "All Data"
        )

        for trace in box.data:
            fig.add_trace(trace, row=row, col=col)

    # Update layout for better display
    fig.update_layout(
        height=row_height * num_rows * 100,
        showlegend=False,
        title_text=f"Boxplots of {value_column}",
        title_x=0.5
    )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=use_container_width)

# st.write("### Donation Value Distribution")

# generate_boxplots(
#     df=filtered_df,
#     group_column="RegEntity_Group",
#     value_column="DonationsValue",
#     plots_per_row=2,
#     row_height=6,
#     yscale='linear',
#     key="boxplot1"  # Unique key for multiple charts on one page
# )

# generate_boxplots(
#     df=filtered_df,
#     group_column="DonorCategory",
#     value_column="DonationsValue",
#     plots_per_row=3,
#     row_height=5,
#     yscale='log',
#     key="boxplot2"
# )