"""
A streamlist app to analyze political donations in the UK
Run this file first to start the app
"""
# import necessary modules
import streamlit as st
import os
# Set the page config at the very beginning of the script
st.set_page_config(page_title="Political Party Analysis",
                   layout="wide")

# import local modules
try:
    import setup
    import politicalpartyanalysis
    from utils.logger import logger
    from data.data_utils import initialise_data
except ImportError as e:
    raise SystemExit(f"Error: Failed to import modules - {e}")


# log current working directory
if 'logger' in globals():
    # log current file and path
    logger.info("Streamlit App Starting...")
    current_file = os.path.abspath(__file__)
    current_path = os.path.dirname(current_file)
    logger.info(f"Current Working Directory: {os.getcwd()}")
    logger.info(f"running {current_path}, {current_file}")
else:
    # Run the setup function
    raise SystemExit("Error: Logger is not properly configured!")
# Run the setup function
logger.info("Running App setup...")
setup.setup_package()
logger.info("Setup completed successfully.")
# except Exception as e:
#     logger.critical(f"App setup crashed: {e}", exc_info=True)
#     st.error(f"App setup failed. Please check logs. {__name__}")
#     raise SystemExit("App setup failed. Exiting.")

# run political party analysis
try:
    logger.info("Running Menu setup...")
    politicalpartyanalysis.pagesetup()
    logger.info("Menu setup completed successfully.")
except Exception as e:
    logger.critical(f"Menu setup crashed: {e}", exc_info=True)
    st.error(f"Menu setup failed. Please check logs. {__name__}")
    raise SystemExit("Menu setup failed. Exiting.")


# Run the first load function
try:
    # Create a loading message
    loading_message = st.empty()
    # Display a loading message
    loading_message.markdown(
        "<h3 style='text-align: center; color: blue;'>"
        "Please wait while the data sets are being "
        "calculated...</h3>",
        unsafe_allow_html=True,
    )
    initialise_data()  # Load the data
    # Clear the loading message
    loading_message.empty()
except Exception as e:
    logger.critical(f"First load crashed: {e}", exc_info=True)
    st.error(f"Data loading failed. Please check logs. {e}")
    raise SystemExit("Data loading failed. Exiting.")



logger.info("App is fully loaded and ready!")
# The app is now ready to be run.
# To run the app, open a terminal and run:
#  "streamlit run PoliticalPartyAnalysisDashboard.py
# The app will open in a new tab in your default web browser.
