import streamlit as st
import datasetupandclean as dc

# Set up multipage navigation and reference pages.
from app_pages.multi_page import MultiPage

# load pages scripts
from app_pages.introduction import introduction_body
from app_pages.headlinefigures import hlf_body
# from app_pages.regulatedentitypage import regulatedentitypage_body
from app_pages.dubiousdonations import dubiousdonations_body
from app_pages.dubiousdonationsByRegulatedEntity import dubiousdonationsByDonor_body
# from app_pages.sponsorships import sponsorship_body
from app_pages.notesondataprep import notesondataprep_body
from app_pages.cashdonations import cashdonations_body
# from app_pages.donorspage import donorspage_body
# from app_pages.donationsbypoliticalpartys import donationsbypoliticalpartys_body

app = MultiPage(app_name="UK Political Donations")  # Create an instance

# Add your app pages here using .add_page()
# Display a loading message

app.add_page("Introduction", introduction_body)
app.add_page("Head Line Figures", hlf_body)
app.add_page("Cash Donations", cashdonations_body)
# app.add_page("Sponsorships", sponsorship_body)
# app.add_page("Bequeths", bequeth_body)
# app.add_page("Paid Visits", visits_body)
# app.add_page("Regulated Entities", regulatedentitypage_body)
# app.add_page("Donors", donorspage_body)
# app.add_page("Donor is a Political Party", donationsbypoliticalpartys_body)
app.add_page("Dubious Donations", dubiousdonations_body)
app.add_page("Dubious Donations by Regulated Entity", dubiousdonationsByDonor_body)
app.add_page("Notes on Data and Manipulations", notesondataprep_body)

app.run()  # Run the  app

loading_message = st.empty()
loading_message.markdown("<h3 style='text-align: center; color: blue;'>Please wait while the data sets are being calculated...</h3>", unsafe_allow_html=True)

# Ensure g_thresholds is available as a global dictionary
if 'g_thresholds' not in st.session_state:
    dc.create_thresholds()


# Load and cache data correctly
@st.cache_data
def get_data():
    return dc.load_data()


@st.cache_data
def get_party_summary_data():
    return dc.load_party_summary_data()


@st.cache_data
def get_cleaned_data():
    return dc.load_cleaned_data()


if "data" not in st.session_state:
    st.session_state["data"] = get_data()


if "data_party_sum" not in st.session_state:
    st.session_state["data_party_sum"] = get_party_summary_data()


if "data_clean" not in st.session_state:
    st.session_state["data_clean"] = get_cleaned_data()


# Remove the loading message
loading_message.empty()

# The app is now ready to be run. To run the app, open a terminal
# and run the following command streamlit run politicalpartyanalysis.py
