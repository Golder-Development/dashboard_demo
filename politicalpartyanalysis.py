import streamlit as st
from components.global_variables import initialize_session_state
# initializations
initialize_session_state()
from data.data_loader import firstload
# from app_pages import introduction
from app_pages.multi_page import MultiPage
from app_pages.introduction import introduction_body
from app_pages.headlinefigures import hlf_body
from app_pages.dubiousdonations import dubiousdonations_body
from app_pages.dubiousdonationsByRegulatedEntity import (
    dubiousdonationsByDonor_body)
from app_pages.cashdonations import cash_donations_page
from app_pages.cashdonationsByRegulatedEntity import (
    cashdonationsregentity_body)
from app_pages.sponsorships import sponsorships_body_page
from app_pages.donorspage_headlines import donorsheadlinespage_body
from app_pages.donors_perdonor_page import donorspage_body
from app_pages.visits import visits_body_page
from app_pages.notesondataprep import notesondataprep_body
from app_pages.mod_page_calls import (mod_bequeths_page,
                                      mod_corporate_donations_page,
                                      mod_corporate_donors_per_entity_page,
                                      mod_dubious_donors_page,
                                      mod_sponsorships_per_entity_page,
                                      mod_sponsorship_page,
                                      mod_sponsorships_per_donor_page,
                                      mod_visits_page,
                                      loginpage,
                                      logoutpage
                                      )

# Create an instance of the MultiPage class
app = MultiPage(app_name="UK Political Donations")  # Create an instance
# Display a loading message
loading_message = st.empty()
loading_message.markdown("<h3 style='text-align: center; color: blue;'>"
                         "Please wait while the data sets are being "
                         "calculated...</h3>", unsafe_allow_html=True)

# Add your app pages here using .add_page()
app.add_page("Introduction", introduction_body)
app.add_page("Login", loginpage)
app.add_page("Head Line Figures", hlf_body)
app.add_page("Donors Head Lines", donorsheadlinespage_body)
app.add_page("Cash Donations", cash_donations_page)
app.add_page("Bequeths", mod_bequeths_page)
app.add_page("Corporate Donations", mod_corporate_donations_page)
app.add_page("Sponsorships", sponsorships_body_page)
app.add_page("Paid Visits", visits_body_page)
app.add_page("Dubious Donors", mod_dubious_donors_page)
app.add_page("Dubious Donations", dubiousdonations_body)
app.add_page("Dubious Donations by Regulated Entity",
             dubiousdonationsByDonor_body)
app.add_page("Cash Donations by Regulated Entity",
             cashdonationsregentity_body)
app.add_page("Sponsorship per entity ", mod_sponsorships_per_entity_page)
app.add_page("Corporate Donations per entity",
             mod_corporate_donors_per_entity_page)
app.add_page("Sponsorships -Mod", mod_sponsorship_page)
app.add_page("Paid Visits -Mod", mod_visits_page)
app.add_page("Sponsorships per Donor", mod_sponsorships_per_donor_page)
app.add_page("Donations Per Donor", donorspage_body)
app.add_page("Notes on Data and Manipulations", notesondataprep_body)
app.add_page("Logout", logoutpage)

# app.add_page("Regulated Entities", regulatedentitypage_body)

app.run()  # Run the  app

# Assuming data_loader is a module or class that needs to be imported

firstload()  # Load the data

loading_message.empty()

# The app is now ready to be run. To run the app, open a terminal
# and run the following command streamlit run politicalpartyanalysis.py
