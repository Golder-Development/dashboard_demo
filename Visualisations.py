import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
# import seaborn as sns
# import calculations as ppcalc
import math
import plotly


def plot_donations_by_year(Data='filtered_df',
                           XValues='YearReceived',
                           YValue='Value',
                           GGroup='RegEntity_Group',
                           XLabel='Year',
                           YLabel='Total Value (£)',
                           Title='Donations by Year and Entity Type',
                           CalcType='sum',
                           use_container_width=True
                           ):
    """
    Plots a stacked bar chart of donations by year and entity type.

    Parameters:
        filtered_df (pd.DataFrame): The dataset containing the filtered
                                    donations.
        XValues (str): The column name for the x-axis values.
        YValues (str): The column name for the y-axis values.
        GGroup (str): The column name for the group values

    Returns:
        None (displays the plot in Streamlit)
    """
    filtered_df = Data
    # Group data using requested columns and calculation type
    if CalcType == 'sum':
        donations_by_year_entity = filtered_df.groupby([XValues,
            GGroup])[YValue].sum().unstack().fillna(0)
    if CalcType == 'avg':
        donations_by_year_entity = filtered_df.groupby([XValues,
            GGroup])[YValue].mean().unstack().fillna(0)
    if CalcType == 'count':
        donations_by_year_entity = filtered_df.groupby([XValues,
            GGroup])[YValue].count().unstack().fillna(0)
    if CalcType == 'median':
        donations_by_year_entity = filtered_df.groupby([XValues,
            GGroup])[YValue].median().unstack().fillna(0)
    if CalcType == 'max':
        donations_by_year_entity = filtered_df.groupby([XValues,
            GGroup])[YValue].max().unstack().fillna(0)
    if CalcType == 'min':
        donations_by_year_entity = filtered_df.groupby([XValues,
            GGroup])[YValue].min().unstack().fillna(0)
    if CalcType == 'std':
        donations_by_year_entity = filtered_df.groupby([XValues,
            GGroup])[YValue].std().unstack().fillna(0)
    if CalcType == 'var':
        donations_by_year_entity = filtered_df.groupby([XValues,
            GGroup])[YValue].var().unstack().fillna(0)
    if CalcType == 'sem':
        donations_by_year_entity = filtered_df.groupby([XValues,
            GGroup])[YValue].sem().unstack().fillna(0)
    if CalcType == 'skew':
        donations_by_year_entity = filtered_df.groupby([XValues,
            GGroup])[YValue].skew().unstack().fillna(0)
    if CalcType == 'kurt':
        donations_by_year_entity = filtered_df.groupby([XValues,
            GGroup])[YValue].kurt().unstack().fillna(0)
    if CalcType == 'quantile':
        donations_by_year_entity = filtered_df.groupby([XValues,
            GGroup])[YValue].quantile().unstack().fillna(0)
    if CalcType == 'corr':
        donations_by_year_entity = filtered_df.groupby([XValues,
            GGroup])[YValue].corr().unstack().fillna(0)
    if CalcType == 'cov':
        donations_by_year_entity = filtered_df.groupby([XValues,
            GGroup])[YValue].cov().unstack().fillna(0)
    else:
        donations_by_year_entity = filtered_df.groupby([XValues,
            GGroup])[YValue].sum().unstack().fillna(0)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot stacked bar chart
    donations_by_year_entity.plot(kind='bar', stacked=True, ax=ax)

    # Set labels and title
    ax.set_xlabel(XLabel)
    ax.set_ylabel(YLabel)
    ax.set_title(Title)

    # Format axes using EngFormatter for better readability
    # Ensure x-axis shows whole numbers
    # ax.xaxis.set_major_formatter(ticker.EngFormatter())
    # # Engineering notation for large numbers
    ax.yaxis.set_major_formatter(ticker.EngFormatter())

    # Add legend
    ax.legend()

    # Display the plot in Streamlit
    st.plotly_chart(fig.get_figure(), use_container_width=True)


