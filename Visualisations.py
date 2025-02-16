import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns


def format_number(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:,.1f}M"
    elif value >= 10_000:
        return f"{value / 1_000:,.1f}k"
    else:
        return f"{value:,.2f}"


def plot_donations_by_year(Data='filtered_df', XValues='YearReceived', YValue='Value', GGroup='RegEntity_Group', XLabel='Year', YLabel='Total Value (£)', Title='Donations by Year and Entity Type'):
    """
    Plots a stacked bar chart of donations by year and entity type.

    Parameters:
        filtered_df (pd.DataFrame): The dataset containing the filtered donations.
        XValues (str): The column name for the x-axis values.
        YValues (str): The column name for the y-axis values.
        GGroup (str): The column name for the group values

    Returns:
        None (displays the plot in Streamlit)
    """
    filtered_df = Data
    # Group data by YearReceived and RegulatedEntityType, summing the 'Value' column
    donations_by_year_entity = filtered_df.groupby([XValues, GGroup])[YValue].sum().unstack().fillna(0)

    # Create figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot stacked bar chart
    donations_by_year_entity.plot(kind='bar', stacked=True, ax=ax)

    # Set labels and title
    ax.set_xlabel(XLabel)
    ax.set_ylabel(YLabel)
    ax.set_title(Title)

    # Format axes using EngFormatter for better readability
    # ax.xaxis.set_major_formatter(ticker.EngFormatter())  # Ensure x-axis shows whole numbers
    ax.yaxis.set_major_formatter(ticker.EngFormatter())  # Engineering notation for large numbers

    # Add legend
    ax.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)

def plot_regressionplot(
        sum_df,
        x_column="DonationEvents",
        y_column="DonationsValue",
        x_label="Number of Donations",
        y_label="Value of Donations (£)",
        title="Number of Donations vs. Value of Donations by Regulated Entity"
        ):
    """
    Creates and displays a regression plot with customizable labels.

    Parameters:
        sum_df (pd.DataFrame): DataFrame containing data for visualization.
        x_column (str): Column name for x-axis values.
        y_column (str): Column name for y-axis values.
        x_label (str): Label for the x-axis.
        y_label (str): Label for the y-axis.
        title (str): Title of the chart.

    Returns:
        None
    """
    if sum_df is None or x_column not in sum_df or y_column not in sum_df:
        st.error("Data is missing or incorrect column names provided.")
        return

    fig, ax = plt.subplots()
    sns.regplot(x=sum_df[x_column], y=sum_df[y_column], ax=ax)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))

    st.pyplot(fig)


def plot_pie_chart(
        df,
        category_column,
        value_column=None,
        title="Pie Chart",
        autopct_format="{p:.0f}%",
        start_angle=90
        ):
    """
    Creates and displays a pie chart in Streamlit, allowing aggregation by count or sum.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        category_column (str): The column used for grouping (categorical variable).
        value_column (str, optional): The column used for summing values. If None, counts instances.
        title (str): The title of the pie chart.
        autopct_format (str): The format of percentage labels (default "{p:.0f}%").
        start_angle (int): The starting angle for the pie chart (default 90 degrees).

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
    grouped_data.plot.pie(ax=ax, autopct=lambda p: autopct_format.format(p=p), startangle=start_angle)

    ax.set_title(title)
    ax.axis('equal')  # Ensures the pie chart is circular

    st.pyplot(fig)


"""
stored visulisation functions not used in the final app
        # Add a graph comparing the number of donations per RegulatedEntity to the value of donations
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
        vis.plot_pie_chart(sum_df, category_column="RegEntity_Group", title="Donations by Regulated Entity")
        # Create the pie chart
        vis.plot_pie_chart(sum_df, category_column="RegEntity_Group", value_column="DonationsValue", title="Value of Donations by Regulated Entity")

"""
