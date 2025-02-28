import pandas as pd
import streamlit as st


def filter_data(df, apply_date_filter=True, apply_entity_filter=True):
    """
    Filters the dataset based on user-selected filters for Regulated Entity and Date Range.

    Parameters:
    - df (pd.DataFrame): The dataset to filter.
    - apply_date_filter (bool): Whether to apply the date range filter.
    - apply_entity_filter (bool): Whether to apply the regulated entity filter.

    Returns:
    - pd.DataFrame: The filtered dataset.
    """

    # Convert ReceivedDate to datetime (coerce errors to NaT)
    df["ReceivedDate"] = pd.to_datetime(df["ReceivedDate"], errors="coerce")

    # --- Date Range Filter ---
    if apply_date_filter:
        # Get min and max dates from the dataset
        min_date = df["ReceivedDate"].min()
        max_date = df["ReceivedDate"].max()

        # Date range slider
        start_date, end_date = st.slider(
            "Select Date Range",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="YYYY-MM-DD"
        )

        # Apply date range filter
        date_filter = (df["ReceivedDate"] >= start_date) & (df["ReceivedDate"] <= end_date)
        df = df[date_filter]

    # --- Regulated Entity Filter ---
    if apply_entity_filter:
        # Create a mapping of RegulatedEntityName -> RegulatedEntityId
        entity_mapping = dict(zip(df["RegulatedEntityName"], df["RegulatedEntityId"]))

        # Add "All" as an option and create a dropdown for Regulated Entity
        selected_entity_name = st.selectbox("Filter by Regulated Entity", ["All"] + sorted(entity_mapping.keys()))

        # Get the corresponding ID for filtering
        selected_entity_id = entity_mapping.get(selected_entity_name, None)

        # Apply entity filter
        if selected_entity_id:
            df = df[df["RegulatedEntityId"] == selected_entity_id]

    return df
