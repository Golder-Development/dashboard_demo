import streamlit as st
import datetime as dt
from data.data_loader import load_cleaned_data
from components.filters import filter_by_date, filter_by_entity, filter_by_donation_type
from components.calculations import get_filtered_data, compute_summary_statistics
from components.Visualisations import display_donation_trends

def cash_donations_page():
    """Displays the Cash Donations page in Streamlit."""
    
    # Load dataset
    cleaned_df = load_cleaned_data()
    if cleaned_df is None:
        st.error("No data found. Please upload a dataset.")
        return

    # Date range selection
    min_date, max_date = cleaned_df["ReceivedDate"].min().date(), cleaned_df["ReceivedDate"].max().date()
    start_date, end_date = st.slider("Select Date Range", min_value=min_date, max_value=max_date, value=(min_date, max_date), format="YYYY-MM-DD")
    
    # Convert selected dates to datetime
    start_date, end_date = dt.datetime.combine(start_date, dt.datetime.min.time()), dt.datetime.combine(end_date, dt.datetime.max.time())

    # Entity selection
    entity_mapping = dict(zip(cleaned_df["RegulatedEntityName"], cleaned_df["RegulatedEntityId"]))
    selected_entity_name = st.selectbox("Filter by Regulated Entity", ["All"] + sorted(entity_mapping.keys()))
    selected_entity_id = entity_mapping.get(selected_entity_name, None)

    # Apply filters
    filtered_df = get_filtered_data(cleaned_df, selected_entity_id, start_date, end_date)

    # Compute Statistics
    stats = compute_summary_statistics(filtered_df)

    # Display results
    st.write(f"## Summary Statistics for {selected_entity_name}")
    st.metric(label="Total Donations", value=f"£{stats['total_value']:,}")
    st.metric(label="Mean Donation Value", value=f"£{stats['mean_value']:.2f}")
    st.metric(label="Total Donors", value=f"{stats['num_donors']:,}")
    
    # Display visualizations
    st.write("## Donation Trends")
    display_donation_trends(filtered_df)