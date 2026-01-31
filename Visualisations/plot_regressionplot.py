import streamlit as st
import plotly.express as px
from components.ColorMaps import political_colors
from utils.logger import logger
from utils.logger import log_function_call  # Import decorator


def plot_regressionplot(
    graph_df,
    XValues="DonationEvents",
    YValues="DonationsValue",
    size_column=None,
    color_column=None,  # New: Allows color differentiation (e.g., by category)
    XLabel="Number of Donations",
    YLabel="Value of Donations (Â£)",
    Title="Number of Donations vs. Value of Donations by Regulated Entity",
    size_label="Regulated Entities",
    size_scale=1,  # Adjusted default for better scaling
    dot_size=50,
    x_scale="log",  # linear or log
    y_scale="log",  # linear or log
    use_custom_colors=False,
    legend_title=None,
    show_trendline=True,  # New: Option to enable regression trendline
    width='stretch',
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

    color_mapping = political_colors

    # Validate Data
    if graph_df is None or XValues not in graph_df or YValues not in graph_df:
        st.error("Data is missing or incorrect column names provided.")
        return

    # Assign size dynamically
    size_arg = size_column if size_column in graph_df else None

    # Determine color mapping
    if use_custom_colors and color_column:
        color_discrete_map = {
            cat: color_mapping.get(cat, "#636efa")
            for cat in graph_df[color_column].unique()
        }
    else:
        color_discrete_map = None

    # Create Scatter Plot
    fig = px.scatter(
        graph_df,
        x=XValues,
        y=YValues,
        size=size_arg,
        color=color_column if use_custom_colors else None,
        labels={XValues: XLabel, YValues: YLabel, size_column: size_label},
        title=Title,
        log_x=(x_scale == "log"),
        log_y=(y_scale == "log"),
        size_max=dot_size,
        color_discrete_map=color_discrete_map,
    )

    # Optional Trendline
    if show_trendline:
        trend_fig = px.scatter(
            graph_df,
            x=XValues,
            y=YValues,
            trendline="ols",
            log_x=(x_scale == "log"),
            log_y=(y_scale == "log"),
        )
        trend_trace = trend_fig.data[1]
        fig.add_trace(trend_trace)

    # Improve Layout & Hover Info
    fig.update_layout(
        xaxis_title=XLabel,
        yaxis_title=YLabel,
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
    st.plotly_chart(fig, use_container_width=True)
