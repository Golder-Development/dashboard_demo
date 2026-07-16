import streamlit as st
import plotly.express as px
import pandas as pd
from components.ColorMaps import political_colors
from utils.plotly_v6_fix import get_plotly_safe_data, clean_plotly_figure
from utils.logger import log_function_call, logger


@log_function_call
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
    width='stretch',
    show_filter_box=False,
):
    # logging debug - Piechart code - initial parameters
    logger.debug(
        f"plot_pie_chart called with parameters: "
        f"XValues={XValues}, YValues={YValues}, Title={Title}, "
        f"XLabel={XLabel}, YLabel={YLabel}, color_column={color_column}, "
        f"use_custom_colors={use_custom_colors}, hole={hole}, "
        f"widget_key={widget_key}, legend_title={legend_title}"
    )
    
    if graph_df is None or XValues not in graph_df:
        st.error("Data is missing or incorrect column name provided.")
        return
    
    # CRITICAL: Normalize string columns to prevent LargeUTF8 errors
    from data.data_file_defs import normalize_string_columns_for_streamlit
    graph_df = normalize_string_columns_for_streamlit(graph_df.copy())

    # Define custom color mapping (Adjust colors as needed)
    color_mapping = political_colors

    # Determine aggregation method
    if YValues and YValues in graph_df:
        # If a value column exists, sum up the values
        data = graph_df.groupby(XValues, observed=True, as_index=False)[YValues].sum()
        numeric_col = YValues
    else:
        # FIX 1: Use value_counts() instead of non-existent .YValues() method
        # This safely counts occurrences of each group
        data = graph_df[XValues].value_counts().reset_index()
        # Columns of value_counts in modern pandas are [XValues, 'count']
        data.columns = [XValues, "count"]
        numeric_col = "count"

    # Custom labels for tooltips
    labels_dict = {XValues: XLabel or XValues, numeric_col: YLabel or numeric_col}

    if color_column:
        labels_dict[color_column] = color_label or color_column

    # Determine color mapping
    if use_custom_colors:
        color_discrete_map = {
            str(cat).strip(): color_mapping.get(str(cat).strip(), "#636efa") 
            for cat in data[XValues].unique()
        }
    else:
        color_discrete_map = None

    # --- FIX 3: SAFELY GENERATE REQUIRED COLUMNS ---
    # We dynamically build the list depending on whether we counted or summed
    required_columns = [XValues, numeric_col]
    if color_column and color_column in data.columns:
        required_columns.append(color_column)

    # Check plotly version and apply fix for v6 onwards
    chart_data = get_plotly_safe_data(data, required_columns)

    # Create Pie Chart
    fig = px.pie(
        chart_data,
        names=XValues,
        values=numeric_col,
        # FIX 2: Added color column parameter to ensure discrete color mapping applies correctly
        color=XValues if use_custom_colors else None, 
        title=Title,
        hole=hole,
        labels=labels_dict,  # FIX 2: Must be passed as a dictionary, not a raw string!
        color_discrete_map=color_discrete_map,
    )

    # Improve layout
    fig.update_layout(
        title=dict(xanchor="center", yanchor="top", x=0.5),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="center", 
            x=0.5
        ),
        legend_title=dict(
            text=(legend_title if legend_title else XLabel if XLabel else XValues)
        ),
    )

    # Display in Streamlit
    safe_fig_dict = clean_plotly_figure(fig)
    st.plotly_chart(safe_fig_dict, use_container_width=True)
    logger.info("Pie chart displayed successfully.")