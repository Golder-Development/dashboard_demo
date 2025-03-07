import streamlit as st
import plotly.express as px
from components.ColorMaps import political_colors
from utils.logger import logger
from utils.logger import log_function_call  # Import decorator


def plot_pie_chart(
    graph_df,  # df
    XValues,  # category_column
    YValues,  # value_column
    color_label=None,
    color_column=None,
    use_custom_colors=False,
    color_map=None,
    Title="Pie Chart",  # title
    YLabel="Value",  # category_label
    XLabel="Category",  # value_label
    hole=0.3,
    widget_key="default",
    legend_title=None,
    use_container_width=True,
    show_filter_box=False,
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
            graph_df (pd.DataFrame): The DataFrame containing the data.
            XValues - category_column (str): Column used for grouping (categorical variable).
            YValues - value_column (str, optional): Column for summing values.
                If None, counts instances.
            Title - title (str): Title of the pie chart.
            XLabel - category_label (str): Custom label for category column in tooltips.
            YLabel - value_label (str): Custom label for the values.
            color_label (str): Custom label for the color column (if used).
            color_column (str, optional): Column for color differentiation.
            use_custom_colors (bool): Whether to apply custom colors from a
                dictionary.
            hole (float): Size of the hole in the middle (0 for full pie,
                >0 for donut).
            widget_key (str, optional): Unique key for Streamlit widgets to allow
                multiple charts on the same page.
            use_container_width (bool): Whether to use full width in Streamlit.

        Returns:
            None (Displays the chart in Streamlit)
        """
        if graph_df is None or XValues not in graph_df:
            st.error("Data is missing or incorrect column name provided.")
            return

        # Define custom color mapping (Adjust colors as needed)
        color_mapping = political_colors

        # Determine aggregation method
        if YValues:
            data = graph_df.groupby(XValues, observed=True, as_index=False)[
                YValues
            ].sum()
        else:
            data = graph_df[XValues].YValues().reset_index()
            data.columns = [XValues, "count"]
            XValues = "count"

        # Custom labels for tooltips
        labels = {XValues: XLabel, YValues: YLabel}

        if color_column:
            labels[color_column] = color_label

        # Determine color mapping
        if use_custom_colors:
            color_discrete_map = {
                cat: color_mapping.get(cat, "#636efa") for cat in data[XValues]
            }
        else:
            color_discrete_map = None

        # Create Pie Chart
        fig = px.pie(
            data,
            names=XValues,
            values=YValues,
            color=XValues if use_custom_colors else None,
            title=Title,
            hole=hole,
            labels=XLabel,
            color_discrete_map=color_discrete_map,
        )

        # Improve layout
        fig.update_layout(
            title=dict(xanchor="center", yanchor="top", x=0.5),
            legend=dict(orientation="h",
                        yanchor="top",
                        y=-0.1,
                        xanchor="center", x=0.5),
            legend_title=(
                XValues
                if XValues
                else "Legend" if legend_title is None else legend_title
            ),
        )

        # Display in Streamlit
        st.plotly_chart(fig, use_container_width=use_container_width)
