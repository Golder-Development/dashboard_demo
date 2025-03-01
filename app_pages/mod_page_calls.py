import streamlit as st
from app_pages.modular_page import display_data_page
from app_pages.modular_page_per_donor import (
    display_per_group_data_page
)
from components.text_management import check_password  # , load_page_text
from utils.logger import logger  # Import the logger
from utils.logger import log_function_call  # Import decorator


# Example usage for different pages
# Donated Visits
def mod_visits_page():
    display_data_page(filter_key="DonatedVisits_ftr",
                      target_label="Donated Visit")


# Visits per donor
def mod_visits_per_donor():
    display_per_group_data_page(filter_key="DonatedVisits_ftr",
                                target_label="Donated Visits per Donor",
                                group_entity="Donor")


# Visits per entity
def mod_visits_per_regulated_entity():
    display_per_group_data_page(filter_key="DonatedVisits_ftr",
                                target_label="Donated Visits per Entity",
                                group_entity="RegulatedEntity")


# Donated Sponsorships
def mod_sponsorship_page():
    display_data_page(filter_key="Sponsorships_ftr",
                      target_label="Sponsorship")


# Sponsorships per Entity
def mod_sponsorships_per_entity_page():
    display_per_group_data_page(filter_key="Sponsorships_ftr",
                                target_label="Sponsorships per Entity",
                                group_entity="RegulatedEntity")


# sponsorships per donor
def mod_sponsorships_per_donor_page():
    display_per_group_data_page(filter_key="Sponsorships_ftr",
                                target_label="Sponsorships per Donor",
                                group_entity="Donor")


# Donated Bequests
def mod_bequeths_page():
    display_data_page(filter_key="Bequests_ftr",
                      target_label="Bequest")


# Corporate Donations
def mod_corporate_donations_page():
    display_data_page(filter_key="CorporateDonations_ftr",
                      target_label="Corporate Donation")


# corporate Donorations per donor
def mod_corporate_donorations_per_donor_page():
    display_per_group_data_page(filter_key="CorporateDonations_ftr",
                                target_label="Corporate Donations per Entity",
                                group_entity="Donor")


# corporate donations per entity
def mod_corporate_donations_per_donor_page():
    display_per_group_data_page(filter_key="CorporateDonations_ftr",
                                target_label="Corporate Donations per Donor",
                                group_entity="RegulatedEntity")


# Dubious Donations
def mod_dubious_donations_page():
    display_data_page(filter_key="DubiousDonations_ftr",
                      target_label="Dubious Donor")


# Dubious Donations by entity
def mod_dubious_donations_per_entity_page():
    display_per_group_data_page(filter_key="DubiousDonations_ftr",
                                target_label="Dubious Donors per Entity",
                                group_entity="RegulatedEntity")


# Dubious Donations per donor
def mod_dubious_donations_per_donor_page():
    display_per_group_data_page(filter_key="DubiousDonations_ftr",
                                target_label="Dubious Donors per Donor",
                                group_entity="Donor")


# Corporate Donors per Entity
def mod_corporate_donations_per_entity_page():
    display_per_group_data_page(filter_key="CorporateDonations_ftr",
                                target_label="Corporate Donations per Entity",
                                group_entity="RegulatedEntity")


# Donations by Political Party by donor
def mod_donations_per_political_party_page():
    display_per_group_data_page(filter_key="PoliticalParty_ftr",
                                target_label="Donations per Political Party",
                                group_entity="Donor")


# Regulated Entity Donors
def mod_regulated_donor_per_entity_page():
    display_per_group_data_page(filter_key="RegulatedEntity_ftr",
                                target_label="Donors per Regulated Entity",
                                group_entity="RegulatedEntity")


# Regulated Entity Donors
def mod_regulated_entity_per_donors_page():
    display_per_group_data_page(filter_key="RegulatedEntity_ftr",
                                target_label="Regulated Entity by Donor",
                                group_entity="Donor")


# Dubious Donors by entity
def mod_dubious_donors_per_entity_page():
    display_per_group_data_page(filter_key="DubiousDonors_ftr",
                                target_label="Dubious Donors per Entity",
                                group_entity="RegulatedEntity")


# Dubious Donors
def mod_dubious_donors_page():
    display_data_page(filter_key="DubiousDonors_ftr",
                      target_label="Dubious Donor")


# Cash Donations
def mod_cash_donations_page():
    display_data_page(filter_key="CashDonations_ftr",
                      target_label="Cash Donation")


# Cash Donations per donor
def mod_cash_donations_per_donor_page():
    display_per_group_data_page(filter_key="CashDonations_ftr",
                                target_label="Cash Donations per Donor",
                                group_entity="Donor")


# Cash Donations per entity
def mod_cash_donations_per_entity_page():
    display_per_group_data_page(filter_key="CashDonations_ftr",
                                target_label="Cash Donations per Entity",
                                group_entity="RegulatedEntity")


# Non Cash Donations
def mod_non_cash_donations_page():
    display_data_page(filter_key="NonCashDonations_ftr",
                      target_label="Non Cash Donation")


# Non Cash Donations per donor
def mod_non_cash_donations_per_donor_page():
    display_per_group_data_page(filter_key="NonCashDonations_ftr",
                                target_label="Non Cash Donations per Donor",
                                group_entity="Donor")


# Non Cash Donations per entity
def mod_non_cash_donations_per_entity_page():
    display_per_group_data_page(filter_key="NonCashDonations_ftr",
                                target_label="Non Cash Donations per Entity",
                                group_entity="RegulatedEntity")


# login
@log_function_call
def loginpage():
    # page_texts = load_page_text("login")

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


# logout
@log_function_call
def logoutpage():
    # page_texts = load_page_text("logout")

    if "is_admin" not in st.session_state:
        st.session_state.security["is_admin"] = False

    # Logout button
    if st.session_state.security["is_admin"]:
        if st.button("Logout"):
            st.session_state.security["is_admin"] = False
            st.success("Logout successful!")
