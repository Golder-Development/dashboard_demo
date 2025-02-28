from utils.logger import logger, log_function_call


@log_function_call
def apply_filters(df, filters=None):
    """
    Apply filtering conditions to the DataFrame.
    """
    if filters:
        for column, value in filters.items():
            df = df[df[column] == value]
    return df


@log_function_call
def count_unique(df, column, filters=None):
    df = apply_filters(df, filters)
    return df[column].nunique()


@log_function_call
def count_occurrences(df, column, value, filters=None):
    df = apply_filters(df, filters)
    return df[df[column] == value]["EventCount"].sum()


@log_function_call
def sum_column(df, column, filters=None):
    df = apply_filters(df, filters)
    return df[column].sum()


@log_function_call
def get_impermissible_donors_ct(df, filters=None):
    return count_unique(df[df["DonationType"] == "Impermissible Donor"], "DonorId", filters)


@log_function_call
def get_unidentified_donors_ct(df, filters=None):
    return count_unique(df[df["DonationType"] == "Unidentified Donor"], "DonorId", filters)


@log_function_call
def get_blank_field_ct(df, column, missing_value, filters=None):
    df = apply_filters(df, filters)
    return df[df[column] == missing_value].index.nunique()


@log_function_call
def get_dubious_donations(df, filters=None):
    dubious_conditions = (
        (df["DonationType"].isin([
            "Impermissible Donor", "Unidentified Donor",
            "Total value of donations not reported individually", "Aggregated Donation"
        ])) | 
        (df["DonationAction"] != "Accepted") |
        (df["NatureOfDonation"] == "Aggregated Donation") |
        (df["IsAggregation"] == "True") |
        (df["ReceivedDate"] == '1900-01-01 00:00:00') |
        (df["RegulatedEntityId"] == "1000001") |
        (df["RegulatedEntityName"] == 'Unidentified Entity') |
        (df["DonorId"] == "1000001") |
        (df["DonorName"] == 'Unidentified Donor')
    )
    return apply_filters(df[dubious_conditions], filters)


@log_function_call
def get_dubious_donation_ct(df, filters=None):
    return get_dubious_donations(df, filters)["EventCount"].sum()


@log_function_call
def get_dubious_donation_value(df, filters=None):
    return get_dubious_donations(df, filters)["Value"].sum()


@log_function_call
def get_top_entity_by(df, metric, filters=None):
    df = apply_filters(df, filters)
    grouped = df.groupby("RegulatedEntityName")[metric].sum()
    top_entity = grouped.idxmax()
    top_value = grouped.max()
    return top_entity, top_value


@log_function_call
def get_top_donation_type(df, filters=None):
    return get_top_entity_by(df, "EventCount", filters)


@log_function_call
def format_number(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:,.1f}M"
    elif value >= 10_000:
        return f"{value / 1_000:,.1f}k"
    else:
        return f"{value:,.2f}"


@log_function_call
def get_metrics(df, filters=None):
    return {
        "unique_reg_entities": count_unique(df, "RegulatedEntityName", filters),
        "unique_donors": count_unique(df, "DonorId", filters),
        "unique_donations": sum_column(df, "EventCount", filters),
        "total_value": sum_column(df, "Value", filters),
        "mean_value": df["Value"].mean()
    }