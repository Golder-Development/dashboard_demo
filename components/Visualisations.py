import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.logger import log_function_call, logger


@log_function_call
def plot_regressionplot(graph_df,
                        XValues,
                        YValues,
                        Title,
                        widget_key,
                        show_trendline=True):
    if graph_df is None or not all(col in graph_df.columns for col in [XValues, YValues]):
        st.error("Missing required columns in dataset.")
        logger.error(f"Missing required columns in dataset. {__name__}")
        return

    fig = px.scatter(graph_df, x=XValues, y=YValues, title=title, trendline="ols" if show_trendline else None)

    if show_trendline and len(fig.data) > 1:
        fig.add_trace(fig.data[1])
    else:
        st.warning("Insufficient data for regression trendline.")

    st.plotly_chart(fig)


@log_function_call
def plot_pie_chart(graph_df,
                   XValues,
                   YValues,
                   color_column=None,
                   use_custom_colors=False,
                   color_mapping=None,
                   Title="Pie Chart",
                   YLabel="Value",
                   XLabel="Category",
                   hole=0.3,
                   widget_key="default"):
    
    # Ensure the required columns exist
    if XValues not in graph_df.columns or YValues not in graph_df.columns:
        st.error(f"❌ Error: Columns '{XValues}' or '{YValues}' not found in dataset.")
        logger.error(f"Columns '{XValues}' or '{YValues}' not found in dataset. {__name__}")
        return
    
    # Handle missing values in category column
    graph_df = graph_df.copy()  # Prevent modifying original DataFrame
    if graph_df[XValues].isna().any():
        st.warning(f"⚠️ Missing values detected in '{XValues}'. Filling with 'Unknown'.")
        graph_df[XValues] = graph_df[XValues].fillna("Unknown")

    # Aggregate data
    data = graph_df.groupby(XValues, as_index=False)[YValues].sum()

    # Apply custom colors if enabled
    color_discrete_map = {cat: color_mapping.get(cat, "#636efa") for cat in data[XValues]} if use_custom_colors and color_mapping else None

    # Create pie chart
    fig = px.pie(data, names=XValues, values=YValues, title=Title, hole=hole, 
                 color=XValues, color_discrete_map=color_discrete_map)

    # Display chart
    st.plotly_chart(fig)


@log_function_call
def plot_custom_bar_chart(graph_df,
                          XValues,
                          YValues,
                          Title,
                          use_custom_colors,
                          color_mapping,
                          group_column=None):
    if graph_df is None or not all(col in graph_df.columns for col in [XValues, YValues]):
        logger.error(f"Missing required columns in dataset. {__name__}")
        return

    color_discrete_map = {cat: color_mapping.get(cat, "#636efa") for cat in graph_df[group_column]} if use_custom_colors and group_column else None

    fig = px.bar(graph_df,
                 x=XValues,
                 y=YValues,
                 title=Title,
                 color=group_column,
                 color_discrete_map=color_discrete_map)
    st.plotly_chart(fig)


@log_function_call
def plot_bar_line_by_year(graph_df,
                          XValues="Year",
                          YValues="Value",
                          GroupData="DonationType",
                          XLabel="Year",
                          YLabel="Total",
                          Title=None,
                          CalcType="sum",
                          use_custom_colors=False,
                          percentbars=False,
                          LegendTitle="Donation Type",
                          ChartType="Bar",
                          y_scale="linear",
                          widget_key="default"):
    if Title is None:
        Title = f"{YLabel} by {XLabel}, grouped by {LegendTitle}"
    if graph_df is None or XValues not in graph_df.columns or YValues not in graph_df.columns:
        st.error("Missing required columns in dataset.")
        logger.error(f"Missing required columns in dataset. {__name__}")
        return

    aggregation_methods = {"sum": "sum", "average": "mean", "count": "count"}
    if CalcType not in aggregation_methods:
        st.warning(f"Invalid CalcType '{CalcType}'. Defaulting to 'sum'.")
        CalcType = "sum"

    df_agg = (
        graph_df.groupby(XValues)[YValues]
        .agg(aggregation_methods[CalcType])
        .reset_index()
    )
    year_options = sorted(df_agg[XValues].unique())

    if not year_options:
        st.warning("No available years in dataset.")
        return

    selected_years = st.slider(
        "Select Year Range",
        min_value=min(year_options),
        max_value=max(year_options),
        value=(min(year_options), max(year_options)),
        key=f"year_slider_{widget_key}"
    )
    df_agg = df_agg[(df_agg[XValues] >= selected_years[0]) & 
                    (df_agg[XValues] <= selected_years[1])]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_agg[XValues],
                         y=df_agg[YValues],
                         name=Title))
    fig.add_trace(go.Scatter(x=df_agg[XValues],
                             y=df_agg[YValues],
                             mode='lines+markers',
                             name="Trend"))

    fig.update_layout(title=Title,
                      xaxis_title=XValues,
                      yaxis_title=YValues)
    st.plotly_chart(fig)
