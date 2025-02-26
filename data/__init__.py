from utils import get_git_version
import os

MODULE_DIR = os.path.dirname(__file__)

__version__ = get_git_version(MODULE_DIR)
__author__ = "Paul Golder"
__author_github__ = "https://github.com/Hysnap"
__description__ = "Data for the project."
