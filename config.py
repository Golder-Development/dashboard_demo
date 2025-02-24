# config.py - Stores global constants

import os
import pandas as pd

# Base directory
BASE_DIR = os.path.dirname(__file__)

DIRECTORIES = {
    "data_dir": os.path.join(BASE_DIR, "data"),
    "output_dir": os.path.join(BASE_DIR, "output"),
    "logs_dir": os.path.join(BASE_DIR, "logs"),
    "reference_dir": os.path.join(BASE_DIR, "reference_files"),
    "components_dir": os.path.join(BASE_DIR, "components"),
    "app_pages_dir": os.path.join(BASE_DIR, "app_pages"),
    "utils_dir": os.path.join(BASE_DIR, "utils")
}

# File paths
FILENAMES = {
    "ec_donations_fname": "Donations_accepted_by_political_parties.csv",
    "donor_map_fname": "PoliticalDonorsDeDuped.csv",
    "politician_party_fname": "ListOfPoliticalPeople_Final.csv",
    "regentity_map_fname": "PoliticalEntityDeDuped.csv",
    "cleaned_data_fname": "cleaned_data.csv",
    "cleaned_donations_fname": "cleaned_donations.csv",
    "cleaned_donorlist_fname": "cleaned_donorlist.csv",
    "cleaned_regentity_fname": "cleaned_regentity.csv",
    "party_summary_fname": "party_summary.csv",
    "potential_donor_duplicates_fname": "potential_donor_duplicates.csv",
    "potential_regentity_duplicates_fname": "potential_regentity_duplicates.csv",
    "original_data_fname": "original_data.csv"
}

# Safe Donors
SAFE_DONORS = [
    "Trade Union",
    "Registered Political Party",
    "Friendly Society",
    "Public Fund"
]

# Dubious Donations
DUBIOUS_DONATION_TYPES = [
    "Impermissible Donor",
    "Unidentified Donor",
    "Total value of donations not reported individually",
    "Aggregated Donation"
]

# Placeholder values
PLACEHOLDER_DATE = pd.Timestamp("1900-01-01 00:00:00")
PLACEHOLDER_ID = 1000001

# Threshold for donations
THRESHOLDS = {
    0: "No Relevant Donations",
    1: "Single Donation Entity",
    50: "Very Small Entity",
    100: "Small Entity",
    1000: "Medium Entity"
}

# PartyParent RegulatedEntityId's
PARTYPARENTS = {
    "Conservative": 52,
    "Liberal Democrat": 90,
    "Labour": 53,
    "Scottish National Party": 102,
    "Green Party": 63,
    "Plaid Cymru": 77,
    "UK Independence Party (UKIP)": 85,
    "Unknown": 0
}
