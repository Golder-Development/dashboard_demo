def apply_filters(df, filters=None):
    """
    Apply filtering conditions to the DataFrame.

    Parameters:
        df (pd.DataFrame): The dataset.
        filters (dict, optional): Dictionary where keys are column names
        and values are filter conditions.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    if filters:
        for column, value in filters.items():
            df = df[df[column] == value]
    return df


def get_impermissible_donors_ct(df, filters=None):
    """Counts unique donors labeled as 'Impermissible Donor'."""
    df = apply_filters(df, filters)
    return df[df["DonationType"] == "Impermissible Donor"]["DonorId"].nunique()


def get_dubious_donation_actions_ct(df, filters=None):
    """Counts the number of unique actions marked as dubious."""
    df = apply_filters(df, filters)
    return df[df["DonationAction"].notnull()].index.nunique()


def get_blank_received_date_ct(df, filters=None):
    """Counts donations that have a missing received date."""
    df = apply_filters(df, filters)
    return df[df["ReceivedDate"] == '1900-01-01 00:00:00'].index.nunique()


def get_blank_regulated_entity_id_ct(df, filters=None):
    """Counts donations with missing regulated entity ID."""
    df = apply_filters(df, filters)
    return df[df["RegulatedEntityId"].isnull()].index.nunique()


def get_blank_donor_id_ct(df, filters=None):
    """Counts donations with missing donor ID."""
    df = apply_filters(df, filters)
    return df[df["DonorId"].isnull()].index.nunique()


def get_blank_donor_name_ct(df, filters=None):
    """Counts donations with missing donor name."""
    df = apply_filters(df, filters)
    return df[df["DonorName"].isnull()].index.nunique()


def get_dubious_donors_ct(df, filters=None):
    """Calculates total dubious donors (impermissible + missing ID/name)."""
    df = apply_filters(df, filters)
    return get_impermissible_donors_ct(df) + get_blank_donor_id_ct(df) + get_blank_donor_name_ct(df)


def get_dubious_donation_actions(df, filters=None):
    """Calculates total dubious donation actions."""
    df = apply_filters(df, filters)
    return get_dubious_donation_actions_ct(df) + get_blank_received_date_ct(df) + get_blank_regulated_entity_id_ct(df)


def get_total_value_dubious_donations(df, filters=None):
    """Calculates the total value of all dubious donations."""
    df = apply_filters(df, filters)
    return df[
        (df["DonationType"] == "Impermissible Donor") |
        (df["DonationAction"].notnull()) |
        (df["ReceivedDate"].isnull()) |
        (df["RegulatedEntityId"].isnull()) |
        (df["DonorId"].isnull()) |
        (df["DonorName"].isnull())
    ]["Value"].sum()


def get_donors_ct(df, filters=None):
    """Counts unique donors"""
    df = apply_filters(df, filters)
    return df["DonorId"].nunique()


def get_value_total(df, filters=None):
    """Sums total value of donations"""
    df = apply_filters(df, filters)
    return df['Value'].sum()


def get_value_mean(df, filters=None):
    """Mean of value of donations"""
    df = apply_filters(df, filters)
    return df['Value'].mean()


def get_donations_ct(df, filters=None):
    """Mean of value of donations"""
    df = apply_filters(df, filters)
    return df['ECRef'].nunique()


def get_regentity_ct(df, filters=None):
    """Mean of value of donations"""
    df = apply_filters(df, filters)
    return df["RegulatedEntityName"].nunique()


def get_mindate(df, filters=None):
    import pandas as pd
    """Mean of value of donations"""
    df = apply_filters(df, filters)
    df = df[df["ReceivedDate"] != pd.to_datetime('1900-01-01 00:00:00')]
    return df["ReceivedDate"].min()


def get_maxdate(df, filters=None):
    """Mean of value of donations"""
    df = apply_filters(df, filters)
    return df["ReceivedDate"].max()


# Define a function to set the category
def RegulatedEntityGroup(RegulatedEntityNameVar):
    import streamlit as st
    RegulatedEntity_df = st.session_state.get("data_party_sum", None)
    # Define Dictionary with grouped values
    RegEntityGrouping = {0:'No Relevant Donations', 1: 'Single Donation Entity', 50: 'Very Small Entity', 100: 'Small Entity', 1000: 'Medium Entity', float('inf'): RegulatedEntityNameVar}
    # Select all relevant donation events for specified Entity Name
    RE_Events = RegulatedEntity_df[RegulatedEntity_df.index == RegulatedEntityNameVar]
    # Compare Count of events to rangelimits in Dictionary and return Category
    for rangeLimit, category in RegEntityGrouping.items():
        if RE_Events.DonationEvents.agg(sum) <= rangeLimit:
            return category
