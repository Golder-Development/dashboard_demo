"""
Configuration file for the package.
"""
import os
from setuptools import setup, find_packages
from utils.logger import logger, log_function_call
from utils.version import get_git_version
from utils.global_variables import initialize_session_state

def setup_package():
    """
    Function to setup the package.
    """
    logger.info("Setting up the package")
    # Define the directory
    MODULE_DIR = os.path.dirname(__file__)
    logger.info(f"Module directory: {MODULE_DIR}")
    # Define the name of the package
    name = "Political Party Analysis Dashboard"
    # Define the version of the package
    try:
        version = get_git_version(MODULE_DIR)
        logger.info(f"Version: {version}")
    except Exception as e:
        logger.error(f"Error getting version: {e}")

    # Define the description of the package
    description = "A package to clean and dedupe data"
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
    entry_points = {"PoliticalPartyAnalysisDashboard": ["main = main:main"]}
    # Define the package data
    package_data = {"data": ["data/Donations_accepted_by_political_parties.csv"]}
    # Define the package classifiers
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
    # Define the package keywords
    keywords = ["data", "cleaning", "deduplication", "political party analysis"]
    # Define the package URL
    url = "https://github.com/Golder-Development/dashboard_demo"
    # initialize variables
    try:
        initialize_session_state()
    except Exception as e:
        logger.error(f"Error initializing session: {e}")
    logger.info("Package setup complete")
