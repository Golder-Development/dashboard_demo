def hlf_body():
    """
    This function displays the content of Page two.
    """
    import streamlit as st
    import calculations as ppcalc
    import matplotlib.pyplot as plt

    df = st.session_state.get("data", None)
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
        st.write(f"* During the period from {min_date} to {max_date}, {unique_regulated_entities} "
                 "regulated political bodies received donations")
        st.write(f"* These reveived a total value of £{total_value_donations} from {unique_donors} unique donors")
        st.write(f"* The average donation was £{mean_value_donations} and there were {unique_donations} unique donations")
    with col2:
        # use data from the dataset
        st.write("## Headline Visuals")
        st.write("* Share of number of donations by Regulated Entity")
        if df is not None:
            # Plot the pie chart
            fig, ax = plt.subplots()
            filtered_df["RegulatedEntityName"].value_counts().plot.pie(ax=ax, autopct='%1.1f%%', startangle=90)

            # Set the title and ensure the chart is circular
            ax.set_title("Regulated Entity Distribution")
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Display the chart in Streamlit
            st.pyplot(fig)
        else:
            st.error("Data not found. Please check dataset loading in the "
                     "main app.")
        st.write("* Share of value of donations by party")
        if df is not None:
            # Group by RegulatedEntityName and sum the 'Value' column
            grouped_data = filtered_df.groupby("RegulatedEntityName")["Value"].sum()

            # Create the pie chart
            fig, ax = plt.subplots()
            grouped_data.plot.pie(ax=ax, autopct='%1.1f%%', startangle=90)

            # Set the title and ensure the chart is circular
            ax.set_title("Regulated Entity Donation Distribution")
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Display the chart in Streamlit
            st.pyplot(fig)
        else:
            st.error("Data not found. Please check dataset loading in the "
                     "main app.")
    st.write("## Next Steps")
