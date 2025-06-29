# config.py - Stores global constants

import os
import pandas as pd
from pathlib import Path
# Base directory
BASE_DIR = Path(os.getcwd())

# ReRun MP Party Membership
RERUN_MP_PARTY_MEMBERSHIP = False

# Placeholder values
PLACEHOLDER_DATE = pd.Timestamp("1900-01-01 00:00:00")
PLACEHOLDER_ID = 1000001
perc_target = 0.5

DIRECTORIES = {  # "directory_name": "directory_path"
    "BASE_DIR": Path(os.getcwd()),
    "data_dir": os.path.join("data"),
    "output_dir": os.path.join("output"),
    "logs_dir": os.path.join("logs"),
    "reference_dir": os.path.join("reference_files"),
    "components_dir": os.path.join("components"),
    "app_pages_dir": os.path.join("app_pages"),
    "utils_dir": os.path.join("utils"),
    "source_dir": os.path.join("source"),
    "tests_dir": os.path.join("tests"),
}

DIRECTORIES_original = {  # "directory_name": "directory_path"
    "BASE_DIR": Path(os.getcwd()),
    "data_dir": os.path.join(BASE_DIR, "data"),
    "output_dir": os.path.join(BASE_DIR, "output"),
    "logs_dir": os.path.join(BASE_DIR, "logs"),
    "reference_dir": os.path.join(BASE_DIR, "reference_files"),
    "components_dir": os.path.join(BASE_DIR, "components"),
    "app_pages_dir": os.path.join(BASE_DIR, "app_pages"),
    "utils_dir": os.path.join(BASE_DIR, "utils"),
    "source_dir": os.path.join(BASE_DIR, "source"),
    "tests_dir": os.path.join(BASE_DIR, "tests"),
}

# File paths
FILENAMES = {  # "directory" : {"file_name": "file_path"}
    "reference_dir": {
        "Donor_dedupe_cleaned_fname": "Donor_dedupe_cleaned_data.csv",
        "ListofPoliticalPeople_fname": "ListOfPoliticalPeople.csv",
        "mppartymemb_fname": "mppartymemb_pypd.csv",
        "donor_map_fname": "PoliticalDonorsDeduped.csv",
        "politician_party_fname": "ListOfPoliticalPeople_Final.csv",
        "regentity_map_fname": "PoliticalEntityDeDuped.csv",
        "original_data_fname": "original_data.csv",
        "CREDENTIALS_FILE": "admin_credentials.json",
        "TEXT_FILE": "admin_text.json",
        "ELECTION_DATES": "elections.csv",
        "LAST_MODIFIED_DATES": "last_modified_dates.json",
    },
    "output_dir": {
        "cleaned_data_fname": "cleaned_data.csv",
        "cleaned_donations_fname": "cleaned_donations.csv",
        "cleaned_donorlist_fname": "cleaned_donorlist.csv",
        "cleaned_regentity_fname": "cleaned_regentity.csv",
        "party_summary_fname": "party_summary.csv",
        "imported_raw_fname": "imported_raw.csv",
    },
    "source_dir": {
        "source_data_fname": "Donations_accepted_by_political_parties_202506.csv"
    },
}


# Threshold for donations
THRESHOLDS = {  # "threshold_range": "threshold_name"
    (0, 0): "No Relevant Donations",
    (1, 1): "Single Donation Entity",
    (2, 5): "Very Small Entity",
    (6, 15): "Small Entity",
    (16, 100): "Small Medium Entity",
    (101, 200): "Medium Entity",
    (201, 500): "Medium Large Entity",
    (501, 1000): "Large Entity",
}

# Data remappings
DATA_REMAPPINGS = {
    "NatureOfDonation": {  # "original_value": "new_value"
        "IsBequest": "Is A Bequest",
        "IsAggregation": "Aggregated Donation",
        "IsSponsorship": "Sponsorship",
        "Donation to nan": "Other",
        "Other Payment": "Other",
    },
    # Mapping of party name to RegulatedEntityId
    "PartyParents": {  # "party_name": "RegulatedEntityId"
        "Conservatives": 52,
        "Labour": 53,
        "Liberal Democrats": 90,
        "Scottish National Party": 102,
        "Green Party": 63,
        "Plaid Cymru": 77,
        "UKIP": 85,
        "Unknown": 0,
    },
}

