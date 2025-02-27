"""
A streamlist app to analyze political donations in the UK
Run this file first to start the app
"""
import streamlit as st
import setup
import politicalpartyanalysis
from data.data_loader import firstload

# Run the setup function
setup.setup()
# run political party analysis
politicalpartyanalysis.pagesetup()
# Display a loading message
loading_message = st.empty()
loading_message.markdown("<h3 style='text-align: center; color: blue;'>"
                         "Please wait while the data sets are being "
                         "calculated...</h3>", unsafe_allow_html=True)
# Run the first load function
firstload()
# Clear the loading message
loading_message.empty()
# The app is now ready to be run. To run the app, open a terminal
# and run the following command "streamlit run PoliticalPartyAnalysisDashboard.py
# The app will open in a new tab in your default web browser.