import pandas as pd
import streamlit as st
from filters import filter_by_date, filter_by_entity, filter_by_donation_type


def get_filtered_data(df, entity_id, start_date, end_date):
    """Apply all necessary filters and return filtered DataFrame."""
    df = filter_by_date(df, start_date, end_date)
    df = filter_by_donation_type(df)
    df = filter_by_entity(df, entity_id)
    return df


def compute_summary_statistics(df):
    """Compute key statistics like total donations, mean, std, etc."""
    return {
        "total_value": df["Value"].sum(),
        "mean_value": df["Value"].mean(),
        "num_donations": len(df),
        "num_donors": df["DonorId"].nunique(),
    }


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


# Convert placeholder date to datetime once
PLACEHOLDER_DATE = pd.Timestamp("1900-01-01 00:00:00")
PLACEHOLDER_ID = 1000001


def count_unique_donors(df, donation_type, filters=None):
    """Counts unique donors based on a specific DonationType."""
    df = apply_filters(df, filters)
    return df[df["DonationType"].eq(donation_type)]["DonorId"].nunique()


def count_missing_values(df, column, missing_value, filters=None):
    """Counts donations where a specific column has a given missing value."""
    df = apply_filters(df, filters)
    return df[df[column].eq(missing_value)].shape[0]


def count_null_values(df, column, filters=None):
    """Counts donations where a specific column has null (NaN) values."""
    df = apply_filters(df, filters)
    return df[column].isna().sum()


# Specific functions using the generic ones
def get_impermissible_donors_ct(df, filters=None):
    return count_unique_donors(df, "Impermissible Donor", filters)


def get_unidentified_donors_ct(df, filters=None):
    return count_unique_donors(df, "Unidentified Donor", filters)


def get_blank_received_date_ct(df, filters=None):
    return count_missing_values(df, "ReceivedDate",
                                PLACEHOLDER_DATE,
                                filters)


def get_blank_regulated_entity_id_ct(df, filters=None):
    return count_missing_values(df, "RegulatedEntityId",
                                PLACEHOLDER_ID,
                                filters)


def get_blank_donor_id_ct(df, filters=None):
    return count_missing_values(df, "DonorId", PLACEHOLDER_ID, filters)


def get_blank_donor_name_ct(df, filters=None):
    return count_null_values(df, "DonorName", filters)


def get_dubious_donors(df, filters=None):
    dubious_conditions = (
        (df["DonationType"].isin([
            "Impermissible Donor", "Unidentified Donor",
            "Total value of donations not reported individually",
            "Aggregated Donation"
        ])) |
        (df["NatureOfDonation"] == "Aggregated Donation") |
        (df["IsAggregation"] == "True") |
        (df["DonorId"] == PLACEHOLDER_ID) |
        (df["DonorName"] == 'Unidentified Donor')
    )
    return apply_filters(df[dubious_conditions], filters)


def get_dubious_donors_ct(df, filters=None):
    """Calculates total dubious donors (impermissible + missing ID/name)."""
    return get_dubious_donors(df, filters)["EventCount"].sum()


def get_dubious_donors_value(df, filters=None):
    """Calculates total dubious donors (impermissible + missing ID/name)."""
    return get_dubious_donors(df, filters)["Value"].sum()


def get_dubious_donations(df, filters=None):
    dubious_conditions = (
        (df["DonationType"].isin([
            "Impermissible Donor", "Unidentified Donor",
            "Total value of donations not reported individually",
            "Aggregated Donation"
        ])) |
        (df["DonationAction"] != "Accepted") |
        (df["NatureOfDonation"] == "Aggregated Donation") |
        (df["IsAggregation"] == "True") |
        (df["ReceivedDate"] == PLACEHOLDER_DATE) |
        (df["RegulatedEntityId"] == PLACEHOLDER_ID) |
        (df["RegulatedEntityName"] == 'Unidentified Entity') |
        (df["DonorId"] == PLACEHOLDER_ID) |
        (df["DonorName"] == 'Unidentified Donor')
    )
    return apply_filters(df[dubious_conditions], filters)


def get_dubious_donation_actions(df, filters=None):
    return get_dubious_donations(df, filters)["EventCount"].sum()


def get_dubious_donation_value(df, filters=None):
    return get_dubious_donations(df, filters)["Value"].sum()


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
    df = df[df["ReceivedDate"] != pd.to_datetime(PLACEHOLDER_DATE)]
    return df["ReceivedDate"].min()


def get_maxdate(df, filters=None):
    """Most recent date from data subset"""
    df = apply_filters(df, filters)
    return df["ReceivedDate"].max()


