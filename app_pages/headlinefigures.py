def hlf_body():
    """
    This function displays the content of Page two.
    """
    import streamlit as st
    import calculations as ppcalc
    import matplotlib.pyplot as plt
    import seaborn as sns

    def format_number(value):
        if value >= 1_000_000:
            return f"{value / 1_000_000:.1f}M"
        elif value >= 10_000:
            return f"{value / 1_000:.1f}k"
        else:
            return f"{value:,.2f}"

    df = st.session_state.get("data_clean", None)
    sum_df = st.session_state.get("data_party_sum", None)
    # set filters to None and filtered_df to the original dataset
    filters = None
    filtered_df = df
    # Call each function separately with the selected filter
    unique_donors = ppcalc.get_donors_ct(filtered_df, filters)
    total_value_donations = ppcalc.get_value_total(filtered_df, filters)
    mean_value_donations = ppcalc.get_value_mean(filtered_df, filters)
    unique_donations = ppcalc.get_donations_ct(filtered_df, filters)
    unique_regulated_entities = ppcalc.get_regentity_ct(filtered_df, filters)
    min_date = ppcalc.get_mindate(filtered_df, filters).date()
    max_date = ppcalc.get_maxdate(filtered_df, filters).date()

    # Display the headline figures
    st.write("# Topline Summary of Political Donations to the UK Political "
             "Parties")
    col1, col2 = st.columns(2)
    with col1:
        st.write("## Headline Figures")
        st.write(f"* During the period from {min_date} to {max_date}, {unique_regulated_entities:,} "
                 "regulated political bodies received donations")
        st.write(f"* These received a total value of £{format_number(total_value_donations)} from {unique_donors:,} unique donors")
        st.write(f"* The average donation was £{format_number(mean_value_donations)} and there were {unique_donations:,} unique donations")
        # Add a graph comparing the number of donations per RegulatedEntity to the value of donations
        st.write("## Donations vs. Value by Regulated Entity")
        if sum_df is not None:
            fig, ax = plt.subplots()
            sns.regplot(x=sum_df["DonationEvents"], y=sum_df["DonationsValue"], ax=ax)
            ax.set_xlabel("Number of Donations")
            ax.set_ylabel("Value of Donations (£)")
            ax.set_title("Number of Donations vs. Value of Donations by Regulated Entity")
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: format_number(x)))
            st.pyplot(fig)
        else:
            st.error("Summary data not found. Please check dataset loading in the main app.")
    with col2:
        # use data from the summary dataset
        st.write("## Headline Visuals")
        st.write("* Share of number of donations by Regulated Entity")
        if sum_df is not None:
            grouped_data = sum_df["RegEntity_Group"].value_counts()
            # Plot the pie chart
            fig, ax = plt.subplots()
            grouped_data.plot.pie(ax=ax, autopct=lambda p: f'{p:.0f}%', startangle=90)

            # Set the title and ensure the chart is circular
            ax.set_title("Regulated Entity Distribution")
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Display the chart in Streamlit
            st.pyplot(fig)
        else:
            st.error("Summary data not found. Please check dataset loading in the "
                     "main app.")
        st.write("* Share of value of donations by party")
        if sum_df is not None:
            # Group by RegEntity_Group and sum the 'DonationsValue' column
            grouped_data2 = sum_df.groupby("RegEntity_Group")["DonationsValue"].sum()
            # Create the pie chart
            fig, ax = plt.subplots()
            grouped_data2.plot.pie(ax=ax, autopct=lambda p: f'{p:.0f}%', startangle=90)

            # Set the title and ensure the chart is circular
            ax.set_title("Regulated Entity Donation Distribution")
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Display the chart in Streamlit
            st.pyplot(fig)
        else:
            st.error("Summary data not found. Please check dataset loading in the "
                     "main app.")



    # Add a visualization in col1 showing the cumulative Value of donations over time
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Cumulative Value of Donations Over Time")
        if filtered_df.empty:
            st.write("No data available for the selected filters.")
            return
        cumulative_value = filtered_df.groupby('ReceivedDate')['Value'].sum().cumsum()
        plt.figure(figsize=(10, 5))
        plt.plot(cumulative_value.index, cumulative_value.values, label='Cumulative Value')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Value (£)')
        plt.title('Cumulative Value of Donations Over Time')
        plt.legend()
        st.pyplot(plt)

    # Add a visualization in col2 showing the share of all donations by year by RegulatedEntityType
    with col2:
        st.write("### Share of Donations by Year and Regulated Entity Type")
        if filtered_df.empty:
            st.write("No data available for the selected filters.")
            return
        filtered_df['Year'] = filtered_df['ReceivedDate'].dt.year
        donations_by_year_entity = filtered_df.groupby(['Year', 'RegulatedEntityType'])['Value'].sum().unstack().fillna(0)
        donations_by_year_entity.plot(kind='bar', stacked=True, figsize=(10, 5))
        plt.xlabel('Year')
        plt.ylabel('Total Value (£)')
        plt.title('Share of Donations by Year and Regulated Entity Type')
        plt.legend(title='Regulated Entity Type')
        st.pyplot(plt)
    st.write("## Next Steps")
