import streamlit as st
import data.datasetupandclean as dc

# Set up multipage navigation and reference pages.
from app_pages.multi_page import MultiPage

# load pages scripts
from app_pages.introduction import introduction_body
from app_pages.headlinefigures import hlf_body
# from app_pages.regulatedentitypage import regulatedentitypage_body
from app_pages.dubiousdonations import dubiousdonations_body
from app_pages.dubiousdonationsByRegulatedEntity\
    import dubiousdonationsByDonor_body
from app_pages.sponsorships import sponsorships_body
from app_pages.notesondataprep import notesondataprep_body
from app_pages.cashdonations import cash_donations_page
from app_pages.cashdonationsByRegulatedEntity\
    import cashdonationsregentity_body
from app_pages.donorspage_headlines import donorsheadlinespage_body
from app_pages.donorspage_perdonor import donorspage_body
from app_pages.visits import visits_body
# from app_pages.donationsbypoliticalpartys import
# donationsbypoliticalpartys_body

app = MultiPage(app_name="UK Political Donations")  # Create an instance

# Add your app pages here using .add_page()
# Display a loading message

app.add_page("Introduction", introduction_body)
app.add_page("Head Line Figures", hlf_body)
app.add_page("Dubious Donations", dubiousdonations_body)
app.add_page("Dubious Donations by Regulated Entity",
             dubiousdonationsByDonor_body)
app.add_page("Cash Donations", cash_donations_page)
app.add_page("Cash Donations by Regulated Entity",
             cashdonationsregentity_body)
app.add_page("Sponsorships", sponsorships_body)
# app.add_page("Bequeths", bequeth_body)
app.add_page("Paid Visits", visits_body)
# app.add_page("Regulated Entities", regulatedentitypage_body)
# app.add_page("Donor is a Political Party", donationsbypoliticalpartys_body)
app.add_page("Donors Head Lines", donorsheadlinespage_body)
app.add_page("Donorations Per Donor", donorspage_body)
app.add_page("Notes on Data and Manipulations", notesondataprep_body)

app.run()  # Run the  app

loading_message = st.empty()
loading_message.markdown("<h3 style='text-align: center; color: blue;'>"
                         "Please wait while the data sets are being "
                         "calculated...</h3>", unsafe_allow_html=True)

# Ensure g_thresholds is available as a global dictionary
if 'g_thresholds' not in st.session_state:
    dc.create_thresholds()


# Load and cache data correctly
@st.cache_data
def get_data():
    return dc.load_data(output_csv=False,
                        dedupe_donors=False,
                        dedupe_regentity=False
                        )


@st.cache_data
def get_party_summary_data():
    return dc.load_party_summary_data(output_csv=False)


@st.cache_data
def get_cleaned_data():
    return dc.load_cleaned_data(output_csv=False)


@st.cache_data
def get_donor_data():
    return dc.load_donorList_data(output_csv=False)


@st.cache_data
def get_regentity_data():
    return dc.load_regulated_entity_data(output_csv=False)


if "data" not in st.session_state:
    st.session_state["data"] = get_data()


if "data_party_sum" not in st.session_state:
    st.session_state["data_party_sum"] = get_party_summary_data()


if "data_clean" not in st.session_state:
    st.session_state["data_clean"] = get_cleaned_data()


if "data_donor" not in st.session_state:
    st.session_state["data_donor"] = get_donor_data()


if "data_regentity" not in st.session_state:
    st.session_state["data_regentity"] = get_regentity_data()


# Remove the loading message
loading_message.empty()

# The app is now ready to be run. To run the app, open a terminal
# and run the following command streamlit run politicalpartyanalysis.py
