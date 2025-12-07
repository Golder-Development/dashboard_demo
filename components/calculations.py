import pandas as pd
import streamlit as st
from components.filters import apply_filters
from utils.logger import logger


# Convert placeholder date to datetime once
PLACEHOLDER_DATE = st.session_state.get("PLACEHOLDER_DATE")
PLACEHOLDER_ID = st.session_state.get("PLACEHOLDER_ID")


def count_unique_records(df, column, filters=None):
    """Counts unique donors based on a specific DonationType."""
    df = apply_filters(df, filters)
    return df[column].nunique()


def count_missing_values(df, column, missing_value, filters=None):
    """Counts donations where a specific column has a given missing value."""
    df = apply_filters(df, filters)
    return df[df[column].eq(missing_value)].shape[0]


def count_null_values(df, column, filters=None):
    """Counts donations where a specific column has null (NaN) values."""
    df = apply_filters(df, filters)
    return df[column].isna().sum()


def count_records_values(df, column, filters=None):
    """Counts donations where a specific column has null (NaN) values."""
    df = apply_filters(df, filters)
    return df[column]["EventCount"].sum()


# Specific functions using the generic ones
def count_unique_donors(df, filters=None):
    """Counts unique donors based on a specific DonationType."""
    return count_unique_records(df, "DonorId", filters)


def get_impermissible_donors_ct(df, filters=None):
    return count_unique_donors(df, "Impermissible Donor", filters)


def get_unidentified_donors_ct(df, filters=None):
    return count_unique_donors(df, "Unidentified Donor", filters)


def get_blank_received_date_ct(df, filters=None):
    return count_missing_values(df, "ReceivedDate", PLACEHOLDER_DATE, filters)


def get_blank_regulated_entity_id_ct(df, filters=None):
    return count_missing_values(df, "PartyId", PLACEHOLDER_ID,
                                filters)


def get_blank_donor_id_ct(df, filters=None):
    return count_missing_values(df, "DonorId", PLACEHOLDER_ID, filters)


def get_blank_donor_name_ct(df, filters=None):
    return count_null_values(df, "DonorName", filters)


def get_dubious_donors(df, filters=None):
    filters = st.session_state["filter_def"].get("DubiousDonor_ftr")
    return apply_filters(df, filters)


def get_dubious_donors_ct(df, filters=None):
    """Calculates total dubious donors (impermissible + missing ID/name)."""
    return get_dubious_donors(df, filters)["EventCount"].sum()


def get_dubious_donors_value(df, filters=None):
    """Calculates total dubious donors (impermissible + missing ID/name)."""
    return get_dubious_donors(df, filters)["Value"].sum()


def get_dubious_donations(df, filters=None):
    filters = st.session_state["filter_def"].get("DubiousDonor_ftr")
    return apply_filters(df, filters)


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
    return df["Value"].sum()


def get_value_mean(df, filters=None):
    """Mean of value of donations"""
    df = apply_filters(df, filters)
    return df["Value"].mean()


def get_donations_ct(df, filters=None):
    """Count of Donations"""
    df = apply_filters(df, filters)
    return df["EventCount"].sum()


def get_regentity_ct(df, filters=None):
    """Count of Regulated Entities"""
    df = apply_filters(df, filters)
    return df["PartyName"].nunique()


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
    thresholds = st.session_state.get("thresholds", {})
    thresholds_df = pd.DataFrame(
        list(thresholds.items()),
        columns=["Donation Event Threshold", "Entity Category"],
    )

    st.write("### Threshold Logic Table")
    st.table(thresholds_df)


def get_returned_donations_ct(df, filters=None):
    """Counts donations that have been returned."""
    retfilters = st.session_state["filter_def"].get("ReturnedDonation_ftr")
    df = apply_filters(df, retfilters)
    return df["EventCount"].sum()


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


