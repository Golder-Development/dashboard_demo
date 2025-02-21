import pandas as pd

def filter_by_date(df, start_date, end_date, date_column="ReceivedDate"):
    """Filter the DataFrame by a given date range."""
    return df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]

def filter_by_entity(df, entity_id):
    """Filter DataFrame by selected regulated entity."""
    return df[df["RegulatedEntityId"] == entity_id] if entity_id else df

def filter_by_donation_type(df, donation_type="Cash"):
    """Filter DataFrame by donation type."""
    return df[df["DonationType"] == donation_type]
