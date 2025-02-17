import streamlit as st
import calculations as ppcalc
import Visualisations as vis


def donorsheadlinespage_body():
    """
    This function displays the content of Page two.
    """
    donors_df = st.session_state.get("data_clean", None)
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
    donors_summary = donors_df.groupby(['DonorName','DonationType'])\
        .agg({'Value': ['count',
                        'sum',
                        'mean',
                        'median'],
              'RegulatedEntityName':'nunique'}).reset_index()
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
        st.write(f"* Between {min_date} and {max_date}, {donors} donors made "
                 f"{donations} these were worth in total £{totaldonations}."
                 f" The average donations per donor was {avg_donations}, and"
                 f" the median donation value was £{median_donation}.")
        # Graph showing average donor donation vs total number of
        # donations per donor with size of circle set to number of regulated
        # entities donated to.
        vis.plot_regressionplot(donors_summary,
                                y_column='Average Donation',
                                x_column='No of Donations',
                                size_column='Regulated Entities',
                                title='Avg. Donation vs No. of Donations per Donor',
                                y_label='Average Donation £',
                                x_label='Number of Donations',
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
        st.write('* The whisker and box graphs below shoe the distribution of '
                 ' Average Donation size by Donation Type. These reenforce the'
                 ' point that there are a few donors who make large donations,'
                 ' and the majority of donors make small donations, regardless'
                 ' of the type of donation.')
    vis.generate_boxplots(donors_summary,
                            column="Donation Type",
                            value_column='Average Donation',
                            row_height=5,
                            plots_per_row=2
                            )
    st.write("## Individual Donor Analysis and Data")
