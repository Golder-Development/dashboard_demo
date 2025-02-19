import streamlit as st
import calculations as ppcalc
import datetime as dt
import Visualisations as vis
import pandas as pd

def donorspage_body():
    """
    This function displays the content of Page two.
    """
    donors_df = st.session_state.get("data_clean", None)
    # donors_df = donors_df[donors_df["DonorStatus"] != "Registered Political\
    #    Party"]

    min_date = ppcalc.get_mindate(donors_df).date()
    max_date = ppcalc.get_maxdate(donors_df).date()

    # Add a date range slider
    date_range2 = st.slider(
        "Select Date Range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )

    # # Extract start and end dates from the slider
    start_date, end_date = date_range2
    start_date = dt.datetime.combine(start_date, dt.datetime.min.time())
    end_date = dt.datetime.combine(end_date, dt.datetime.max.time())

    # # Filter by date range
    date_filter = (donors_df["ReceivedDate"] >= start_date) & (donors_df
                                                               ["ReceivedDate"]
                                                               <= end_date)

    # --- Dropdown for donor Entity ---
    # Create a mapping of DonorName -> DonorId
    entity_mapping2 = dict(zip(donors_df["DonorName"], donors_df["DonorId"]))

    # Add "All" as an option and create a dropdown that displays names but
    # returns IDs
    selected_entity_name = (
        st.selectbox("Filter by Donor",
                     ["All"] + sorted(map(str, entity_mapping2.keys())))
    )

    # Get the corresponding ID for filtering
    selected_entity_id = (
        entity_mapping2.get(selected_entity_name, None)
        if selected_entity_name != "All" else None
    )

    # Apply filters
    filters = (
        {"DonorId": selected_entity_id}
        if selected_entity_name != "All"
        else None
    )

    # Apply filters to the dataset
    donors_d_df = donors_df[date_filter]

    if filters:
        donors_r_d_df = (
            donors_d_df[donors_d_df["DonorId"] == selected_entity_id]
        )
    else:
        donors_r_d_df = donors_d_df

    donors = ppcalc.get_donors_ct(donors_r_d_df)
    donations = ppcalc.get_donations_ct(donors_r_d_df)
    totaldonations = ppcalc.get_value_total(donors_r_d_df)
    median_donation = ppcalc.get_median_donation(donors_r_d_df)
    min_date_f = ppcalc.get_mindate(donors_r_d_df).date()
    max_date_f = ppcalc.get_maxdate(donors_r_d_df).date()
    avg_donations = donations/donors
    # create a summary dataframe of donors, count of donations, total value of
    # donations, median donation size, average donation size, number of
    # regulated entities donated to, average donation size per regulated entity
    # donated to, average donation size per donation
    donors_summary = donors_d_df.groupby(['DonorName', 'DonationType'])\
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
    donors_summary['Total Value'] = pd.to_numeric(donors_summary['Total Value'], errors='coerce')
    donors_summary['Regulated Entities'] = pd.to_numeric(donors_summary['Regulated Entities'], errors='coerce')
    donors_summary['Average Value per Regulated Entity'] =\
        donors_summary['Total Value'] / donors_summary['Regulated Entities']
    donors_summary['Average Number Donations per Entity'] =\
        donors_summary['No of Donations'] / donors_summary['Regulated Entities']
    donors_entity_summary = donors_d_df.groupby(['DonorName'])\
        .agg({'Value': ['count',
                        'sum',
                        'mean',
                        'median'],
              'RegulatedEntityName': 'nunique'}).reset_index()

    # Ensure aggregates are numeric
    donors_entity_summary.columns = ['RegulatedEntityName',
                                      'No of Donations',
                                      'Total Value',
                                      'Average Donation',
                                      'Median Donation',
                                      'Regulated Entities']
    for col in ['No of Donations',
                'Total Value',
                'Average Donation',
                'Median Donation',
                'Regulated Entities']:
        donors_entity_summary[col] = pd.to_numeric(donors_entity_summary[col], errors='coerce')
    donors_entity_summary.columns = ['Regulated Entity',
                                      'No of Donations',
                                      'Total Value',
                                      'Average Donation',
                                      'Median Donation',
                                      'Regulated Entities']
    donors_entity_summary['Average Value per Regulated Entity'] = (
        donors_entity_summary.apply(
            lambda row: row['Total Value'] / row['Regulated Entities']
            if row['Regulated Entities'] > 0 else 0, axis=1
        )
    )
    donors_entity_summary['Average Number Donations per Entity'] = (
        donors_entity_summary.apply(
            lambda row: row['No of Donations'] / row['Regulated Entities']
            if row['Regulated Entities'] > 0 else 0, axis=1
        )
    )
    donors_entity_summary['Regulated Entities_f'] = (
        donors_entity_summary['Average Number Donations per Entity']
        .apply(lambda x: f"{x:.0f}"))
    for col in ['Total Value',
                'Average Donation',
                'Median Donation',
                'Average Value per Regulated Entity']:
        donors_entity_summary[col] = pd.to_numeric(donors_entity_summary[col], errors='coerce')
        donors_entity_summary[col] = (
            donors_entity_summary[col]
            .apply(lambda x: f"£{ppcalc.format_number(x)}")
        )
    donors_entity_summary['Avg No. Donations Per Entity'] = (
        donors_entity_summary['Average Number Donations per Entity']
        .apply(lambda x: f"{x:.2f}")
    )
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
        st.write(f"* Between {min_date_f} and {max_date_f}, "
                 f"{selected_entity_name} made "
                 f"{donations} these were worth in total £{totaldonations}."
                 f" The average number of donations was {avg_donations}, and"
                 f" the median donation value was £{median_donation}.")
        # Graph showing average donor donation vs total number of
        # donations per donor with size of circle set to number of regulated
        # entities donated to.

    with col2:
        st.write(' * As can be easily seen from the graph, there is a vast'
                 ' number of donors who only make a single donation. These'
                 ' donations are generally under £1M and are made to a'
                 ' single regulated entity.')

    left, mid = st.columns(2)
    with left:
        vis.plot_custom_bar_chart(
                                    df=donors_r_d_df,
                                    x_column='DonorStatus',
                                    y_column='Value',
                                    group_column='DonationType',
                                    agg_func='sum',
                                    title='Total Donations by Donation Type',
                                    x_label='Donation Type',
                                    y_label='Donation £',
                                    orientation='v',
                                    barmode='stack',
                                    x_scale='category',
                                    y_scale='log',
                                    key='avg_donation_donation_type',
                                    use_container_width=True
                                )
    with mid:

        st.write("<div style='text-align: center;'><b>Size of circles "
                 "represent the Average Value in GBP per entity.</b></div>",
                 unsafe_allow_html=True)

    # Display the styled dataframe
    st.dataframe(donors_summary.style.format({"Total Value": "£{:.2f}",
                                              "Average Donation": "£{:.2f}",
                                              "Median Donation": "£{:.2f}",
                                              "Average Value per Regulated Entity": "£{:.2f}"}))
    # Top 5 donors
    st.write("### Top 5 Most Promiscuous Donors")
    st.dataframe(ppcalc.get_top_donors(donors_entity_summary,
                                       "Regulated Entities"))

    st.write("### Top 5 Most Generous Overall Donors")
    st.dataframe(ppcalc.get_top_donors(donors_entity_summary,
                                       "Total Value"))

    st.write("### Top 5 Most Generous on Avg Donors")
    st.dataframe(ppcalc.get_top_donors(donors_entity_summary,
                                       "Average Donation"))

    st.write("### Top 5 Most Generous on Avg Donors (Excluding single donations)")
    st.dataframe(ppcalc.get_top_donors(donors_entity_summary,
                                       "Average Donation",
                                       exclude_single_donation=True))

    st.write("### Top 5 Most Active Donors by No of Donations")
    st.dataframe(ppcalc.get_top_donors(donors_entity_summary,
                                       "No of Donations",
                                       exclude_single_donation=False))