def get_top_or_bottom_entity_by_column(df,
                                       column,
                                       value_column,
                                       top=True,
                                       filters=None):
    """
    Returns the name and value of the entity with the
    greatest or smallest value
    in the specified column.

    Parameters:
        df (pd.DataFrame): The dataset.
        column (str): The column to group by.
        value_column (str): The column to sum for the value.
        top (bool, optional): If True, returns the top entity.
        If False, returns the bottom entity.
        filters (dict, optional): Dictionary where keys are column names
        and values are filter conditions.

    Returns:
        tuple: (EntityName, Value)
    """
    df = apply_filters(df, filters)
    grouped = df.groupby(column)[value_column].sum()
    if top:
        entity = grouped.idxmax()
        value = grouped.max()
    else:
        entity = grouped.idxmin()
        value = grouped.min()
    return entity, value


def format_number(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:,.1f}M"
    elif value >= 10_000:
        return f"{value / 1_000:,.1f}k"
    else:
        return f"{value:,.0f}"


def get_median_donation(df, filters=None):
    """Calculates the median donation value."""
    df = apply_filters(df, filters)
    return df["Value"].median()


def calculate_percentage(numerator=0, denominator=0):
    """Calculate the percentage of a numerator to a denominator"""
    try:
        numerator = float(numerator)
        denominator = float(denominator)
    except (ValueError, TypeError):
        return 0
    return (numerator / denominator) * 100 if denominator > 0 else 0


def get_avg_donations_per_entity(df, filters=None):
    """Calculates the average number of donations per entity."""
    df = apply_filters(df, filters)
    return df.groupby("PartyId").size().mean()


def get_avg_value_per_entity(df, filters=None):
    """Calculates the average value of donations per entity."""
    df = apply_filters(df, filters)
    return df.groupby("PartyId")["Value"].mean().mean()


def get_avg_donors_per_entity(df, filters=None):
    """Calculates the average number of donors per entity."""
    df = apply_filters(df, filters)
    return df.groupby("PartyId")["DonorId"].nunique().mean()


def get_donors_stdev(df, filters=None):
    """Calculates the standard deviation of donors per entity."""
    df = apply_filters(df, filters)
    return df.groupby("PartyId").size().std()


def get_value_stdev(df, filters=None):
    """Calculates the standard deviation of value per entity."""
    df = apply_filters(df, filters)
    return df.groupby("PartyId")["Value"].mean().std()


def get_noofdonors_per_ent_stdev(df, filters=None):
    """Calculates the standard deviation of donors per entity."""
    df = apply_filters(df, filters)
    return df.groupby("PartyId")["DonorId"].nunique().std()


