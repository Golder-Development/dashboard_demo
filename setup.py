"""
Configuration file for the package.
"""
import os
import streamlit as st
from utils.logger import logger, log_function_call
from utils.version import get_git_version
from utils.global_variables import initialize_session_state


@log_function_call
def setup_package():
    """
    Function to setup the package.
    """
    # log current file and path
    logger.info("Setting up the package")
    # Define the directory
    MODULE_DIR = os.path.dirname(__file__)
    logger.info(f"Module directory: {MODULE_DIR}")
    # Define the name of the package
    packagename = "Political Party Analysis Dashboard"
    # Define the version of the package
    try:
        version = get_git_version(MODULE_DIR)
        logger.info(f"Version: {version}")
    except Exception as e:
        logger.critical(f"App setup crashed: {e}", exc_info=True)
        st.error(f"App setup failed. Please check logs. {e}")
        raise SystemExit("App setup failed. Exiting.")
    # Define the description of the package
    packagedescription = "A package to clean and dedupe data"
    # Define the author of the package
    author = "Paul Golder"
    # Define the email address of the package author
    author_email = "PGOLDER1972@gmail.com"
    # Define the dependencies of the package
    requirements = [
        "setuptools",
        "numpy",
        "scipy",
        "pandas",
        "matplotlib",
        "seaborn",
        "plotly",
        "patsy",
        "statsmodels",
        "rapidfuzz",
        "streamlit",
        "pytest",
        "bcrypt"
    ]
    # Define the entry points of the package
    packageentry_points = {"PoliticalPartyAnalysisDashboard": ["main = main:main"]}
    # Define the package data
    package_data = {"data": ["source/Donations_accepted_by_political_parties.csv"]}
    # Define the package classifiers
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
    # Define the package keywords
    packagekeywords = ["data", "cleaning", "deduplication", "political party analysis"]
    # Define the package URL
    packageurl = "https://github.com/Golder-Development/dashboard_demo"
    # initialize variables
    try:
        initialize_session_state()
        logger.info("Package setup complete")
    except Exception as e:
        logger.critical(f"App setup crashed: {e}", exc_info=True)
        st.error(f"App setup failed. Please check logs. {e}")
        raise SystemExit("App setup failed. Exiting.")
    return
