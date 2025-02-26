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

# Placeholder values
PLACEHOLDER_DATE = pd.Timestamp("1900-01-01 00:00:00")
PLACEHOLDER_ID = 1000001

# Threshold for donations
THRESHOLDS = {
    (0, 0): "No Relevant Donations",
    (1, 1): "Single Donation Entity",
    (2, 5): "Very Small Entity",
    (6, 15): "Small Entity",
    (16, 100): "Small Medium Entity",
    (101, 200): "Medium Entity",
    (201, 500): "Medium Large Entity",
    (501, 1000): "Large Entity"
}

# Data remappings
DATA_REMAPPINGS = {
    "NatureOfDonation": {
        "IsBequest": "Is A Bequest",
        "IsAggregation": "Aggregated Donation",
        "IsSponsorship": "Sponsorship",
        "Donation to nan": "Other",
        "Other Payment": "Other"
    },
    # Mapping of party name to RegulatedEntityId
    "PartyParents": {
        "Conservatives": 52,
        "Labour": 53,
        "Liberal Democrats": 90,
        "Scottish National Party": 102,
        "Green Party": 63,
        "Plaid Cymru": 77,
        "UKIP": 85,
        "Unknown": 0
    }
}

# category filter definitions
FILTER_DEF = {
    "Sponsorships_ftr": {
        "DonationType": "Sponsorship",
        "NatureOfDonation": "Sponsorship",
        "IsSponsorship": True
        },
    "ReturnedDonations_ftr": {
        "DonationAction": ["Returned", "Forfeited", "returned", "forfeited"],
        "DubiousData": list(range(1, 10))
        },
    "DubiousDonors_ftr": {
        "DubiousDonor": list(range(1, 10))
        },
    "AggregatedDonations_ftr": {
        "IsAggregation": True,
        "DonationType": "Aggregated Donation"
        },
    "SafeDonors_ftr": {
        "DonorType": ["Trade Union", "Registered Political Party",
                      "Friendly Society", "Public Fund"]
        },
    "DubiousDonationType_ftr": {
        "NatureOfDonation": ["Impermissible Donor",
                             "Unidentified Donor",
                             "Total value of donations not reported individually",
                             "Aggregated Donation"]
        },
    "BlankDate_ftr": {
        "ReceivedDate": [PLACEHOLDER_DATE, None]
        },
    "BlankDonor_ftr": {
        "DonorId": ["1000001", None]
        },
    "BlankRegEntity_ftr": {
        "RegulatedEntityId": ["1000001", None]
        },
    "DonatedVisits_ftr": {
        "DonationType": "Visit",
        "NatureOfDonation": "Visit"
        },
    }