# Function to calculate key values
def compute_summary_statistics(df, filters):
    """Compute key statistics like total donations, mean, std, etc."""
    try:
        df = apply_filters(df, filters)
    except Exception as e:
        logger.error(f"Error applying filters: {e}")
        return {
            "unique_reg_entities": 0,
            "unique_donors": 0,
            "unique_donations": 0,
            "total_value": 0.0,
            "mean_value": 0.0,
            "avg_donations_per_entity": 0.0,
            "avg_value_per_entity": 0.0,
            "avg_donors_per_entity": 0.0,
            "donors_stdev": 0.0,
            "value_stdev": 0.0,
            "noofdonors_per_ent_stdev": 0.0,
            "most_common_entity": ("", 0.0),
            "most_valuable_entity": ("", 0.0),
            "least_common_entity": ("", 0.0),
            "least_valuable_entity": ("", 0.0),
            "most_common_donor": ("", 0.0),
            "most_valuable_donor": ("", 0.0)
            }

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Filtered result is not a DataFrame")

    if df is None or df.empty:
        return {
            "unique_reg_entities": 0,
            "unique_donors": 0,
            "unique_donations": 0,
            "total_value": 0.0,
            "mean_value": 0.0,
            "avg_donations_per_entity": 0.0,
            "avg_value_per_entity": 0.0,
            "avg_donors_per_entity": 0.0,
            "donors_stdev": 0.0,
            "value_stdev": 0.0,
            "noofdonors_per_ent_stdev": 0.0,
            "most_common_entity": ("", 0.0),
            "most_valuable_entity": ("", 0.0),
            "least_common_entity": ("", 0.0),
            "least_valuable_entity": ("", 0.0),
            "most_common_donor": ("", 0.0),
            "most_valuable_donor": ("", 0.0),
        }

    regentity_ct = get_regentity_ct(df, filters)
    donors_ct = get_donors_ct(df, filters)
    donations_ct = get_donations_ct(df, filters)
    value_total = get_value_total(df, filters)
    value_mean = get_value_mean(df, filters)
    avg_donations_per_entity = get_avg_donations_per_entity(df, filters)
    avg_value_per_entity = get_avg_value_per_entity(df, filters)
    avg_donors_per_entity = get_avg_donors_per_entity(df, filters)
    donors_stdev = get_donors_stdev(df, filters)
    value_stdev = get_value_stdev(df, filters)
    noofdonors_per_ent_stdev = get_noofdonors_per_ent_stdev(df, filters)
    most_common_entity = get_top_or_bottom_entity_by_column(df=df,
                                                            column="PartyName",
                                                            value_column="EventCount",
                                                            top=True,
                                                            filters=filters)
    most_valuable_entity = get_top_or_bottom_entity_by_column(df=df,
                                                              column="PartyName",
                                                              value_column="Value",
                                                              top=True,
                                                              filters=filters)
    least_common_entity = get_top_or_bottom_entity_by_column(df=df,
                                                             column="PartyName",
                                                             value_column="EventCount",
                                                             top=False,
                                                             filters=filters)
    least_valuable_entity = get_top_or_bottom_entity_by_column(df=df,
                                                               column="PartyName",
                                                               value_column="Value",
                                                               top=False,
                                                               filters=filters)
    most_common_donor = get_top_or_bottom_entity_by_column(df=df,
                                                           column="DonorName",
                                                           value_column="EventCount",
                                                           top=True,
                                                           filters=filters)
    most_valuable_donor = get_top_or_bottom_entity_by_column(df=df,
                                                             column="DonorName",
                                                             value_column="Value",
                                                             top=True,
                                                             filters=filters)
    return {
        "unique_reg_entities": regentity_ct,
        "unique_donors": donors_ct,
        "unique_donations": donations_ct,
        "total_value": value_total,
        "mean_value": value_mean,
        "avg_donations_per_entity": avg_donations_per_entity,
        "avg_value_per_entity": avg_value_per_entity,
        "avg_donors_per_entity": avg_donors_per_entity,
        "donors_stdev": donors_stdev,
        "value_stdev": value_stdev,
        "noofdonors_per_ent_stdev": noofdonors_per_ent_stdev,
        "most_common_entity": most_common_entity,
        "most_valuable_entity": most_valuable_entity,
        "least_common_entity": least_common_entity,
        "least_valuable_entity": least_valuable_entity,
        "most_common_donor": most_common_donor,
        "most_valuable_donor": most_valuable_donor,
    }


