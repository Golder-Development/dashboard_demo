import numpy as np
from utils.logger import logger
from utils.decorators import log_function_call  # Import decorator


def filter_by_date(df, start_date, end_date, date_column="ReceivedDate"):
    """Filter the DataFrame by a given date range."""
    return df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]


def apply_filters(df, providedfilters=None, logical_operator="or"):
    """
    Apply filtering conditions to the DataFrame.

    Parameters:
        df (pd.DataFrame): The dataset.
        providedfilters (dict, optional): Dictionary where keys
            are column names and values are filter conditions
            (single value or list).
        logical_operator (str, optional): Logical operator to combine
                                          conditions ("and" or "or").
                                          Default is "or".
    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    # If no filters provided, return original DataFrame
    if not providedfilters:
        return df

    conditions = []
    for column, value in providedfilters.items():
        if value is None or value == []:  # Skip empty filters
            continue
        if isinstance(value, (list, tuple, set)):
            conditions.append(df[column].isin(value))
        else:  # Single value filtering
            conditions.append(df[column] == value)

    if not conditions:  # If no valid filters, return the original DataFrame
        return df

    if logical_operator == "and":
        final_condition = np.logical_and.reduce(conditions)
    elif logical_operator == "or":
        final_condition = np.logical_or.reduce(conditions)
    elif logical_operator == "nor":
        final_condition = ~np.logical_or.reduce(conditions)
    elif logical_operator == "except":
        final_condition = ~np.logical_and.reduce(conditions)
    else:
        raise ValueError("logical_operator must be " " 'and', 'or', 'nor', or 'except'")

    return df[final_condition]
