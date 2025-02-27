"""
Configuration file for the package.
"""

import os
import logging
from utils.version import get_git_version
from utils.global_variables import initialize_session_state


def setup():
    """
    Function to setup the package.
    """
    # Define the directory
    MODULE_DIR = os.path.dirname(__file__)

    # Define the name of the package
    name = "data"
    # Define the version of the package
    __version__ = get_git_version(MODULE_DIR)
    # Define the description of the package
    __description__ = "A package to clean and dedupe data"
    # Define the author of the package
    __author__ = "Paul Golder"
    # Define the email address of the package author
    __author_email__ = "PGOLDER1972@gmail.com"
    # Logging configuration
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        filename="logs\\app_log.log",
        encoding="utf-8",
        level=logging.DEBUG,
    )
    # Define the dependencies of the package
    requirements = ["pandas", "numpy", "scikit-learn", "fuzzywuzzy"]
    # Define the entry points of the package
    entry_points = {"console_scripts": ["data = data.__main__:main"]}
    # Define the package data
    package_data = {"data": ["data/*.csv"]}
    # Define the package classifiers
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
    # Define the package keywords
    keywords = ["data", "cleaning", "deduplication"]
    # Define the package URL
    url = "https://github.com/Golder-Development/dashboard_demo"

    # initialize variables
    initialize_session_state()

    __all__ = [
        "name",
        "__version__",
        "__description__",
        "__author__",
        "__author_email__",
        "logger",
        "requirements",
        "entry_points",
        "package_data",
        "classifiers",
        "keywords",
        "url",
    ]
