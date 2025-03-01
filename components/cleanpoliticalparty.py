import pandas as pd
import re
import os
import pdpy
import streamlit as st
from utils.logger import logger
from utils.logger import log_function_call  # Import decorator

@log_function_call
def load_mppartymemb_pypd():
    """Load MP party memberships data into session state."""
    try:
        # Load MP party memberships data
        mppartymemb_df = pd.read_csv(st.session_state.mppartymemb_fname)
        logger.debug(f"Loaded MP Party Memberships data: {mppartymemb_df}")

        # Store MP party memberships data in session state
        st.session_state.mppartymemb_pypd = mppartymemb_df

        logger.info("MP Party Memberships Data Loaded Successfully.")

    except Exception as e:
        logger.error(f"Failed to load MP Party Memberships data: {e}")
        st.session_state.mppartymemb_pypd = pd.DataFrame()


# Function to extract status and clean names
@log_function_call
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
@log_function_call
def get_party_df_from_pdpy(
    from_date="2001-01-01", to_date="2024-12-31", while_mp=False, collapse=True
):
    mppartymemb_df = pdpy.fetch_mps_party_memberships(
        from_date=from_date, to_date=to_date, while_mp=while_mp, collapse=collapse
    )
    # feedback
    mppartymemb_df = mppartymemb_df.drop(columns=["person_id", "party_id"])
    logger.debug("Fetched data from PdPy sample")
    logger.debug(mppartymemb_df[["given_name", "family_name", "party_name"]].head())
    # Save final dataset
    mppartymemb_df.to_csv(st.session_state.mppartymemb_fname, index=False)
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


@log_function_call
def clean_political_party_data():
    # Load MP party memberships data
    load_mppartymemb_pypd()

    # Load original file
    df = pd.read_csv(st.session_state.original_data_fname)

    # Clean names and extract status
    df[["CleanedName", "Status"]] = df["RegulatedEntityName"].apply(
        lambda x: pd.Series(extract_status_and_clean_name(x))
    )

    # Assign PoliticalParty based off UK Parliament data
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
    logger.debug("sample of original file")
    logger.debug(
        df[
            [
                "OriginalRegulatedEntityName",
                "RegulatedEntityName",
                "CleanedName",
                "Status",
            ]
        ].head()
        )
    logger.debug("sample of cleaned file"
    f" {df[['CleanedName', 'Status']].head()} ")
    # print count of records by party
    logger.debug("count of records by party"
    f" {df["PoliticalParty_pdpy"].value_counts()} ")# Save final dataset

    final_file_path = st.session_state.mp_party_memberships_file_path
    df.to_csv(final_file_path, index=False)

    logger.info(f"Processed file saved as: {final_file_path}")
