import pandas as pd
import requests
import re
import pdpy
import streamlit as st


# Load dataset
file_path = "reference_files//ListOfPoliticalPeople.csv"
df = pd.read_csv(file_path)


# Function to extract status and clean names
def extract_status_and_clean_name(name):
    status_list = []

    if name.startswith("The Rt Hon"):
        status_list.append("The Rt Hon")
        name = name.replace("The Rt Hon ", "").strip()

    for suffix in ["MP", "MSP", "MEP", "Mp", "Msp", "Mep"]:
        if re.search(rf"\b{suffix}\b", name):
            status_list.append(suffix)
            name = re.sub(rf"\b{suffix}\b", "", name).strip()

    status = " & ".join(status_list) if status_list else None
    return name, status


# Apply function
df[["CleanedName", "Status"]] = (
    df["RegulatedEntityName"]
    .apply(lambda x: pd.Series(extract_status_and_clean_name(x))
           )
    )


# Function to query PdPy api
def get_party_df_from_pdpy(name,
                           fromdate="2021-01-01",
                           todate="2021-12-31",
                           while_mp=True,
                           collapse=True):
    st.cache_data()
    mppartymemb_df = pdpy.fetch_mps_party_memberships(from_date="2021-01-01",
                                                      to_date="2021-12-31",
                                                      while_mp=True,
                                                      collapse=True)
    # Save final dataset
    final_file_path = "reference_files//mppartymemb_pypd.csv"
    mppartymemb_df.to_csv(final_file_path, index=False)
    return mppartymemb_df


# Function to query UK Parliament API
def get_party_from_parliament(name):
    url = f"https://members.parliament.uk/api/Members/Search?Name={name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "items" in data and data["items"]:
            party = (
                data["items"][0]["value"]["latestParty"]
                .get("name", "Unknown")
            )
            return party, 100
        return "Unknown", 50


# Assign PoliticalParty and Confidence
def determine_party(name, status, donee_type):
    party, confidence = get_party_from_parliament(name)
    comment = ""

    if party == "Unknown":
        if status and "The Rt Hon" in status:
            party = party
            confidence = 90
            comment = "Based on Cabinet Membership"
        elif "MP" in donee_type:
            party = party
            confidence = 85
            comment = "Based on MP"
        elif "MSP" in donee_type:
            party = party
            confidence = 85
            comment = "Based on MSP"
        elif "MEP" in donee_type:
            party = party
            confidence = 80
            comment = "Based on MEP"

    return party, confidence, comment


def get_party_from_pdpy_df(pdpydf, name):
    if pdpydf is not None:
        party = pdpydf.loc[pdpydf["name"] == name, "party"].values
        if party:
            return party[0], 100
        if "items" in party and party["items"]:
            party = (
                party["items"][0]["value"]["latestParty"]
                .get("name", "Unknown")
            )
            return party, 100
        return "Unknown", 50


# Apply function
df[["PoliticalParty", "Confidence", "Comment"]] = (
    df.apply(lambda row: pd.Series(
        determine_party(row["CleanedName"],
                        row["Status"],
                        row["RegulatedDoneeType"])
        ), axis=1)
    )

# Save final dataset
final_file_path = "reference_files//ListOfPoliticalPeople_Final.csv"
df.to_csv(final_file_path, index=False)

print(f"Processed file saved as: {final_file_path}")
