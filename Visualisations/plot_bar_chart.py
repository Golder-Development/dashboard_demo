import streamlit as st
import plotly.express as px
from components.ColorMaps import political_colors
from utils.logger import streamlit_logger as logger
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
    if graph_df is None or XValues not in graph_df or YValues not in graph_df:
        st.error("Data is missing or incorrect column names provided.")
        logger.error("Data is missing or incorrect column names provided.")
        return

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

    color_mapping = political_colors
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
        x=XValues if orientation == "v" else YValues,
        y=YValues if orientation == "v" else XValues,
        color=group_column if group_column else None,
        barmode=barmode,
        title=title,
        labels={XValues: XLabel or XValues, YValues: YLabel or YValues},
        color_discrete_map=color_discrete_map,
        color_discrete_sequence=px.colors.qualitative.__dict__.get(
            color_palette, px.colors.qualitative.Set1
        ),
        orientation=orientation,
    )

    logger.debug(f"Generated Figure: {fig}")

    # Update layout with axis scale optionslegend_title if legend_title 
    # else group_column if group_column else "legend"),
    fig.update_layout(
        xaxis={"type": x_scale},
        yaxis={"type": y_scale},
        legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5),  # Display in Streamlit
        legend_title=(legend_title if legend_title else group_column if group_column else "legend"),    
        title=dict(xanchor="center", yanchor="top", x=0.5),
        margin=dict(l=0, r=0, t=50, b=0),
    )
    # Apply formatting to hover text if YValues is Value, then apply format_number and add a £ sign
    if YValues == "Value":
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br><br>"
            + YValues
            + ": £%{y:,.0f}<extra></extra>"
        )
    
    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=use_container_width)
    logger.info("Bar chart displayed successfully.")
