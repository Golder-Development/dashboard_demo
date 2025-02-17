import pandas as pd
import streamlit as st


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

def get_unidentified_donors_ct(df, filters=None):
    """Counts unique donors labeled as 'Impermissible Donor'."""
    df = apply_filters(df, filters)
    return df[df["DonationType"] == "Unidentified Donor"]["DonorId"].nunique()


def get_dubious_donors_ct(df, filters=None):
    """Calculates total dubious donors (impermissible + missing ID/name)."""
    df = apply_filters(df, filters)
    return df[
        (df["DonationType"] == "Impermissible Donor") |
        (df["DonationType"] == "Unidentified Donor") |
        (df["DonationType"] == "Total value of donations not reported individually") |
        (df["NatureOfDonation"] == "Aggregated Donation") |
        (df["IsAggregation"] == "True") |
        (df["DonorId"].isnull()) |
        (df["DonorName"].isnull())
    ]["EventCount"].sum()


def get_dubious_donors_value(df, filters=None):
    """Calculates total dubious donors (impermissible + missing ID/name)."""
    df = apply_filters(df, filters)
    return df[
        (df["DonationType"] == "Impermissible Donor") |
        (df["DonationType"] == "Unidentified Donor") |
        (df["DonationType"] == "Total value of donations not reported individually") |
        (df["NatureOfDonation"] == "Aggregated Donation") |
        (df["IsAggregation"] == "True") |
        (df["DonorId"].isnull()) |
        (df["DonorName"].isnull())
    ]["Value"].sum()


def get_dubious_donation_actions(df, filters=None):
    """Calculates total dubious donation actions."""
    df = apply_filters(df, filters)
    return df[
        (df["DonationType"] == "Visit") |
        (df["DonationType"] == "Impermissible Donor") |
        (df["DonationType"] == "Unidentified Donor") |
        (df["DonationType"] == "Total value of donations not reported individually") |
        (df["NatureOfDonation"] == "Aggregated Donation") |
        (df["IsAggregation"] == "True") |
        (df["DonationAction"].notnull()) |
        (df["ReceivedDate"] == '1900-01-01 00:00:00') |
        (df["RegulatedEntityId"].isnull()) 
    ]["EventCount"].sum()


def get_dubious_donation_value(df, filters=None):
    """Calculates total value of dubious donation actions."""
    df = apply_filters(df, filters)
    return df[
        (df["DonationType"] == "Visit") |
        (df["DonationType"] == "Impermissible Donor") |
        (df["DonationType"] == "Unidentified Donor") |
        (df["DonationType"] == "Total value of donations not reported individually") |
        (df["NatureOfDonation"] == "Aggregated Donation") |
        (df["IsAggregation"] == "True") |
        (df["DonationAction"].notnull()) |
        (df["ReceivedDate"] == '1900-01-01 00:00:00') |
        (df["RegulatedEntityId"].isnull()) 
    ]["Value"].sum()


def get_total_value_dubious_donations(df, filters=None):
    """Calculates the total value of all dubious donations."""
    df = apply_filters(df, filters)
    return df[
        (df["DonationType"] == "Impermissible Donor") |
        (df["DonationType"] == "Unidentified Donor") |
        (df["DonationType"] == "Total value of donations not reported individually") |
        (df["DonationType"] == "Visit") |
        (df["DonationAction"].notnull()) |
        (df["NatureOfDonation"] == "Aggregated Donation") |
        (df["IsAggregation"] == "True") |
        (df["ReceivedDate"] == '1900-01-01 00:00:00') |
        (df["RegulatedEntityId"].isnull()) |
        (df["DonorId"].isnull()) |
        (df["DonorName"].isnull())
    ]["Value"].sum()


def get_total_ct_dubious_donations(df, filters=None):
    """Calculates the total value of all dubious donations."""
    df = apply_filters(df, filters)
    return df[
        (df["DonationType"] == "Impermissible Donor") |
        (df["DonationType"] == "Unidentified Donor") |
        (df["DonationType"] == "Total value of donations not reported individually") |
        (df["DonationType"] == "Visit") |
        (df["DonationAction"].notnull()) |
        (df["NatureOfDonation"] == "Aggregated Donation") |
        (df["IsAggregation"] == "True") |
        (df["ReceivedDate"] == '1900-01-01 00:00:00') |
        (df["RegulatedEntityId"].isnull()) |
        (df["DonorId"].isnull()) |
        (df["DonorName"].isnull())
    ]["EventCount"].sum()


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
    """Count of Donations"""
    df = apply_filters(df, filters)
    return df["EventCount"].sum()


