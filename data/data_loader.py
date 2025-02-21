import streamlit as st

def load_cleaned_data():
    """Load preprocessed dataset from Streamlit session state."""
    return st.session_state.get("data_clean", None)
