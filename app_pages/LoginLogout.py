import streamlit as st
from app_pages.modular_page_blocks import (check_password)

def login_page():
    # Function to load admin credentials
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False

    if not st.session_state.is_admin:
        st.subheader("Admin Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if check_password(username, password):
                st.session_state.is_admin = True
                st.success("Login successful!")
                st.experimental_rerun()  # Refresh page after login
            else:
                st.error("Invalid username or password.")

def logout_page():
    # Function to logout admin
    if st.session_state.is_admin:
        st.write("---")
        st.subheader("Admin Logout")
        if st.button("Logout"):
            st.session_state.is_admin = False
            st.success("Logout successful!")
            st.experimental_rerun()  # Refresh page after logout
