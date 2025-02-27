import pandas as pd
import re
import os
import pdpy
from utils.logger import logger
from utils.decorators import log_function_call  # Import decorator

# Define the base directory (can be adjusted if needed)
BASE_DIR = os.path.dirname(__file__)  # Gets the directory of the script
# change the directory to the parent directory and then to the data directory
BASE_DIR = os.path.join(BASE_DIR, "..", "reference_files")
# Construct file paths dynamically
file_path = os.path.join(BASE_DIR, "ListOfPoliticalPeople.csv")
mppartymemb_pypd_path = os.path.join(BASE_DIR, "mppartymemb_pypd.csv")
final_file_path = os.path.join(BASE_DIR, "ListOfPoliticalPeople_Final.csv")
# Load dataset
df = pd.read_csv(file_path)


# Function to extract status and clean names
def extract_status_and_clean_name(name):
    status_list = []

    for prefix in [
        "Mr",
        "Mrs",
        "Ms",
        "Miss",
        "Dr",
        "Prof",
        "Sir",
        "Lord",
        "Lady",
        "Dame",
        "Baroness",
        "Baron",
        "Viscount",
        "Viscountess",
        "Earl",
        "Countess",
        "Duke",
        "Duchess",
        "Prince",
        "Princess",
        "King",
        "Queen",
        "President",
        "Chairman",
        "The Rt Hon",
    ]:
        if re.search(rf"\b{re.escape(prefix)}\b", name):
            status_list.append(prefix)
            name = re.sub(rf"\b{re.escape(prefix)}\b", "", name).strip()

    for suffix in [
        "MP",
        "MSP",
        "MEP",
        "Mp",
        "Msp",
        "Mep",
        "mp",
        "msp",
        "mep",
        "QC",
        "Qc",
        "qc",
        "CBE",
        "Cbe",
        "cbe",
        "OBE",
        "Obe",
        "obe",
        "MBE",
        "Mbe",
        "mbe",
        "KBE",
        "Kbe",
        "kbe",
        "DBE",
        "Dbe",
        "dbe",
    ]:
        if re.search(rf"\b{suffix}\b", name):
            status_list.append(suffix)
            name = re.sub(rf"\b{suffix}\b", "", name).strip()

    status = " & ".join(status_list) if status_list else None
    return name, status


# Function to query PdPy api
def get_party_df_from_pdpy(
    from_date="2001-01-01", to_date="2024-12-31", while_mp=False, collapse=True
):
    mppartymemb_df = pdpy.fetch_mps_party_memberships(
        from_date=from_date, to_date=to_date, while_mp=while_mp, collapse=collapse
    )
    # feedback
    mppartymemb_df = mppartymemb_df.drop(columns=["person_id", "party_id"])
    print("Fetched data from PdPy sample")
    print(mppartymemb_df[["given_name", "family_name", "party_name"]].head())
    # Save final dataset
    mppartymemb_df.to_csv(mppartymemb_pypd_path, index=False)
    return mppartymemb_df


# procedure to create unified name column for mp party membership data
def create_unified_name_column(given_name, family_name):
    First_Last_Name = given_name + " " + family_name
    Last_First_Name = family_name + " " + given_name
    return First_Last_Name, Last_First_Name


# Function to determine party based on name
def get_party_from_pdpy_df(pdpydf, name):
    if pdpydf is not None:
        party = pdpydf.loc[pdpydf["First_Last_Name"] == name, "party_name"].values
        if party.size > 0:
            return party[0]
        else:
            party = pdpydf.loc[pdpydf["display_name"] == name, "party_name"].values
            if party.size > 0:
                return party[0]
        return "Unknown"
    else:
        return "Issue with PdPy data"


# Clean names and extract status
df[["CleanedName", "Status"]] = df["RegulatedEntityName"].apply(
    lambda x: pd.Series(extract_status_and_clean_name(x))
)


# # Assign PoliticalParty based off UK Parliament data
# create pdpydf
pdpydf = get_party_df_from_pdpy()

# create unified name column on pdpydf
pdpydf[["First_Last_Name", "Last_First_Name"]] = pdpydf.apply(
    lambda row: pd.Series(
        create_unified_name_column(row["given_name"], row["family_name"])
    ),
    axis=1,
)

# Assign PoliticalParty based off PdpY data
df["PoliticalParty_pdpy"] = df.apply(
    lambda row: get_party_from_pdpy_df(pdpydf, row["CleanedName"]),
    axis=1,
)
testdata = False
if testdata:
    print("sample of original file")
    print(
        df[
            [
                "OriginalRegulatedEntityName",
                "RegulatedEntityName",
                "CleanedName",
                "Status",
            ]
        ].head()
    )
    print("sample of cleaned file")
    print(
        df[["OriginalRegulatedEntityName", "CleanedName", "PoliticalParty_pdpy"]].head()
    )
    # print count of records by party
    print("count of records by party")
    print(df["PoliticalParty_pdpy"].value_counts())

# Save final dataset
ref_dir
final_file_path = os.path.join(BASE_DIR, "ListOfPoliticalPeople_Final.csv")
df.to_csv(final_file_path, index=False)

print(f"Processed file saved as: {final_file_path}")
