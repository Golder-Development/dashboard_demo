import streamlit as st
import datasetupandclean as dc


# Set up multipage navigation and reference pages.
from app_pages.multi_page import MultiPage

# load pages scripts
from app_pages.page1 import page1_body
from app_pages.page2 import hlf_body
from app_pages.page3 import page3_body
from app_pages.page4 import page4_body
from app_pages.notesondataprep import notesondataprep_body

app = MultiPage(app_name="UK Political Donations")  # Create an instance

# Add your app pages here using .add_page()
app.add_page("Introduction", page1_body)
app.add_page("Head Line Figures", hlf_body)
app.add_page("Cash Donations", page3_body)
app.add_page("Dubious Donations", page4_body)
app.add_page("Notes on Data and Manipulations", notesondataprep_body)

app.run()  # Run the  app


# Load and cache data correctly
@st.cache_data
def get_data():
    return dc.load_data()


if "data" not in st.session_state:
    st.session_state["data"] = get_data()

# The app is now ready to be run. To run the app, open a terminal
# and run the following command streamlit run politicalpartyanalysis.py