def plot_regressionplot(sum_df,
                        x_column="DonationEvents",
                        y_column="DonationsValue",
                        size_column=None,
                        x_label="Number of Donations",
                        y_label="Value of Donations (£)",
                        title="Number of Donations vs. Value of Donations by Regulated Entity",
                        size_label="Regulated Entities",
                        size_scale=0.5,
                        y_scale='log',
                        x_scale='log',
                        dot_size=50,
                        use_container_width=True):
    """
    Creates and displays a regression plot with customizable labels and
    dot size using Plotly.

    Parameters:
    sum_df (pd.DataFrame): DataFrame containing data for visualization.
    x_column (str): Column name for x-axis values.
    y_column (str): Column name for y-axis values.
    size_column (str, optional): Column name for dot sizes. If None, uses a fixed size.
    x_label (str): Label for the x-axis.
    y_label (str): Label for the y-axis.
    title (str): Title of the chart.
    size_label (str): Label for the dot sizes.
    size_scale (float): Scale factor for the dot sizes.
    y_scale (str): Scale for the y-axis (default 'Log').
    x_scale (str): Scale for the x-axis (default 'Log').
    dot_size (int): Default size of the dots in the plot if size_column is None.

    Returns:
    None
    """
    if sum_df is None or x_column not in sum_df or y_column not in sum_df:
        st.error("Data is missing or incorrect column names provided.")
        return

    if size_column and size_column in sum_df:
        sizes = sum_df[size_column] * size_scale
    else:
        sizes = dot_size

    fig = plotly.express.scatter(
        sum_df,
        x=x_column,
        y=y_column,
        size=sizes,
        size_max=dot_size,
        labels={x_column: x_label, y_column: y_label, size_column: size_label},
        title=title,
        log_x=(x_scale == 'log'),
        log_y=(y_scale == 'log')
    )

    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label,
        title=title
    )

    st.plotly_chart(fig.get_figure(), use_container_width=True)


def plot_pie_chart(
        df,
        category_column,
        value_column=None,
        title="Pie Chart",
        autopct_format="{p:.0f}%",
        start_angle=90
        ):
    """
    Creates and displays a pie chart in Streamlit, allowing aggregation by
        count or sum.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        category_column (str): The column used for grouping (categorical
                                variable).
        value_column (str, optional): The column used for summing values.
                                        If None, counts instances.
        title (str): The title of the pie chart.
        autopct_format (str): The format of percentage labels (default
                                    "{p:.0f}%").
        start_angle (int): The starting angle for the pie chart (default
                                    90 degrees).

    Returns:
        None
    """
    if df is None or category_column not in df:
        st.error("Data is missing or incorrect column name provided.")
        return

    # Determine how to aggregate: Count instances or sum a numerical column
    if value_column and value_column in df:
        grouped_data = df.groupby(category_column)[value_column].sum()
    else:
        grouped_data = df[category_column].value_counts()

    # Plot the pie chart
    fig, ax = plt.subplots()
    grouped_data.plot.pie(ax=ax, autopct=lambda p: autopct_format.format(p=p),
                          startangle=start_angle)

    ax.set_title(title)
    ax.axis('equal')  # Ensures the pie chart is circular

    st.plotly_chart(fig.get_figure(), use_container_width=True)


"""
stored visulisation functions not used in the final app
        # Add a graph comparing the number of donations per RegulatedEntity to
        #   the value of donations
        if sum_df is not None:
            vis.plot_regressionplot(
                sum_df,
                x_column="DonationEvents",
                y_column="DonationsValue",
                x_label="Total Donations",
                y_label="Donation Amount (£)",
                title="Impact of Donations on Political Entities"
            )
        # Plot the pie chart
        vis.plot_pie_chart(sum_df, category_column="RegEntity_Group",
            title="Donations by Regulated Entity")
        # Create the pie chart
        vis.plot_pie_chart(sum_df, category_column="RegEntity_Group",
            value_column="DonationsValue", title="Value of Donations by
                            Regulated Entity")

"""


def generate_boxplots(df,
                      column="All",
                      value_column="Value",
                      plots_per_row=3,
                      row_height=5,
                      yscale='log',
                      use_container_width=True):
    """
    Generates boxplots for each unique value in the specified column of a
    dataframe using Plotly.

    Parameters:
    - df: pandas DataFrame
    - column: str, the column to group by (e.g., 'RegEntity_Group')
    - value_column: str, the column to plot values for (e.g., 'Value')
    - plots_per_row: int, number of plots per row in the output
    - yscale: str, scale for the y-axis (e.g., 'log' or 'linear')
    Returns:
    - None (shows the plots)
    Example of code to use module:
    - generate_boxplots(df, column='RegEntity_Group', value_column='Value')
    """
    import plotly.express as px
    import plotly.subplots as sp

    if column == "All":
        unique_groups = ["All"]
        num_rows = 1
    else:
        unique_groups = df[column].unique()
        num_rows = math.ceil(len(unique_groups) / plots_per_row)

    fig = sp.make_subplots(rows=num_rows, cols=plots_per_row, subplot_titles=[f'Boxplot of {value_column} for {group}' for group in unique_groups])

    for idx, group in enumerate(unique_groups):
        if column == "All":
            group_data = df[value_column].dropna()
        else:
            group_data = df.loc[df[column] == group, value_column].dropna()

        row = idx // plots_per_row + 1
        col = idx % plots_per_row + 1

        box = px.box(df[df[column] == group] if column != "All" else df, y=value_column, points="all", log_y=(yscale == 'log'))
        for trace in box.data:
            fig.add_trace(trace, row=row, col=col)

    fig.update_layout(height=row_height * num_rows * 100, showlegend=False)
    st.plotly_chart(fig.get_figure(), use_container_width=True)
