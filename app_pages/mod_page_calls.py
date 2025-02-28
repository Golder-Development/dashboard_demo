import streamlit as st
from app_pages.modular_page import display_data_page
from app_pages.modular_page_per_donor import (
    display_data_page as display_per_group_data_page
)
from app_pages.modular_page_per_entity import (
    display_data_page as display_per_entity_data_page
)
from components.text_management import load_page_text, check_password
from utils.logger import logger  # Import the logger
from utils.logger import log_function_call  # Import decorator


# Example usage for different pages
# Donated Visits
def mod_visits_page():
    display_data_page("DonatedVisits_ftr",
                      "Donated Visit")


# Visits per donor
def mod_visits_per_donor():
    display_per_group_data_page("Visits_ftr",
                                "Visit per Donor",
                                "Donor")


# Visits per entity
def mod_visits_per_regulated_entity():
    display_per_group_data_page("Visits_ftr",
                                "Visit per Regulated Entity",
                                "RegulatedEntity")


# Donated Sponsorships
def mod_sponsorship_page():
    display_data_page("Sponsorships_ftr",
                      "Sponsorship")


# Sponsorships per Entity
def mod_sponsorships_per_entity_page():
    display_per_group_data_page("Sponsorships_ftr",
                                "Sponsor",
                                "RegulatedEntity")


# sponsorships per donor
def mod_sponsorships_per_donor_page():
    display_per_group_data_page("Sponsorships_ftr",
                                "Sponsor",
                                "Donor")


# Donated Bequests
def mod_bequeths_page():
    display_data_page("Bequests_ftr",
                      "Bequest")


# Corporate Donations
def mod_corporate_donations_page():
    display_data_page("CorporateDonations_ftr",
                      "Corporate Donation")


# corporate Donorations per donor
def mod_corporate_donorations_per_donor_page():
    display_per_entity_data_page("CorporateDonations_ftr",
                                 "Dubious Donors by Entity",
                                 "Donor")


# corporate donations per entity
def mod_corporate_donations_per_donor_page():
    display_per_entity_data_page("CorporateDonations_ftr",
                                 "Dubious Donors by Entity",
                                 "RegulatedEntity")


# Dubious Donations
def mod_dubious_donations_page():
    display_data_page("DubiousDonations_ftr",
                      "Dubious Donor")


# Dubious Donations by entity
def mod_dubious_donations_per_entity_page():
    display_per_group_data_page("DubiousDonations_ftr",
                                 "Dubious Donors by Entity",
                                 "RegulatedEntity")


# Dubious Donations per donor
def mod_dubious_donations_per_donor_page():
    display_per_group_data_page("DubiousDonations_ftr",
                                 "Dubious Donors by Entity",
                                 "Donor")


# Corporate Donors per Entity
def mod_corporate_donations_per_entity_page():
    display_per_group_data_page("CorporateDonations_ftr",
                                "Company Donor",
                                "RegulatedEntity")


# Donations by Political Party by donor
def mod_donations_per_political_party_page():
    display_per_group_data_page("PoliticalParty_ftr",
                                 "Donations by Political Party",
                                 "Donor")

    
# Regulated Entity Donors
def mod_regulated_donor_per_entity_page():
    display_per_group_data_page("RegulatedEntity_ftr",
                                "Donors by Regulated Entity",
                                "RegulatedEntity")


# Regulated Entity Donors
def mod_regulated_entity_per_donors_page():
    display_per_group_data_page("RegulatedEntity_ftr",
                                "Regulated Entity by Donor",
                                "Donor")


# Dubious Donors by entity
def mod_dubious_donors_per_entity_page():
    display_per_group_data_page("DubiousDonors_ftr",
                                 "Dubious Donors by Entity",
                                 "Regulatedentity")


# Dubious Donors
def mod_dubious_donors_page():
    display_data_page("DubiousDonors_ftr",
                      "Dubious Donors by Entity",
                      "Regulatedentity")




#login
@log_function_call
def loginpage():
    page_texts = load_page_text("login")

    if "is_admin" not in st.session_state:
        st.session_state.security["is_admin"] = False

    if not st.session_state.security["is_admin"]:
        st.subheader("Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if check_password(username, password):
                st.session_state.security["is_admin"] = True
                st.success("Login successful!")
                logger.info("User is not logged in as admin.")
            else:
                st.error("Invalid username or password.")
                st.success("You are not logged in as admin.")
                logger.info("User is not logged in as admin.")
    else:
        st.warning("You are already logged in as admin.")


#logout
@log_function_call
def logoutpage():
    page_texts = load_page_text("logout")

    if "is_admin" not in st.session_state:
        st.session_state.security["is_admin"] = False

    # Logout button
    if st.session_state.security["is_admin"]:
        if st.button("Logout"):
            st.session_state.security["is_admin"] = False
            st.success("Logout successful!")
