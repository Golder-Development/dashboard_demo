import streamlit as st
import json
import os
import bcrypt
from utils.global_variables import initialize_session_state
from utils.logger import logger
from utils.decorators import log_function_call  # Import decorator


# File paths
def Refresh_Text_Session_State():
    if "FILENAMES" or "DIRECTORIES" not in st.session_state:
        initialize_session_state()


# Function to load admin credentials
def load_credentials():
    if "CREDENTIALS_FILE" not in st.session_state:
        Refresh_Text_Session_State()
    else:
        CREDENTIALS_FILE = st.session_state.get("CREDENTIALS_FILE")
    with open(CREDENTIALS_FILE, "r") as f:
        return json.load(f)


# Function to verify password
def check_password(username, password):
    credentials = load_credentials()
    if username == credentials["admin_username"]:
        return bcrypt.checkpw(
            password.encode(), credentials["admin_password_hash"].encode()
        )
    return False


# Function to load text for a specific page
def load_page_text(pageref_label):
    all_texts = load_all_text()
    return all_texts.get(target_label, {})


# Function to toggle soft delete
def toggle_soft_delete(pageref_label, text_key, delete_status):
    if "TEXT_FILE" not in st.session_state:
        Refresh_Text_Session_State()
    else:
        TEXT_FILE = st.session_state.get("TEXT_FILE")
    all_texts = load_all_text()
    if pageref_label in all_texts and text_key in all_texts[pageref_label]:
        all_texts[pageref_label][text_key]["is_deleted"] = delete_status
        with open(TEXT_FILE, "w", encoding="utf-8") as f:
            json.dump(all_texts, f, indent=4)


# Function to permanently delete a text element
def permanent_delete(pageref_label, text_key):
    if "TEXT_FILE" not in st.session_state:
        Refresh_Text_Session_State()
    else:
        TEXT_FILE = st.session_state.get("TEXT_FILE")
    all_texts = load_all_text()
    if pageref_label in all_texts and text_key in all_texts[pageref_label]:
        del all_texts[pageref_label][text_key]
        if not all_texts[pageref_label]:
            del all_texts[pageref_label]
        with open(TEXT_FILE, "w", encoding="utf-8") as f:
            json.dump(all_texts, f, indent=4)


# Function to load all saved text
def load_all_text():
    if "TEXT_FILE" not in st.session_state:
        Refresh_Text_Session_State()
    else:
        TEXT_FILE = st.session_state.get("TEXT_FILE")
    if os.path.exists(TEXT_FILE):
        with open(TEXT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)  # Returns full dictionary of texts
    return {}  # Return empty dictionary if file doesn't exist


# Function to load text for a specific page
def load_page_text(pageref_label):
    all_texts = load_all_text()
    return all_texts.get(pageref_label, {})  # Return dictionary of text elements


# Function to save text for a specific page and element
def save_text(pageref_label, text_key, new_text):
    if "TEXT_FILE" not in st.session_state:
        Refresh_Text_Session_State()
    else:
        TEXT_FILE = st.session_state.get("TEXT_FILE")
    all_texts = load_all_text()
    if pageref_label not in all_texts:
        all_texts[pageref_label] = {}
    all_texts[pageref_label][text_key] = new_text
    with open(TEXT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_texts, f, indent=4)  # Save updated dictionary
