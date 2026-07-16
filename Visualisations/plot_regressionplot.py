import streamlit as st
import plotly.express as px
from components.ColorMaps import political_colors
from utils.plotly_v6_fix import get_plotly_safe_data, clean_plotly_figure
from utils.logger import logger
from utils.logger import log_function_call  # Import decorator


@log_function_call
def plot_regressionplot(
    graph_df,
    XValues="DonationEvents",
    YValues="DonationsValue",
    size_column=None,
    color_column=None,  # Allows color differentiation (e.g., by category)
    XLabel="Number of Donations",
    YLabel="Value of Donations (£)",
    Title="Number of Donations vs. Value of Donations by Regulated Entity",
    size_label="Regulated Entities",
    size_scale=1,  
    dot_size=50,
    x_scale="log",  # linear or log
    y_scale="log",  # linear or log
    use_custom_colors=False,
    legend_title=None,
    show_trendline=True,  # Option to enable regression trendline
    width='stretch',
):
    color_mapping = political_colors

    # Validate Data
    if graph_df is None or XValues not in graph_df or YValues not in graph_df:
        st.error("Data is missing or incorrect column names provided.")
        return

    # Assign size dynamically
    size_arg = size_column if size_column in graph_df else None

    # Determine color mapping
    if use_custom_colors and color_column and color_column in graph_df:
        color_discrete_map = {
            str(cat).strip(): color_mapping.get(str(cat).strip(), "#636efa")
            for cat in graph_df[color_column].unique()
        }
    else:
        color_discrete_map = None

    # --- FIX 1: DYNAMICALLY BUILD REQUIRED COLUMNS STREAM ---
    # We must explicitly list every column that Plotly relies on to safely clean it
    required_columns = [XValues, YValues]
    if size_arg:
        required_columns.append(size_column)
    if use_custom_colors and color_column and color_column in graph_df:
        required_columns.append(color_column)

    # Check plotly version and apply adapter for v6+ environment safety
    chart_data = get_plotly_safe_data(graph_df, required_columns)

    # Create Scatter Plot
    fig = px.scatter(
        chart_data,
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
    # Note: Using OLS ('ols') requires the 'statsmodels' package installed in your runtime env
    if show_trendline:
        try:
            # FIX 2: Pass chart_data rather than raw graph_df to prevent v6 serialization mismatch 
            trend_fig = px.scatter(
                chart_data,
                x=XValues,
                y=YValues,
                trendline="ols",
                log_x=(x_scale == "log"),
                log_y=(y_scale == "log"),
            )
            # Safely abstract the regression vector line calculation trace
            trend_trace = trend_fig.data[1]
            fig.add_trace(trend_trace)
            logger.debug("Regression trendline computed and appended successfully.")
        except Exception as trend_error:
            logger.warning(
                f"Could not calculate OLS Trendline. Ensure 'statsmodels' package "
                f"is installed. Error detail: {trend_error}"
            )

    # Improve Layout & Hover Info
    fig.update_layout(
        xaxis_title=XLabel,
        yaxis_title=YLabel,
        legend_title=dict(
            text=(
                color_column
                if color_column
                else "Legend" if legend_title is None else legend_title
            )
        ),
        hovermode="closest",
        legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5),
        title=dict(xanchor="center", yanchor="top", x=0.5),  # Centered title
    )

    # Display in Streamlit
    safe_fig_dict = clean_plotly_figure(fig)
    st.plotly_chart(safe_fig_dict, use_container_width=True)
    logger.info("Regression/Scatter chart displayed successfully.")
