import streamlit as st
import calculations as ppcalc
import Visualisations as vis


def donorsheadlinespage_body():
    """
    This function displays the content of Page two.
    """
    donors_df = st.session_state.get("data_clean", None)
    donors_df = donors_df[donors_df["DonorStatus"] != "Registered Political\
        Party"]
    donors = ppcalc.get_donors_ct(donors_df)
    donations = ppcalc.get_donations_ct(donors_df)
    totaldonations = ppcalc.get_value_total(donors_df)
    median_donation = ppcalc.get_median_donation(donors_df)
    min_date = ppcalc.get_mindate(donors_df).date()
    max_date = ppcalc.get_maxdate(donors_df).date()
    avg_donations = donations/donors
    # create a summary dataframe of donors, count of donations, total value of
    # donations, median donation size, average donation size, number of
    # regulated entities donated to, average donation size per regulated entity
    # donated to, average donation size per donation
    donors_summary = donors_df.groupby(['DonorName', 'DonationType'])\
        .agg({'Value': ['count',
                        'sum',
                        'mean',
                        'median'],
              'RegulatedEntityName': 'nunique'}).reset_index()
    donors_summary.columns = ['Donor Name',
                              'Donation Type',
                              'No of Donations',
                              'Total Value',
                              'Average Donation',
                              'Median Donation',
                              'Regulated Entities']
    donors_summary['Average Value per Regulated Entity'] =\
        donors_summary['Total Value'] / donors_summary['Regulated Entities']
    donors_summary['Average Number Donations per Entity'] =\
        donors_summary['No of Donations'] / donors_summary['Regulated Entities']
    donors_topline_summary = donors_df.groupby(['DonorName'])\
        .agg({'Value': ['count',
                        'sum',
                        'mean',
                        'median'],
              'RegulatedEntityName': 'nunique'}).reset_index()
    donors_topline_summary.columns = ['Donor Name',
                                      'No of Donations',
                                      'Total Value',
                                      'Average Donation',
                                      'Median Donation',
                                      'Regulated Entities']
    donors_topline_summary['Average Value per Regulated Entity'] =\
        donors_topline_summary['Total Value'] / donors_topline_summary[
            'Regulated Entities']
    donors_topline_summary['Average Number Donations per Entity'] =\
        donors_topline_summary['No of Donations'] / donors_topline_summary[
            'Regulated Entities']
    donors_topline_summary['Regulated Entities_f'] = donors_topline_summary[
        'Average Number Donations per Entity'].apply(lambda x: f"{x:.0f}")
    donors_topline_summary['Total Donations £'] = donors_topline_summary[
        'Total Value'].apply(lambda x: f"£{ppcalc.format_number(x)}")
    donors_topline_summary['Avg Donations'] = donors_topline_summary[
        'Average Donation'].apply(lambda x: f"£{ppcalc.format_number(x)}")
    donors_topline_summary['Median Donations'] = donors_topline_summary[
        'Median Donation'].apply(lambda x: f"£{ppcalc.format_number(x)}")
    donors_topline_summary['Avg Value Per Entity'] = donors_topline_summary[
        'Average Value per Regulated Entity'].apply(lambda x: f"£{ppcalc.format_number(x)}")
    donors_topline_summary['Avg No. Donations Per Entity'] = \
        donors_topline_summary['Average Number Donations per Entity'].apply(lambda x: f"{x:.2f}")
    # Apply formating to values
    donors = ppcalc.format_number(donors)
    donations = ppcalc.format_number(donations)
    totaldonations = ppcalc.format_number(totaldonations)
    avg_donations = f"{avg_donations:.2f}"
    median_donation = ppcalc.format_number(median_donation)
    st.write("# Analysis of Political Donations by Donor")
    st.write("## Headline Figures")
    col1, col2 = st.columns(2)
    with col1:
        st.write("* For this analysis, any donations made by Political Parties"
                 " have been excluded. This is to focus on donations made by"
                 " individuals, companies, and other organisations.")
        st.write(f"* Between {min_date} and {max_date}, {donors} donors made "
                 f"{donations} these were worth in total £{totaldonations}."
                 f" The average donations per donor was {avg_donations}, and"
                 f" the median donation value was £{median_donation}.")
        # Graph showing average donor donation vs total number of
        # donations per donor with size of circle set to number of regulated
        # entities donated to.
        vis.plot_regressionplot(donors_topline_summary,
                                y_column='Average Donation',
                                x_column='No of Donations',
                                size_column='Regulated Entities',
                                title='Avg. Donation vs No. of Donations per Donor',
                                y_label='Average Donation £',
                                x_label='Number of Donations',
                                x_scale='linear',
                                size_label='Regulated Entities',
                                size_scale=0.5
                                )
    with col2:
        st.write(' * As can be easily seen from the graph, there is a vast'
                 ' number of donors who only make a single donation. These'
                 ' donations are generally under £1M and are made to a'
                 ' single regulated entity.')
        st.write('* There are a few donors who make multiple donations, and a '
                 ' few who make donations to multiple regulated entities. These'
                 ' donations are generally larger in value.')
        st.write('* From the charts below, we can see that on average, donors'
                 ' donated more using cash than other methods.  We can also see that'
                 ' quite a few donors made donations to multiple regulated entities.'
                 ' with BAA being the most promiscuous donor.')
        st.write('* The top 3 most generous donors overall where all Trade Unions, '
                 ' as were all 5 of the most active donors by number of donations. ')
        st.write('* The top 5 most generous on average donors were all individuals,'
                 ' and apart from 2 they each made a single donation. When we exclude'
                 ' donors who only made a single donation, the top 5 most generous'
                 ' on average donors were all except 1 still individuals.')
        st.write('* When we look at the Average value of donations per regulated entity'
                 ' and the number of Entities donated to, we see as the number of Entities'
                 ' donated to increased, the average donation per entity decreased.')
        st.write('* Unsurprisingly, the more Entities donated to more donations made.')
    left, mid = st.columns(2)
    with left:
        vis.plot_custom_bar_chart(
                                    df=donors_df,  # DataFrame to plot
                                    x_column='DonorStatus',  # Column for the x-axis (categorical)
                                    y_column='Value',  # Column for the y-axis (numerical)
                                    group_column='DonationType',  # No grouping by another column
                                    agg_func='sum',
                                    title='Total Donations by Donation Type',  # Title of the chart
                                    x_label='Donation Type',  # X-axis label
                                    y_label='Donation £',  # Y-axis label
                                    orientation='v',  # Vertical bars
                                    barmode='stack',  # Grouped bars
                                    x_scale='category',
                                    y_scale='log',
                                    # color_palette='Set1',  # Color palette for bars
                                    key='avg_donation_donation_type',  # Streamlit widget key
                                    use_container_width=True  # Ensures chart fits container width
                                )
        vis.plot_custom_bar_chart(
                                    df=donors_topline_summary,  # DataFrame to plot
                                    x_column='Regulated Entities',  # Column for the x-axis (categorical)
                                    y_column='Donor Name',  # Column for the y-axis (numerical)
                                    group_column=None,  # No grouping by another column
                                    agg_func='count',
                                    title='Count of Donors vs No of Regulated Entities',  # Title of the chart
                                    x_label='No of Regulated Entities',  # X-axis label
                                    y_label='No of Donors',  # Y-axis label
                                    orientation='v',
                                    barmode='stack',
                                    x_scale='log',
                                    y_scale='log',
                                    color_palette='Viridis',  # Color palette for bars
                                    key='reg_ent_don_name',  # Streamlit widget key
                                    use_container_width=True  # Ensures chart fits container width
                                )
    with mid:
        vis.plot_regressionplot(donors_topline_summary,
                                y_column='No of Donations',
                                x_column='Regulated Entities',
                                size_column='Average Value per Regulated Entity',
                                title='Average Value vs No. of Regulated Entities Donated to',
                                y_label='No. of Donations',
                                x_label='No. of Entities Donated to',
                                size_label='Avg Donated Value £',
                                size_scale=0.5
                                )
        st.write("<div style='text-align: center;'><b>Size of circles represent the Total Value in GBP.</b></div>", unsafe_allow_html=True)
        vis.plot_regressionplot(donors_topline_summary,
                                y_column='Total Value',
                                x_column='Regulated Entities',
                                size_column='Average Value per Regulated Entity',
                                title='Total Value vs No. of Regulated Entities Donated to',
                                y_label='Total Donations £',
                                x_label='No. of Entities Donated to',
                                size_label='Avg Donated Value £',
                                size_scale=0.5
                                )
        st.write("<div style='text-align: center;'><b>Size of circles represent the Average Value in GBP per entity.</b></div>", unsafe_allow_html=True)
    st.write("### Top 5 Most Promiscuous Donors: Entities Donated to")
    donors_summary2 = donors_topline_summary.sort_values('Regulated Entities', ascending=False)
    donors_summary2 = donors_summary2[['Donor Name',
                                       'Regulated Entities',
                                       'Avg No. Donations Per Entity',
                                       'No of Donations',
                                       'Total Donations £',
                                       'Avg Donations',
                                       'Median Donations',
                                       'Avg Value Per Entity'
                                       ]].head(5)
    donors_summary2_styled = donors_summary2.style.set_properties(
        subset=donors_summary2.columns[1:],  # Exclude the first column
        **{'text-align': 'center'}
    )
    # Display the styled dataframe
    st.dataframe(donors_summary2_styled)
    st.write("### Top 5 Most Generous Overall Donors")
    donors_summary2 = donors_topline_summary.sort_values('Total Value', ascending=False)
    donors_summary2 = donors_summary2[['Donor Name',
                                       'Regulated Entities',
                                       'Avg No. Donations Per Entity',
                                       'No of Donations',
                                       'Total Donations £',
                                       'Avg Donations',
                                       'Median Donations',
                                       'Avg Value Per Entity'
                                       ]].head(5)
    donors_summary2_styled = donors_summary2.style.set_properties(
        subset=donors_summary2.columns[1:],  # Exclude the first column
        **{'text-align': 'center'}
    )
    # Display the styled dataframe
    st.dataframe(donors_summary2_styled)
    st.write("### Top 5 Most Generous on Average Donors")
    donors_summary2 = donors_topline_summary.sort_values('Average Donation', ascending=False)
    donors_summary2 = donors_summary2[['Donor Name',
                                       'Regulated Entities',
                                       'Avg No. Donations Per Entity',
                                       'No of Donations',
                                       'Total Donations £',
                                       'Avg Donations',
                                       'Median Donations',
                                       'Avg Value Per Entity'
                                       ]].head(5)
    donors_summary2_styled = donors_summary2.style.set_properties(
        subset=donors_summary2.columns[1:],  # Exclude the first column
        **{'text-align': 'center'}
    )
    # Display the styled dataframe
    st.dataframe(donors_summary2_styled)
    st.write("### Top 5 Most Generous on Average Donors")
    st.write("#### Excluding donors who only made a single donation")
    donors_summary2 = donors_topline_summary.sort_values('Average Donation', ascending=False)
    donors_summary2 = donors_summary2[donors_summary2['No of Donations'] > 1]
    donors_summary2 = donors_summary2[['Donor Name',
                                       'Regulated Entities',
                                       'Avg No. Donations Per Entity',
                                       'No of Donations',
                                       'Total Donations £',
                                       'Avg Donations',
                                       'Median Donations',
                                       'Avg Value Per Entity'
                                       ]].head(5)
    donors_summary2_styled = donors_summary2.style.set_properties(
        subset=donors_summary2.columns[1:],  # Exclude the first column
        **{'text-align': 'center'}
    )
    # Display the styled dataframe
    st.dataframe(donors_summary2_styled)

    st.write("### Top 5 Most Active Donors by No of Donations")
    donors_summary2 = donors_topline_summary.sort_values('No of Donations', ascending=False)
    donors_summary2 = donors_summary2[['Donor Name',
                                       'Regulated Entities',
                                       'Avg No. Donations Per Entity',
                                       'No of Donations',
                                       'Total Donations £',
                                       'Avg Donations',
                                       'Median Donations',
                                       'Avg Value Per Entity'
                                       ]].head(5)
    donors_summary2_styled = donors_summary2.style.set_properties(
       subset=donors_summary2.columns[1:],  # Exclude the first column
                                            **{'text-align': 'center'}
    )
    # Display the styled dataframe
    st.dataframe(donors_summary2_styled)

    st.write("## Individual Donor Analysis and Data")
