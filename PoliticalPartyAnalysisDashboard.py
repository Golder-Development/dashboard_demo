"""
A streamlist app to analyze political donations in the UK
Run this file first to start the app
"""
# import necessary modules
import streamlit as st
import os
# import local modules
try:
    import setup
    import politicalpartyanalysis
    from utils.logger import logger
    from data.data_loader import firstload
except ImportError as e:
    raise SystemExit(f"❌ Error: Failed to import modules - {e}")


# log current working directory
if 'logger' in globals():
    logger.info("🚀 Streamlit App Starting...")
    logger.info(f"Current Working Directory: {os.getcwd()}")
else:
    # Run the setup function
    raise SystemExit("❌ Error: Logger is not properly configured!")
# Run the setup function
try:
    setup.setup_package()
    logger.info("✅ Setup completed successfully.")
except Exception as e:
    logger.critical(f"App setup crashed: {e}", exc_info=True)
    st.error("App setup failed. Please check logs.")
    raise SystemExit("❌ App setup failed. Exiting.")

# run political party analysis
try:
    politicalpartyanalysis.pagesetup()
    logger.info("✅ Menu setup completed successfully.")
except Exception as e:
    logger.critical(f"Menu setup crashed: {e}", exc_info=True)
    st.error("Menu setup failed. Please check logs.")
    raise SystemExit("❌ Menu setup failed. Exiting.")


# Run the first load function
try:
    if "data_clean" not in st.session_state or st.session_state.data_clean is None:
        logger.info("No data found in session state, running firstload()")
        # Display a loading message
        load_message = st.empty()
        load_message.markdown("<h3 style='text-align: center; color: blue;'>"
                              "Please wait while the data sets are being "
                              "calculated...</h3>", unsafe_allow_html=True)
        firstload()  # Load the data
        logger.info("✅ Data first load completed successfully.")
        # Clear the loading message
        load_message.empty()
    else:
        logger.info("Data already loaded in session state.")
except Exception as e:
    logger.critical(f"❌ First load crashed: {e}", exc_info=True)
    st.error("Data loading failed. Please check logs.")
    raise SystemExit("❌ Data loading failed. Exiting.")

logger.info("🎉 App is fully loaded and ready!")
# The app is now ready to be run.
# To run the app, open a terminal and run:
#  "streamlit run PoliticalPartyAnalysisDashboard.py
# The app will open in a new tab in your default web browser.