# category filter definitions
FILTER_DEF = {  # "filter_name": {"column_name": "value"}
    "Sponsorships_ftr": {
        "NatureOfDonation": "Sponsorship",
        "IsSponsorshipInt": 1,
    },
    "ReturnedDonations_ftr": {
        "DonationAction": ["Returned", "Forfeited"],
        "DubiousData": list(range(1, 11)),  # Fixed incorrect range syntax
    },
    "DubiousDonors_ftr": {"DubiousDonor": list(range(1, 11))},
    "DubiousDonations_ftr": {"DubiousData": list(range(1, 11))},
    "AggregatedDonations_ftr": {
        "IsAggregationInt": 1,
        "NatureOfDonation": "Aggregated Donation",
        "DonationType": "Aggregated Donation",
    },
    "SafeDonors_ftr": {
        "DonorStatus": [
            "Trade Union",
            "Registered Political Party",
            "Friendly Society",
            "Public Fund",
        ]
    },
    "DubiousDonorTypes_ftr": {
        "DonorStatus": ["Impermissible Donor",
                        "Unidentified Donor",
                        "Unidentifiable Donor",
                        "Anonymous Donor",
                        ],
        "DonorName": ["Impermissible Donor",
                      "Unidentified Donor",
                      "Unidentifiable Donor",
                      "Anonymous Donor",
                     ],
        "NatureOfDonation": ["Impermissible Donor",
                             "Unidentified Donor",
                             "Unidentifiable Donor",
                             "Anonymous Donor",
                            ],
        "DonorId": [1000001],
        "DonationType": ["Impermissible Donor",
                         "Unidentified Donor",
                         "Unidentifiable Donor",
                         "Anonymous Donor",
                        ],
        },
    "DubiousDonationType_ftr": {
        "NatureOfDonation": [
            "Impermissible Donor",
            "Unidentified Donor",
            "Total value of donations not reported individually",
            "Aggregated Donation",
        ],
        "DonationType": [
            "Aggregated Donation"]
        ,
        "IsAggregation": [True],
        "ReceivedDate": ["PLACEHOLDER_DATE", None],
        "RegulatedEntityId": [1000001],
        "RegulatedEntityName": [
                                "Unidentified Entity",
                                "Unidentifiable Entity",
                                "Unknown Entity",
                                ],
        "DonationAction": ["Returned", "Forfeited"],
        "IsAggregation": [True],
    },
    "BlankDate_ftr": {"ReceivedDate": ["PLACEHOLDER_DATE", None]},
    "BlankDonor_ftr": {"DonorId": [1000001]},
    "BlankRegEntity_ftr": {"RegulatedEntityId": [1000001]},
    "DonatedVisits_ftr": {"DonationType": "Visit",
                          "NatureOfDonation": "Visit"},
    "Bequests_ftr": {"IsBequestInt": 1,
                     "NatureOfDonation": "Bequest",
                     "DonationType": "Bequest"},
    "CorporateDonations_ftr": {
        "DonorStatus": ["Company",
                        "Partnership",
                        "Limited Liability Partnership"]
    },
    "RegulatedEntity_ftr": {
        "RegulatedEntityType": ["Political Party",
                                "Regulated Donee",
                                "Permitted Participant",
                                "Third Party"
                                ]},
    "PoliticalParty_ftr": {"DonorStatus": "Registered Political Party"},
    "CashDonations_ftr": {"DonationType": ["Cash", "Aggregate Donation"]},
    "PublicFundsDonations_ftr": {"DonationType": "Public Funds"},
    "NonCashDonations_ftr": {"DonationType": ["Non Cash",
                                              "Visit",
                                              "Bequest",
                                              "Sponsorship",]},
}

SECURITY = {  # "security_variable": "security_value"
    "is_admin": False,
    "is_authenticated": False,
    "username": "",
    "password": "",
}
