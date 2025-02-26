import streamlit as st
from app_pages.modular_page import display_data_page
from app_pages.modular_page_per_donor import (
    display_data_page as display_per_group_data_page
)
from app_pages.modular_page_per_entity import (
    display_data_page as display_per_entity_data_page
)
from components.text_management import load_page_text, check_password


# Example usage for different pages
def mod_visits_page():
    display_data_page("DonatedVisits_ftr",
                      "Donated Visit")


def mod_sponsorship_page():
    display_data_page("Sponsorships_ftr",
                      "Sponsorship")


def mod_bequeths_page():
    display_data_page("Bequests_ftr",
                      "Bequest")


def mod_corporate_donations_page():
    display_data_page("CorporateDonations_ftr",
                      "Corporate Donation")


def mod_dubious_donors_page():
    display_data_page("DubiousDonors_ftr",
                      "Dubious Donor")


def mod_corporate_donors_per_entity_page():
    display_per_group_data_page("CorporateDonations_ftr",
                                "Company Donor",
                                "RegulatedEntity")


def mod_sponsorships_per_entity_page():
    display_per_group_data_page("Sponsorships_ftr",
                                "Sponsor",
                                "RegulatedEntity")


def mod_sponsorships_per_donor_page():
    display_per_group_data_page("Sponsorships_ftr",
                                "Sponsor",
                                "Donor")


def mod_visits_per_donor():
    display_per_group_data_page("Visits_ftr",
                                "Visit per Donor",
                                "Donor")


def loginpage():
    page_texts = load_page_text("login")

    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False

    if not st.session_state.is_admin:
        st.subheader("Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if check_password(username, password):
                st.session_state.is_admin = True
                st.success("Login successful!")
            else:
                st.error("Invalid username or password.")


def logoutpage():
    page_texts = load_page_text("logout")

    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False

    # Logout button
    if st.session_state.is_admin:
        if st.button("Logout"):
            st.session_state.is_admin = False
            
