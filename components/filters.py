def filter_by_date(df, start_date, end_date, date_column="ReceivedDate"):
    """Filter the DataFrame by a given date range."""
    return df[(df[date_column] >= start_date) & (df[date_column] <= end_date)]


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
            df = df[df[column] == value] if value else df

    return df
