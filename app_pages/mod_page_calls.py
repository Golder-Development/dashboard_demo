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
def mod_visits():
    display_data_page(functionname="mod_visits",
                      filter_key="DonatedVisits_ftr",
                      target_label="Donated Visit")


# Visits per donor
def mod_visits_per_donor():
    display_per_group_data_page(
        functionname="mod_visits_per_donor",
        filter_key="DonatedVisits_ftr",
        target_label="Donated Visits per Donor",
        group_entity="Donor")


# Visits per entity
def mod_visits_per_regulated_entity():
    display_per_group_data_page(
        functionname="mod_visits_per_regulated_entity",
        filter_key="DonatedVisits_ftr",
        target_label="Donated Visits per Entity",
        group_entity="Party")


# Donated Sponsorships
def mod_sponsorships():
    display_data_page(
        functionname="mod_sponsorships",
        filter_key="Sponsorships_ftr",
        target_label="Sponsorship")


# Sponsorships per Entity
def mod_sponsorships_per_entity():
    display_per_group_data_page(
        functionname="mod_sponsorships_per_entity",
        filter_key="Sponsorships_ftr",
        target_label="Sponsorships per Entity",
        group_entity="Party")


# sponsorships per donor
def mod_sponsorships_per_donor():
    display_per_group_data_page(
        functionname="mod_sponsorships_per_donor",
        filter_key="Sponsorships_ftr",
        target_label="Sponsorships per Donor",
        group_entity="Donor")


# Donated Bequests
def mod_bequeths():
    display_data_page(
        functionname="mod_bequeths",
        filter_key="Bequests_ftr",
        target_label="Bequest")


def mod_bequeths_per_entity():
    display_per_group_data_page(
        functionname="mod_bequeths_per_entity",
        filter_key="Bequests_ftr",
        target_label="Bequest",
        group_entity="Party")


def mod_bequeths_per_donor():
    display_per_group_data_page(
        functionname="mod_bequeths_per_donor",
        filter_key="Bequests_ftr",
        target_label="Bequest",
        group_entity="Donor")


# Corporate Donations
def mod_corporate_donations():
    display_data_page(
        functionname="mod_corporate_donations",
        filter_key="CorporateDonations_ftr",
        target_label="Corporate Donation")


# corporate Donorations per donor
def mod_corporate_donorations_per_donor():
    display_per_group_data_page(
        functionname="mod_corporate_donorations_per_donor",
        filter_key="CorporateDonations_ftr",
        target_label="Corporate Donations per Entity",
        group_entity="Donor")


# corporate donations per entity
def mod_corporate_donations_per_donor():
    display_per_group_data_page(
        functionname="mod_corporate_donations_per_donor",
        filter_key="CorporateDonations_ftr",
        target_label="Corporate Donations per Donor",
        group_entity="Party")


# Dubious Donations
def mod_dubious_donations():
    display_data_page(
        functionname="mod_dubious_donations",
        filter_key="DubiousDonations_ftr",
        target_label="Dubious Donor")


# Dubious Donations by entity
def mod_dubious_donations_per_entity():
    display_per_group_data_page(
        functionname="mod_dubious_donations_per_entity",
        filter_key="DubiousDonations_ftr",
        target_label="Dubious Donors per Entity",
        group_entity="Party")


# Dubious Donations per donor
def mod_dubious_donations_per_donor():
    display_per_group_data_page(
        functionname="mod_dubious_donations_per_donor",
        filter_key="DubiousDonations_ftr",
        target_label="Dubious Donors per Donor",
        group_entity="Donor")


# Corporate Donors per Entity
def mod_corporate_donations_per_entity():
    display_per_group_data_page(
        functionname="mod_corporate_donations_per_entity",
        filter_key="CorporateDonations_ftr",
        target_label="Corporate Donations per Entity",
        group_entity="Party")


# Donations by Political Party by donor
def mod_donations_per_political_party():
    display_per_group_data_page(
        functionname="mod_donations_per_political_party",
        filter_key="PoliticalParty_ftr",
        target_label="Donations per Political Party",
        group_entity="Donor")


# Regulated Entity Donors
def mod_regulated_donor_per_entity():
    display_per_group_data_page(
        functionname="mod_regulated_donor_per_entity",
        filter_key="RegulatedEntity_ftr",
        target_label="Donors per Regulated Entity",
        group_entity="Party")


# Regulated Entity Donors
def mod_regulated_entity_per_donor():
    display_per_group_data_page(
        functionname="mod_regulated_entity_per_donor",
        filter_key="RegulatedEntity_ftr",
        target_label="Regulated Entity by Donor",
        group_entity="Donor")


# Dubious Donors by entity
def mod_dubious_donors_per_entity():
    display_per_group_data_page(
        functionname="mod_dubious_donors_per_entity",
        filter_key="DubiousDonors_ftr",
        target_label="Dubious Donors per Entity",
        group_entity="Party")


# Dubious Donors
def mod_dubious_donors():
    display_data_page(
        functionname="mod_dubious_donors",
        filter_key="DubiousDonors_ftr",
        target_label="Dubious Donor")


# Cash Donations
def mod_cash_donations():
    display_data_page(
        functionname="mod_cash_donations",
        filter_key="CashDonations_ftr",
        target_label="Cash Donation")


# Cash Donations per donor
def mod_cash_donations_per_donor():
    display_per_group_data_page(
        functionname="mod_cash_donations_per_donor",
        filter_key="CashDonations_ftr",
        target_label="Cash Donations per Donor",
        group_entity="Donor")


# Cash Donations per entity
def mod_cash_donations_per_entity():
    display_per_group_data_page(
        functionname="mod_cash_donations_per_entity",
        filter_key="CashDonations_ftr",
        target_label="Cash Donations per Entity",
        group_entity="Party")


# Non Cash Donations
def mod_non_cash_donations():
    display_data_page(
        functionname="mod_non_cash_donations",
        filter_key="NonCashDonations_ftr",
        target_label="Non Cash Donation")


# Non Cash Donations per donor
def mod_non_cash_donations_per_donor():
    display_per_group_data_page(
        functionname="mod_non_cash_donations_per_donor",
        filter_key="NonCashDonations_ftr",
        target_label="Non Cash Donations per Donor",
        group_entity="Donor")


# Non Cash Donations per entity
def mod_non_cash_donations_per_entity():
    display_per_group_data_page(
        functionname="mod_non_cash_donations_per_entity",
        filter_key="NonCashDonations_ftr",
        target_label="Non Cash Donations per Entity",
        group_entity="Party")


# Non Cash Donations
def mod_publicfund_donations():
    display_data_page(
        functionname="mod_publicfund_donations",
        filter_key="PublicFundsDonations_ftr",
        target_label="Non Cash Donation")


# Non Cash Donations per donor
def mod_publicfund_donations_per_donor():
    display_per_group_data_page(
        functionname="mod_publicfund_donations_per_donor",
        filter_key="PublicFundsDonations_ftr",
        target_label="Non Cash Donations per Donor",
        group_entity="Donor")


# Non Cash Donations per entity
def mod_publicfund_donations_per_entity():
    display_per_group_data_page(
        functionname="mod_publicfund_donations_per_entity",
        filter_key="PublicFundsDonations_ftr",
        target_label="Non Cash Donations per Entity",
        group_entity="Party")


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