def display_thresholds_table():
    """Creates and displays a table showing the threshold logic."""
    # Convert the dictionary into a DataFrame
    thresholds_df = pd.DataFrame(list(st.session_state.g_thresholds.items()),
                                 columns=["Donation Event Threshold",
                                          "Entity Category"])
    # format the table change Donation event Threshold column to Integer and
    # add bold to header
    thresholds_df = thresholds_df.style.format(
        {"Donation Event Threshold": "{:.0f}"}
    ).set_table_styles(
        [{'selector': 'th', 'props': [('font-size', '1.2em'),
                                      ('text-align', 'center')]}]
    )
    st.write("### Threshold Logic Table")
    # Static table (can use `st.dataframe()` for interactive table)
    st.table(thresholds_df)


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
    df = df[df["ReceivedDate"] != pd.to_datetime(PLACEHOLDER_DATE)]
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
    """Counts donations are aggregated donations"""
    df = apply_filters(df, filters)
    return df["IsAnAggregate"]["EventCount"].sum()


def get_donation_isanaggregate_value(df, filters=None):
    """Calculates the total value of all aggregated donations."""
    df = apply_filters(df, filters)
    return df.groupby("IsAnAggregate")["Value"].sum()


def get_top_entity_by_value(df, filters=None):
    """
    Returns the name and value of the regulated entity with the
    greatest value of donations.

    Parameters:
        df (pd.DataFrame): The dataset.
        filters (dict, optional): Dictionary where keys are column names
        and values are filter conditions.

    Returns:
        tuple: (RegulatedEntityName, Value)
    """
    df = apply_filters(df, filters)
    top_entity = df.groupby("RegulatedEntityName")["Value"].sum().idxmax()
    top_value = df.groupby("RegulatedEntityName")["Value"].sum().max()
    return top_entity, top_value


def get_top_entity_by_donations(df, filters=None):
    """
    Returns the name and value of the regulated entity with the
    greatest number of donations.

    Parameters:
        df (pd.DataFrame): The dataset.
        filters (dict, optional): Dictionary where keys are column names
        and values are filter conditions.

    Returns:
        tuple: (RegulatedEntityName, Value)
    """
    df = apply_filters(df, filters)
    top_entity = df.groupby("RegulatedEntityName")["EventCount"].sum().idxmax()
    top_value = df.groupby("RegulatedEntityName")["EventCount"].sum().max()
    return top_entity, top_value


def get_top_donType_by_don(df, filters=None):
    """
    Returns the name and value of the regulated entity with the greatest
    number of donations.

    Parameters:
        df (pd.DataFrame): The dataset.
        filters (dict, optional): Dictionary where keys are column names and
        values are filter conditions.

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


def get_median_donation(df, filters=None):
    """Calculates the median donation value."""
    df = apply_filters(df, filters)
    return df["Value"].median()


def get_top_donors(df, sort_col, exclude_single_donation=False):
    """Returns top 5 donors sorted by a specific column."""
    if exclude_single_donation:
        df = df[df["No of Donations"] > 1]
    return df.sort_values(sort_col, ascending=False)[[
        "Donor Name", "Regulated Entities", "Avg No. Donations Per Entity",
        "No of Donations", "Total Donations £", "Avg Donations",
        "Median Donations", "Avg Value Per Entity"
    ]].head(5)


def calculate_percentage(numerator, denominator):
    """ Calculate the percentage of a numerator to a denominator """
    return (numerator / denominator) * 100 if denominator > 0 else 0


def get_avg_donations_per_entity(df, filters=None):
    """Calculates the average number of donations per entity."""
    return df.groupby('RegulatedEntityId').size().mean()


def get_avg_value_per_entity(df, filters=None):
    """Calculates the average value of donations per entity."""
    return df.groupby('RegulatedEntityId')['Value'].mean().mean()


def get_avg_donors_per_entity(df, filters=None):
    """Calculates the average number of donors per entity."""
    return df.groupby('RegulatedEntityId')['DonorId'].nunique().mean()


def get_donors_stdev(df, filters=None):
    """Calculates the standard deviation of donors per entity."""
    return df.groupby('RegulatedEntityId').size().std()


def get_value_stdev(df, filters=None):
    """Calculates the standard deviation of value per entity."""
    return df.groupby('RegulatedEntityId')['Value'].mean().std()


def get_noofdonors_per_ent_stdev(df, filters=None):
    """Calculates the standard deviation of donors per entity."""
    return df.groupby('RegulatedEntityId')['DonorId'].nunique().std()


# Function to calculate key values
def get_metrics(df, filters):
    return {
        "unique_reg_entities": get_regentity_ct(df, filters),
        "unique_donors": get_donors_ct(df, filters),
        "unique_donations": get_donations_ct(df, filters),
        "total_value": get_value_total(df, filters),
        "mean_value": get_value_mean(df, filters),
        "avg_donations_per_entity": get_avg_donations_per_entity(df, filters),
        "avg_value_per_entity": get_avg_value_per_entity(df, filters),
        "avg_donors_per_entity": get_avg_donors_per_entity(df, filters),
        "donors_stdev": get_donors_stdev(df, filters),
        "value_stdev": get_value_stdev(df, filters),
        "noofdonors_per_ent_stdev": get_noofdonors_per_ent_stdev(df, filters)
    }
