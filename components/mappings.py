"""
File to store all the mappings for the project
1. Mappings for the data cleansing
"""

import pandas as pd
from utils.logger import streamlit_logger as logger
from utils.logger import log_function_call  # Import decorator


def map_nature_of_donation(row):
    if pd.notna(row["NatureOfDonation"]):
        return row["NatureOfDonation"]
    if str(row["IsBequest"]).lower() == "true":
        return "IsABequest"
    if str(row["IsAggregation"]).lower() == "true":
        return "IsAggregatedDonation"
    if str(row["IsSponsorship"]).lower() == "true":
        return "IsSponsorship"
    if pd.notna(row["RegulatedDoneeType"]) and row["RegulatedDoneeType"] != "":
        return f"Donation to {row['RegulatedDoneeType']}"
    if pd.notna(row["RegulatedEntityType"]) and row["RegulatedEntityType"] != "":
        return f"Donation to {row['RegulatedEntityType']}"
    if pd.notna(row["DonationAction"]):
        return row["DonationAction"]
    if pd.notna(row["DonationType"]):
        return row["DonationType"]
    return "Other"
