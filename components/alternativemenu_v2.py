"""
This is a rework of the multipage functionality to
mirror streamlits recommended approach, as outlined
on "https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation"
"""
import streamlit as st
from components.global_variables import initialize_session_state

initialize_session_state()
from data.data_utils import initialise_data
# from app_pages.multi_page import MultiPage
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
from app_pages.mod_page_calls import visits_per_entity_page as mod_visits_per_entity_page
from app_pages.mod_page_calls import visits_per_donor as mod_visits_per_donor
from app_pages.mod_page_calls import sponsorship_per_entity_page as mod_sponsor_per_entity_page
from app_pages.mod_page_calls import corporate_donations_page as mod_corporate_page
from app_pages.mod_page_calls import bequeths_page as mod_bequests_page
from app_pages.regulatedentitypage import regulatedentitypage_body
from app_pages.donationsbypoliticalpartys import donationsbypoliticalpartys_body
from app_pages.mod_page_calls import loginpage, logoutpage

initialise_data()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = True

login_page = st.Page(loginpage,
                     title="Log in",
                     icon=":material/login:")
logout_page = st.Page(logoutpage,
                      title="Log out",
                      icon=":material/logout:")
introduction = st.Page(
    introduction_body,
    title="Introduction",
    icon=":material/dashboard:",
    default=True
)
headlinefigures = st.Page(hlf_body,
                          title="Head Line Report",
                          icon=":material/bug_report:")
regulatedentity = st.Page(
    regulatedentitypage_body,
    title="Political Entity Analysis",
    icon=":material/notification_important:"
    )
visits = st.Page(visits_body_page,
                 title="Paid Visits",
                 icon=":material/attach_money:")
if mod_visits_per_entity_page:
    visitsperentity = st.Page(mod_visits_per_entity_page,
                              title="Paid Visits Per Entity",
                              icon=":material/attach_money:",
                              url_path="visitsperentity")
if mod_visits_per_donor:
    visitsperdonor = st.Page(mod_visits_per_donor,
                             title="Paid Visits Per Donor",
                             icon=":material/attach_money:")

sponsorships = st.Page(sponsorships_body_page,
                       title="Sponsorships",
                       icon=":material/attach_money:")
sponsorshipsperentity = st.Page(mod_sponsor_per_entity_page,
                                title="Sponsorships Per Entity",
                                icon=":material/attach_money:",
                                url_path="sponsorshipsperentity")

cashdonations = st.Page(cash_donations_page,
                        title="Cash Donations",
                        icon=":material/attach_money:")
cashdonationsperentity = st.Page(cashdonationsregentity_body,
                                 title="Cash Donations Per Entity",
                                 icon=":material/attach_money:")
dubiousdonations = st.Page(dubiousdonations_body,
                           title="Dubious Donations",
                           icon=":material/attach_money:")
dubiousdonationsperdonor = st.Page(dubiousdonationsByDonor_body,
                                   title="Dubious Donations Per Donor",
                                   icon=":material/attach_money:")
dubiousdonors = st.Page(dubiousdonations_body,
                        title="Dubious Donors",
                        icon=":material/attach_money:")
donors = st.Page(donorsheadlinespage_body,
                 title="Donors",
                 icon=":material/attach_money:")
donationsperentity = st.Page(donationsbypoliticalpartys_body,
                             title="Donations per Entity",
                             icon=":material/attach_money:")
bequests = st.Page(mod_bequests_page,
                   title="Bequests",
                   icon=":material/attach_money:")
companydonors = st.Page(mod_corporate_page,
                        title="Company Donors",
                        icon=":material/attach_money:")
donationsperdonor = st.Page(donorspage_body,
                            title="Donations Per Donor",
                            icon=":material/attach_money:")
notesondataprep = st.Page(notesondataprep_body,
                          title="Notes on Data Preparation",
                          icon=":material/notes:")
# individualdonors = st.Page("app_pages/individualdonors.py", title="Individual Donors", icon=":material/attach_money:")
# otherdonors = st.Page("app_pages/otherdonors.py", title="Other Donors", icon=":material/attach_money:")
# search = st.Page("tools/search.py", title="Search", icon=":material/search:")
# dubiousdonationsperentity = st.Page(dubiousdonationsByDonor_body, title="Dubious Donations Per Entity", icon=":material/attach_money:")
# sponsorshipsperdonor = st.Page("app_pages/sponsorshipsperdonor.py", title="Sponsorships Per Donor", icon=":material/attach_money:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            # "Account": [logout_page],
            "Headline Reports": [
                introduction,
                headlinefigures,
                visits,
                sponsorships,
                cashdonations,
                dubiousdonations,
                bequests,
                companydonors,
                # individualdonors,
                # otherdonors
                donors
                ],
            "Detailed Reports Per Entity": [
                regulatedentity,
                visitsperentity,
                sponsorshipsperentity,
                cashdonationsperentity,
                donationsperentity
                # dubiousdonationsperentity
                ],
            "Detailed Reports Per Donor": [
                donationsperdonor,

                ],
            "Tools": [
                notesondataprep
                ],
        }
    )
else:
    pg = st.navigation([introduction])

pg.run()
