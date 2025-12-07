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
    tab1, tab2 = st.tabs(["Donated Visits", "Donated Visits by.."])
    with tab1:
        display_data_page(functionname="mod_visits",
                          filter_key="DonatedVisits_ftr",
                          target_label="Donated Visit")
    with tab2:
        display_per_group_data_page(
            functionname="mod_visits_per_donor",
            filter_key="DonatedVisits_ftr",
            target_label="Donated Visits per Donor",
            group_entity="Donor")


# Donated Sponsorships
def mod_sponsorships():
    tab1, tab2 = st.tabs(["Sponsorships", "Sponsorships by.."])
    with tab1:
        display_data_page(
            functionname="mod_sponsorships",
            filter_key="Sponsorships_ftr",
            target_label="Sponsorship")
    with tab2:
        display_per_group_data_page(
            functionname="mod_sponsorships_per_donor",
            filter_key="Sponsorships_ftr",
            target_label="Sponsorships per Donor",
            group_entity="Donor")


# Donated Bequests
def mod_bequeths():
    tab1, tab2 = st.tabs(["Bequests", "Bequests by.."])
    with tab1:
        display_data_page(
            functionname="mod_bequeths",
            filter_key="Bequests_ftr",
            target_label="Bequest")
    with tab2:
        display_per_group_data_page(
            functionname="mod_bequeths_per_donor",
            filter_key="Bequests_ftr",
            target_label="Bequest per Donor",
            group_entity="Donor")


# Corporate Donations
def mod_corporate_donations():
    tab1, tab2 = st.tabs(["Corporate Donations", "Corporate Donations by.."])
    with tab1:
        display_data_page(
            functionname="mod_corporate_donations",
            filter_key="CorporateDonations_ftr",
            target_label="Corporate Donation")
    with tab2:
        display_per_group_data_page(
            functionname="mod_corporate_donations_per_donor",
            filter_key="CorporateDonations_ftr",
            target_label="Corporate Donation per Donor",
            group_entity="Donor")


# Dubious Donations
def mod_dubious_donations():
    tab1, tab2 = st.tabs(["Dubious Donations", "Dubious Donations by.."])
    with tab1:
        display_data_page(
            functionname="mod_dubious_donations",
            filter_key="DubiousDonations_ftr",
            target_label="Dubious Donation")
    with tab2:
        display_per_group_data_page(
            functionname="mod_dubious_donations_per_donor",
            filter_key="DubiousDonations_ftr",
            target_label="Dubious Donations per Donor",
            group_entity="Donor")


# Donations by Political Party by donor
def mod_donations_per_political_party():
    display_per_group_data_page(
            functionname="mod_donations_per_political_party",
            filter_key="PoliticalParty_ftr",
            target_label="Donations per Political Party",
            group_entity="Donor")


# Regulated Entity Donors
def mod_regulated_donor_per_entity():
    tab1, tab2 = st.tabs(["Donors per Regulated Entity",
                          "TBC"])
    with tab1:
        display_per_group_data_page(
            functionname="mod_regulated_donor_per_entity",
            filter_key="RegulatedEntity_ftr",
            target_label="Donors per Regulated Entity",
            group_entity="Party",)



def mod_regulated_entity_per_donor():
    tab1, tab2 = st.tabs(["Regulated Entity by Donor",
                          "TBC"])
    with tab1:
        display_per_group_data_page(
            functionname="mod_regulated_donor_per_entity",
            filter_key="RegulatedEntity_ftr",
            target_label="Regulated Entity by Entity",
            group_entity="Entity",
            tab_name="RegEntity_by_Donor")



# Dubious Donors
def mod_dubious_donors():
    tab1, tab2 = st.tabs(["Dubious Donors", "Dubious Donors by.."])
    with tab1:
        display_data_page(
            functionname="mod_dubious_donors",
            filter_key="DubiousDonors_ftr",
            target_label="Dubious Donor")
    with tab2:
        display_per_group_data_page(
            functionname="mod_dubious_donors_per_entity",
            filter_key="DubiousDonors_ftr",
            target_label="Dubious Donors per Entity",
            group_entity="Party")


# Cash Donations
def mod_cash_donations():
    tab1, tab2 = st.tabs(["Cash Donations", "Cash Donations by.."])
    with tab1:
        display_data_page(
            functionname="mod_cash_donations",
            filter_key="CashDonations_ftr",
            target_label="Cash Donation")
    with tab2:
        display_per_group_data_page(
            functionname="mod_cash_donations_per_donor",
            filter_key="CashDonations_ftr",
            target_label="Cash Donations per Donor",
            group_entity="Donor")


# Non Cash Donations
def mod_non_cash_donations():
    tab1, tab2 = st.tabs(["Non Cash Donations", "Non Cash Donations by.."])
    with tab1:
        display_data_page(
            functionname="mod_non_cash_donations",
            filter_key="NonCashDonations_ftr",
            target_label="Non Cash Donation")
    with tab2:
        display_per_group_data_page(
            functionname="mod_non_cash_donations_per_donor",
            filter_key="NonCashDonations_ftr",
            target_label="Non Cash Donations per Donor",
            group_entity="Donor")


# Public Fund Donation
def mod_publicfund_donations():
    Tab1, Tab2 = st.tabs(["Public Fund Donations",
                          "Public Fund Donations by.."])
    with Tab1:
        display_data_page(
            functionname="mod_publicfund_donations",
            filter_key="PublicFundsDonations_ftr",
            target_label="Public Fund Donation")
    with Tab2:
        display_per_group_data_page(
            functionname="mod_publicfund_donations_per_donor",
            filter_key="PublicFundsDonations_ftr",
            target_label="Public Fund Donation per Donor",
            group_entity="Donor")


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