def get_regentity_ct(df, filters=None):
    """Count of Regulated Entities"""
    df = apply_filters(df, filters)
    return df["RegulatedEntityName"].nunique()


def get_mindate(df, filters=None):
    """Earliest date from data subset"""
    df = apply_filters(df, filters)
    df = df[df["ReceivedDate"] != pd.to_datetime('1900-01-01 00:00:00')]
    return df["ReceivedDate"].min()


def get_maxdate(df, filters=None):
    """Most recent date from data subset"""
    df = apply_filters(df, filters)
    return df["ReceivedDate"].max()


def display_thresholds_table():
    """Creates and displays a table showing the threshold logic."""
    # Convert the dictionary into a DataFrame
    thresholds_df = pd.DataFrame(list(st.session_state.g_thresholds.items()), columns=["Donation Event Threshold", "Entity Category"])
    # format the table change Donation event Threshold column to Integer and add bold to header
    thresholds_df = thresholds_df.style.format({"Donation Event Threshold": "{:.0f}"}).set_table_styles([{
        'selector': 'th',
        'props': [('font-size', '1.2em'), ('text-align', 'center')]}])
    st.write("### Threshold Logic Table")
    st.table(thresholds_df)  # Static table (can use `st.dataframe()` for interactive table)


def get_returned_donations_ct(df, filters=None):
    """Counts donations that have been returned."""
    df = apply_filters(df, filters)
    return df[df["DonationAction"] == "Returned"]["EventCount"].sum()


def get_returned_donations_value(df, filters=None):
    """Calculates the total value of all returned donations."""
    df = apply_filters(df, filters)
    return df[df["DonationAction"] == "Returned"]["Value"].sum()


def get_datamindate():
    """Earliest date from full data"""
    df = st.session_state.get("data_clean", None)
    df = df[df["ReceivedDate"] != pd.to_datetime('1900-01-01 00:00:00')]
    return df["ReceivedDate"].min()


def get_datamaxdate():
    """Most recent date from full data"""
    df = st.session_state.get("data_clean", None)
    return df["ReceivedDate"].max()


def get_donationtype_ct(df, filters=None):
    """Counts donations of a specified DonationType."""
    filtered_df = apply_filters(df, filters)
    return len(filtered_df)  # Ensure this returns an integer


def get_donationtype_value(df, filters=None):
    """Calculates the total value of all returned donations."""
    df = apply_filters(df, filters)
    return df.groupby("DonationType")["Value"].sum()


def get_donation_isanaggregate_ct(df, filters=None):
    """Counts donations that have been returned."""
    df = apply_filters(df, filters)
    return df["IsAnAggregate"]["EventCount"].sum()


def get_donation_isanaggregate_value(df, filters=None):
    """Calculates the total value of all returned donations."""
    df = apply_filters(df, filters)
    return df.groupby("IsAnAggregate")["Value"].sum()


def get_top_entity_by_value(df, filters=None):
    """
    Returns the name and value of the regulated entity with the greatest value of donations.

    Parameters:
        df (pd.DataFrame): The dataset.
        filters (dict, optional): Dictionary where keys are column names and values are filter conditions.

    Returns:
        tuple: (RegulatedEntityName, Value)
    """
    df = apply_filters(df, filters)
    top_entity = df.groupby("RegulatedEntityName")["Value"].sum().idxmax()
    top_value = df.groupby("RegulatedEntityName")["Value"].sum().max()
    return top_entity, top_value


def get_top_entity_by_donations(df, filters=None):
    """
    Returns the name and value of the regulated entity with the greatest number of donations.

    Parameters:
        df (pd.DataFrame): The dataset.
        filters (dict, optional): Dictionary where keys are column names and values are filter conditions.

    Returns:
        tuple: (RegulatedEntityName, Value)
    """
    df = apply_filters(df, filters)
    top_entity = df.groupby("RegulatedEntityName")["EventCount"].sum().idxmax()
    top_value = df.groupby("RegulatedEntityName")["EventCount"].sum().max()
    return top_entity, top_value


def get_top_donationType_by_donations(df, filters=None):
    """
    Returns the name and value of the regulated entity with the greatest number of donations.

    Parameters:
        df (pd.DataFrame): The dataset.
        filters (dict, optional): Dictionary where keys are column names and values are filter conditions.

    Returns:
        tuple: (RegulatedEntityName, Value)
    """
    df = apply_filters(df, filters)
    top_entity = df.groupby("DonationType")["EventCount"].sum().idxmax()
    top_value = df.groupby("DonationType")["EventCount"].sum().max()
    return top_entity, top_value


def format_number(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:,.1f}M"
    elif value >= 10_000:
        return f"{value / 1_000:,.1f}k"
    else:
        return f"{value:,.2f}"