def determine_groups_optimized(df, entity, measure, thresholds_dict, exception_dict=None):
    """
    Optimized version of group determination.

    Parameters:
        df (pd.DataFrame): DataFrame containing entity and measure columns.
        entity (str): Column name representing the entity.
        measure (str): Column name representing the numeric measure.
        thresholds_dict (dict): Dictionary mapping (low, high)
        tuples to group labels.
        exception_dict(dict): Dictionary mapping entity values to exception groups.
    Returns:
        pd.Series: A Series containing assigned groups for each row.
    """
    # Step 1: Compute total measure per entity
    entity_totals = df.groupby(entity, as_index=False)[measure].sum()
    entity_totals.rename(columns={measure: "total_measure"}, inplace=True)

    # Step 2: Assign groups based on thresholds or (exceptions)
    # if exception_dict is provided, use assign_group_with_exceptions
    # other wise use assign_group
    if exception_dict:
        #logger to show exception dict being used
        logger.debug(f"Group assignment with exceptions: {exception_dict}")
        entity_totals["group"] = entity_totals.apply(
            lambda row: assign_group_with_exceptions(
                row,
                thresholds_dict,
                row[entity],
                exception_dict
            ), axis=1
        )
    else:
        entity_totals["group"] = entity_totals.apply(
                                    lambda row: assign_group(row["total_measure"],
                                                            thresholds_dict,
                                                            row[entity]), axis=1
            )

    # Step 3: Merge back into the original DataFrame
    df = df.merge(entity_totals[[entity, "group"]], on=entity, how="left")
    logger.debug(f"Group assignment: {df['group'].value_counts()}")
    logger.debug(f"Group assignment: {entity_totals['group'].value_counts()}")

    # Step 4: Validate row count consistency
    if len(df) != len(df):
        st.error(f"Length mismatch: original {len(df)}, merged {len(df)}")
        logger.error(f"Length mismatch: original {len(df)}, merged {len(df)}")
        df.drop_duplicates(inplace=True)

        if len(df) != len(df):
            st.error(f"Mismatch after deduplication: original {len(df)},"
                     f" merged {len(df)}")
            logger.critical(f"Mismatch after deduplication: original"
                            f" {len(df)}, merged {len(df)}")
            return None

    # Step 5: Return the group column
    return df["group"]


def assign_group(total, thresholds_dict, entity_value):
    """
    Assigns a group based on thresholds.
    If above the max threshold, returns the entity name.
    """
    for (low, high), group_name in thresholds_dict.items():
        if low <= total <= high:
            return group_name
    return entity_value  # Assign entity name if above max threshold

def assign_group_with_exceptions(row,
                                 thresholds_dict,
                                 entity_value,
                                 exception_list):
    """
    Assigns a group based on thresholds and exceptions.  
    """
    # Check if this entity is in the exception list first
    if exception_list and entity_value in exception_list:
        return entity_value
    
    # Otherwise, use threshold-based grouping
    return assign_group(row["total_measure"], thresholds_dict, entity_value)
    


def calculate_agg_by_variable(
    datafile=st.session_state.get("data_clean"),
    groupby_variable="PartyName",
    groupby_name="Party",
    agg_variable="Value",
    agg_type="mean",
    agg_name="AverageDonation"
        ):
    """
    Calculate aggregate measures by group.

    Parameters:
    datafile (pd.DataFrame): DataFrame containing entity and measure columns.
    groupby_variable (str): Column name representing the entity.
    agg_variable (str): Column name representing the numeric measure.
    agg_type (str): Aggregation function to use (e.g., 'mean', 'sum').
    agg_name (str): Name for the aggregated measure.

    Returns:
    pd.DataFrame: DataFrame containing aggregated measures by group.
    """
    if datafile is None:
        return pd.DataFrame()

    # Calculate aggregate measures by allocated entity
    if agg_type == "mean":
        agg_df = datafile.groupby(groupby_variable,
                                  as_index=False)[agg_variable].mean()
    elif agg_type == "sum":
        agg_df = datafile.groupby(groupby_variable,
                                  as_index=False)[agg_variable].sum()
    elif agg_type == "count":
        agg_df = datafile.groupby(groupby_variable,
                                  as_index=False)[agg_variable].count()
    elif agg_type == "nunique":
        agg_df = datafile.groupby(groupby_variable,
                                  as_index=False)[agg_variable].nunique()
    else:
        raise ValueError(f"Unsupported aggregation type: {agg_type}")

    agg_df.rename(columns={agg_variable: agg_name,
                           groupby_variable: groupby_name}, inplace=True)

    return agg_df
