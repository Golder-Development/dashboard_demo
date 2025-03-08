import streamlit as st
import json
import os
import bcrypt
from utils.global_variables import initialize_session_state
from utils.logger import logger
from utils.logger import log_function_call  # Import decorator


# File paths
def Refresh_Text_Session_State():
    if "FILENAMES" or "DIRECTORIES" not in st.session_state:
        initialize_session_state()


def load_credentials():
    if "CREDENTIALS_FILE" not in st.session_state:
        Refresh_Text_Session_State()

    CREDENTIALS_FILE = st.session_state.get("CREDENTIALS_FILE", None)
    if not CREDENTIALS_FILE or not os.path.exists(CREDENTIALS_FILE):
        st.error("Credentials file not found!")
        return {}

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
    all_texts = safe_load_json(load_all_text())
    return all_texts.get(pageref_label, {})  # Return dictionary of text elements


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
    """Loads all text data from the JSON file safely."""
    if "TEXT_FILE" not in st.session_state:
        Refresh_Text_Session_State()

    TEXT_FILE = st.session_state.get("TEXT_FILE", None)
    
    if not TEXT_FILE or not os.path.exists(TEXT_FILE):
        return {}  # ✅ Return empty dictionary if file does not exist

    if os.stat(TEXT_FILE).st_size == 0:  # ✅ Check if file is empty
        return {}  # ✅ Return empty dictionary instead of failing on `json.load(f)`

    with open(TEXT_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)  # ✅ Load JSON if file is not empty
        except json.JSONDecodeError:
            st.error("Error: TEXT_FILE contains invalid JSON. Resetting file.")
            return {}  # ✅ Return empty dictionary on JSON error




def save_text(pageref_label, text_key, new_text):
    """Saves text data to the JSON file."""
    if "TEXT_FILE" not in st.session_state:
        Refresh_Text_Session_State()

    TEXT_FILE = st.session_state.get("TEXT_FILE", None)

    if not TEXT_FILE:
        st.error("TEXT_FILE is not set in session state.")
        return

    # Ensure a valid JSON structure exists before writing
    if not os.path.exists(TEXT_FILE) or os.stat(TEXT_FILE).st_size == 0:
        with open(TEXT_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)  # ✅ Initialize file with an empty dictionary

    all_texts = load_all_text()

    if pageref_label not in all_texts:
        all_texts[pageref_label] = {}

    all_texts[pageref_label][text_key] = {"text": new_text, "is_deleted": False}

    with open(TEXT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_texts, f, indent=4)


def load_and_prepare_texts(pageref_label):
    """Loads text elements, converting numbers where needed."""
    page_texts = load_page_text(pageref_label)
    
    for text_key, text_data in page_texts.items():
        text_value = text_data['text']

        # Attempt to convert numbers stored as text
        if isinstance(text_value, str):
            try:
                page_texts[text_key]['text'] = (
                    int(text_value) if text_value.isdigit() else float(text_value)
                )
            except ValueError:
                pass  # Keep as string if conversion fails

    return page_texts


def manage_text_elements(pageref_label):
    """Displays text elements for a page with admin controls (if logged in)."""
    pageref_label_ti = f"{pageref_label}_ti"
    page_texts = load_and_prepare_texts(pageref_label_ti)

    # st.subheader(f"Explanations for {pageref_label_ti}")

    if not page_texts:
        st.info("No text elements available.")
        return  # ✅ Skip the rest of the function

    # # ✅ Show all stored text, regardless of login status
    # for text_key, text_data in page_texts.items():
    #     if not text_data["is_deleted"]:
    #         st.write(f"**{text_key}:** {text_data['text']}")

    # ✅ If user is NOT admin, stop here (No edit controls)
    if not st.session_state.security.get("is_admin", False):
        return  # ✅ Skip the rest of the function

    # ✅ Admin Controls (Editing & Deletion)
    st.subheader(f"Manage Text for {pageref_label_ti}")

    for text_key, text_data in page_texts.items():
        is_deleted = text_data["is_deleted"]
        text_value = text_data["text"]

        if is_deleted:
            st.markdown(f"⚠️ **(Deleted)** {text_key}:")
        else:
            st.text_area(f"Edit {text_key}:", value=text_value, key=f"edit_{text_key}")

        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

        with col1:
            if not is_deleted and st.button(f"Save {text_key}", key=f"save_{text_key}"):
                new_value = st.session_state[f"edit_{text_key}"]
                save_text(pageref_label, text_key, new_value)
                st.success(f"Updated {text_key}!")

        with col2:
            if not is_deleted and st.button(f"Soft Delete {text_key}", key=f"delete_{text_key}"):
                toggle_soft_delete(pageref_label, text_key, True)
                st.warning(f"Soft Deleted {text_key}!")
                st.rerun()

        with col3:
            if is_deleted and st.button(f"Restore {text_key}", key=f"restore_{text_key}"):
                toggle_soft_delete(pageref_label, text_key, False)
                st.success(f"Restored {text_key}!")
                st.rerun()

        with col4:
            if st.button(f"🗑️ Delete {text_key}", key=f"perm_delete_{text_key}"):
                permanent_delete(pageref_label, text_key)
                st.error(f"Permanently Deleted {text_key}!")
                st.rerun()

    # ✅ Add New Text (Admin Only)
    st.subheader("Add a New Text Element")
    new_key = st.text_input("New Text Element Name:")
    new_value = st.text_area("Text Content:")

    if st.button("Add Text Element"):
        if new_key.strip() == "":
            st.error("Text Element Name cannot be empty.")
        elif new_key in page_texts:
            st.error("A text element with this name already exists.")
        else:
            save_text(pageref_label_ti, new_key, new_value)
            st.success(f"Added {new_key}!")
            st.rerun()

def display_text_elements(pageref_label, target_label):
    """Displays stored text elements for a given page."""
    page_texts = load_and_prepare_texts(pageref_label)

    st.subheader(f"Explanations for {target_label}")
    for text_key, text_data in page_texts.items():
        if not text_data["is_deleted"]:
            st.write(f"**{text_key}:** {text_data['text']}")


def safe_load_json(data):
    """Convert JSON string to dictionary safely."""
    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            st.error("Error decoding JSON.")
            return {}
    return data
