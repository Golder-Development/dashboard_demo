import streamlit as st
from components.global_variables import initialize_session_state
initialize_session_state()
from data.data_loader import firstload
# initializations


from app_pages.multi_page import MultiPage
from app_pages.introduction import introduction_body
from app_pages.headlinefigures import hlf_body
from app_pages.dubiousdonations import dubiousdonations_body
from app_pages.dubiousdonationsByRegulatedEntity import dubiousdonationsByDonor_body
from app_pages.cashdonations import cash_donations_page
from app_pages.cashdonationsByRegulatedEntity import cashdonationsregentity_body
from app_pages.sponsorships import sponsorships_body_page
from app_pages.donorspage_headlines import donorsheadlinespage_body
from app_pages.donors_perdonor_page import donorspage_body
from app_pages.visits import visits_body_page
from app_pages.notesondataprep import notesondataprep_body

app = MultiPage(app_name="UK Political Donations")  # Create an instance
# Display a loading message
loading_message = st.empty()
loading_message.markdown("<h3 style='text-align: center; color: blue;'>"
                         "Please wait while the data sets are being "
                         "calculated...</h3>", unsafe_allow_html=True)


# Add your app pages here using .add_page()
app.add_page("Introduction", introduction_body)
app.add_page("Head Line Figures", hlf_body)
app.add_page("Dubious Donations", dubiousdonations_body)
app.add_page("Dubious Donations by Regulated Entity",
             dubiousdonationsByDonor_body)
app.add_page("Cash Donations", cash_donations_page)
app.add_page("Cash Donations by Regulated Entity",
             cashdonationsregentity_body)
app.add_page("Sponsorships", sponsorships_body_page)
# app.add_page("Bequeths", bequeth_body)
app.add_page("Paid Visits", visits_body_page)
# app.add_page("Regulated Entities", regulatedentitypage_body)
# app.add_page("Donor is a Political Party", donationsbypoliticalpartys_body)
app.add_page("Donors Head Lines", donorsheadlinespage_body)
app.add_page("Donations Per Donor", donorspage_body)
app.add_page("Notes on Data and Manipulations", notesondataprep_body)

app.run()  # Run the  app

# Assuming data_loader is a module or class that needs to be imported

firstload()  # Load the data

loading_message.empty()

# The app is now ready to be run. To run the app, open a terminal
# and run the following command streamlit run politicalpartyanalysis.py
