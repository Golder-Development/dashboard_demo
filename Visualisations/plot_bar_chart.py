import streamlit as st
import plotly.express as px
from components.ColorMaps import political_colors
from utils.logger import logger
from utils.logger import log_function_call  # Import decorator


def plot_custom_bar_chart(
    graph_df,
    XValues,
    YValues,
    group_column=None,
    agg_func="count",
    title="Custom Bar Chart",
    XLabel=None,
    YLabel=None,
    orientation="v",
    barmode="group",
    color_palette="Set1",
    widget_key=None,
    x_scale="linear",
    y_scale="linear",
    legend_title=None,
    use_custom_colors=False,
    width='stretch',
    xaxis_sort="value_desc",  # Added option for x-axis sorting
):
    """
    Generates an interactive bar chart using Plotly Express
    Parameters:
    ...
    xaxis_sort (str): Sorting for x-axis ('alphabetic_asc', 'value_desc', 'value_asc').
    ...
    """
    if graph_df is None or XValues not in graph_df or YValues not in graph_df:
        st.error("Data is missing or incorrect column names provided.")
        logger.error("Data is missing or incorrect column names provided.")
        return
    
    # CRITICAL: Normalize string columns to prevent LargeUTF8 errors
    from data.data_file_defs import normalize_string_columns_for_streamlit
    graph_df = normalize_string_columns_for_streamlit(graph_df.copy())

    # Aggregate Data
    if agg_func == "sum":
        df_agg = (
            graph_df.groupby([XValues] + ([group_column] if group_column else []))
            .agg({YValues: "sum"})
            .reset_index()
        )
    elif agg_func == "avg":
        df_agg = (
            graph_df.groupby([XValues] + ([group_column] if group_column else []))
            .agg({YValues: "mean"})
            .reset_index()
        )
    elif agg_func == "count":
        df_agg = (
            graph_df.groupby([XValues] + ([group_column] if group_column else []))
            .agg({YValues: "count"})
            .reset_index()
        )
    elif agg_func == "max":
        df_agg = (
            graph_df.groupby([XValues] + ([group_column] if group_column else []))
            .agg({YValues: "max"})
            .reset_index()
        )
    elif agg_func == "min":
        df_agg = (
            graph_df.groupby([XValues] + ([group_column] if group_column else []))
            .agg({YValues: "min"})
            .reset_index()
        )

    logger.debug(f"Aggregated DataFrame: {df_agg}")

    # Apply x-axis sorting
    if xaxis_sort == "alphabetic_asc":
        df_agg = df_agg.sort_values(by=XValues, ascending=True)
    elif xaxis_sort == "value_desc":
        df_agg = df_agg.sort_values(by=YValues, ascending=False)
    elif xaxis_sort == "value_asc":
        df_agg = df_agg.sort_values(by=YValues, ascending=True)

    logger.debug(f"Sorted DataFrame: {df_agg}")

    color_mapping = political_colors

    # Debugging: Check what values will be mapped
    logger.debug(f"Unique XValues: {df_agg[XValues].unique()}")
    if group_column:
        logger.debug(f"Unique Group Column: {df_agg[group_column].unique()}")

    # Determine which column to apply color mapping to
    color_column = XValues if group_column is None else group_column

    # Determine color mapping
    color_discrete_map = {
        str(cat).strip(): color_mapping.get(str(cat).strip(),
                                            "#636efa") for cat in df_agg[color_column].unique()
    }

    logger.debug(f"Final color_discrete_map: {color_discrete_map}")

    # Generate Bar Chart
    fig = px.bar(
        df_agg,
        x=XValues if orientation == "v" else YValues,
        y=YValues if orientation == "v" else XValues,
        color=color_column,
        barmode=barmode,
        title=title,
        labels={XValues: XLabel or XValues, YValues: YLabel or YValues},
        color_discrete_map=color_discrete_map,
        color_discrete_sequence=color_discrete_map,
        orientation=orientation,
    )

    # Adjust bar width to auto-fill x-axis with a small gap
    fig.update_traces(width=0.9)

    # Debugging missing mappings
    missing_keys = [cat for cat in df_agg[XValues].unique() if cat not in color_mapping]
    logger.debug(f"Missing color mappings for: {missing_keys}")

    logger.debug(f"Generated Figure: {fig}")

    # Update layout with axis scale options
    fig.update_layout(
        xaxis={"type": x_scale},
        yaxis={"type": y_scale},
        legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5),
        legend_title=(legend_title if legend_title else group_column if group_column else "legend"),
        title=dict(xanchor="center", yanchor="top", x=0.5),
        margin=dict(l=0, r=0, t=50, b=0),
    )

    # Apply formatting to hover text if YValues is Value
    if YValues == "Value":
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br><br>"
            + YValues
            + ": £%{y:,.0f}<extra></extra>"
        )

    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)
    logger.info("Bar chart displayed successfully.")
