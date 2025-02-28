import streamlit as st
from components.calculations import (
    get_mindate,
    get_maxdate,
    format_number,
    compute_summary_statistics
    )
import datetime as dt
import components.Visualisations as vis
from pandas import (
                    to_numeric
                    )


def donorspage_body():
    """
    This function displays the content of Page two.
    """
    # set page basic variables
    # Define filter condition
    target_entity = 'DonationType'
    target_filter = 'Cash'
    current_target = 'DonationType == "Cash"'
    target_label = "Cash Donation"
    filters = None
    show_filters = True
    # Set up filters
    filter_by_regentity_dropdown = False if show_filters is False else False
    filter_by_donor_dropdown = False if show_filters is False else True
    filter_by_date_slider = False if show_filters is False else True
    # Load dataset from session state
    cleaned_df = st.session_state.get("data", None)
    if cleaned_df is None:
        st.error("No data available. Please check if the dataset is loaded.")
        return
    # remove donations made by political parties
    cleaned_df = (
        cleaned_df[cleaned_df["DonorStatus"] != "Registered PoliticalParty"]
    )
    # # Get min and max dates from the dataset
    min_date = get_mindate(cleaned_df).date()
    max_date = get_maxdate(cleaned_df).date()

    # # Add a date range slider to filter by received date
    if filter_by_date_slider:
        date_range2 = st.slider(
            "Select Date Range",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="YYYY-MM-DD"
        )
        # # Extract start and end dates from the slider
        start_date, end_date = date_range2
    else:
        start_date = min_date
        end_date = max_date

    # --- Dropdown for Main Entity ---
    if filter_by_regentity_dropdown:
        # set filter by donor dropdown to false
        filter_by_donor_dropdown = False
        # set filter_entity
        filter_entity = "RegulatedEntityId"
        # Create a mapping of RegulatedEntityName -> RegulatedEntityId
        entity_mapping = dict(zip(cleaned_df["RegulatedEntityName"], cleaned_df
                              [filter_entity]))
        # Add "All" as an option and create a dropdown that displays names but
        # returns IDs
        selected_entity_name = st.selectbox("Filter by Regulated Entity",
                                            ["All"] +
                                            sorted(entity_mapping.keys()))
        # Get the corresponding ID for filtering
        selected_entity_id = entity_mapping.get(selected_entity_name, None)
        # Apply filters
        entity_filter = (
            {filter_entity: selected_entity_id}
            if selected_entity_name != "All" else {}
                        )
    elif filter_by_donor_dropdown:
        # set filter by donor dropdown to false
        filter_by_regentity_dropdown = False
        # set filter_entity
        filter_entity = "DonorId"
        # --- Dropdown for donor Entity ---
        # Create a mapping of DonorName -> DonorId
        entity_mapping = dict(zip(cleaned_df["DonorName"],
                                  cleaned_df[filter_entity]))
        # Add "All" as an option and create a dropdown that displays names but
        # returns IDs
        selected_entity_name = (
            st.selectbox("Filter by Donor",
                         ["All"] +
                         sorted(map(str, entity_mapping.keys())))
        )
        # Get the corresponding ID for filtering
        selected_entity_id = (
            entity_mapping.get(selected_entity_name, None)
            if selected_entity_name != "All" else None
        )
        # Apply filters
        entity_filter = (
            {filter_entity: selected_entity_id}
            if selected_entity_name != "All" else {}
                        )
    else:
        filter_entity = None
        entity_filter = None
        selected_entity_id = None
        selected_entity_name = "All"

    # set times on dates so min is earliest and max is latest
    start_date = dt.datetime.combine(start_date, dt.datetime.min.time())
    end_date = dt.datetime.combine(end_date, dt.datetime.max.time())

    # Filter by date range
    date_filter = (
        cleaned_df["ReceivedDate"] >= start_date) & (cleaned_df
                                                     ["ReceivedDate"]
                                                     <= end_date)

    # Create st.dataframe for chosen date range and all entities
    if date_filter is not None:
        cleaned_d_df = cleaned_df[date_filter]
    else:
        cleaned_d_df = cleaned_df
    # Create st.dataframe for chosen target all date range and all entities
    if current_target:
        cleaned_c_df = cleaned_df.query(current_target)
    else:
        cleaned_c_df = cleaned_df
    # Create st.dataframe for chosen entity all date range and all entities
    if entity_filter:
        cleaned_r_df = (
            cleaned_df[
                cleaned_df[filter_entity]
                == entity_filter[filter_entity]
                if entity_filter else True  # If no filters, return all rows
                      ]
                       )
    else:
        cleaned_r_df = cleaned_df
    # Create st.dataframe for chosen entity and date range all measures
    cleaned_r_d_df = (
        cleaned_r_df[date_filter] if date_filter.any() else cleaned_r_df
        )
    # Create st.dataframe for chosen target and date range all entities
    cleaned_c_d_df = cleaned_d_df.query(current_target)
    # Create st.dataframe for chosen target and entity all dates
    cleaned_c_r_df = cleaned_r_df.query(current_target)
    # Create st.dataframe for chosen target, entity and date range
    cleaned_c_r_d_df = cleaned_r_d_df.query(current_target)

    # Get the date range
    min_date = get_mindate(cleaned_c_d_df).date()
    max_date = get_maxdate(cleaned_c_d_df).date()

    # Get the number of donors, donations, total value of donations, median
    ostats = compute_summary_statistics(cleaned_d_df)
    tstats = compute_summary_statistics(cleaned_r_d_df)
    # create a summary st.dataframe of donors
    donors_summary = cleaned_d_df.groupby(['DonorName', 'DonationType'])\
        .agg({'Value': ['count',
                        'sum',
                        'mean',
                        'median'],
              'RegulatedEntityName': 'nunique'}).reset_index()
    donors_summary = ['Donor Name',
                      'Donation Type',
                      'No of Donations',
                      'Total Value',
                      'Average Donation',
                      'Median Donation',
                      'Regulated Entities']
    donors_summary['Total Value'] = (
        to_numeric(donors_summary['Total Value'], errors='coerce')
    )
    donors_summary['Regulated Entities'] = (
        to_numeric(donors_summary['Regulated Entities'], errors='coerce')
    )
    donors_summary['Avg Value per Entity'] = (
        donors_summary['Total Value'] / donors_summary['Regulated Entities']
        )
    donors_summary['Avg Donations per Entity'] = (
        donors_summary['No of Donations'] /
        donors_summary['Regulated Entities']
    )
    donors_entity_summary = cleaned_d_df.groupby(['DonorName'])\
        .agg({'Value': ['count',
                        'sum',
                        'mean',
                        'median'],
              'RegulatedEntityName': 'nunique'}).reset_index()

    # Ensure aggregates are numeric
    donors_entity_summary = ['RegulatedEntityName',
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
        donors_entity_summary[col] = (
             to_numeric(donors_entity_summary[col], errors='coerce')
        )
    donors_entity_summary = ['Regulated Entity',
                             'No of Donations',
                             'Total Value',
                             'Average Donation',
                             'Median Donation',
                             'Regulated Entities']
    donors_entity_summary['Avg Value per Entity'] = (
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
                'Avg Value per Entity']:
        donors_entity_summary[col] = (
            to_numeric(donors_entity_summary[col], errors='coerce')
        )
        donors_entity_summary[col] = (
            donors_entity_summary[col]
            .apply(lambda x: f"£{format_number(x)}")
        )
    donors_entity_summary['Avg No. Donations Per Entity'] = (
        donors_entity_summary['Average Number Donations per Entity']
        .apply(lambda x: f"{x:.2f}")
    )
    # Apply formating to values
    donors = format_number(tstats['unique_donors'])
    donations = format_number(tstats['unique_donations'])
    totaldonations = format_number(tstats['total_value'])
    avg_donations = f"{tstats['mean_value']:.2f}"
    median_donation = format_number(tstats['median_value'])

    st.write("---")
    st.write("# Analysis of Political Donations by Donor")
    st.write("---")
    st.write("## Headline Figures")
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        st.write("* For this analysis, any donations made by Political Parties"
                 " have been excluded. This is to focus on donations made by"
                 " individuals, companies, and other organisations.")
        st.write(f"* Between {min_date} and {max_date}, "
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
    st.write("---")
    left, mid = st.columns(2)
    with left:
        vis.plot_custom_bar_chart(
                                    df=cleaned_r_d_df,
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
                                    widget_key='avg_donation_donation_type',
                                    use_container_width=True
                                )
    with mid:
        st.write("<div style='text-align: center;'><b>Size of circles "
                 "represent the Average Value in GBP per entity.</b></div>",
                 unsafe_allow_html=True)

    # Display the styled st.dataframe
    st.write("---")
    st.dataframe(donors_summary.style.format(
        {"Total Value": "£{:.2f}",
         "Average Donation": "£{:.2f}",
         "Median Donation": "£{:.2f}",
         "Avg Value per Entity": "£{:.2f}"}))


    st.write("---")
