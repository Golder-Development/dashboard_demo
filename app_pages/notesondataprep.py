import streamlit as st


def notesondataprep_body():
    # use markdown to create headers and sub headers
    st.write("# Notes on Data, Data Preperation and Assumptions")
    st.write("## Notes on Data")
    st.write("* The data covers the period from 2001 to 2019")
    st.write("## This is subsection 2")
    st.write("* Here is content for subsection 2")
    # you can play around by adding more sub-sections
    st.write("### This is sub-subsection 2")
    st.write("Here other content")
    # Display a text with informational style.
    st.info("* This is made with st.info()")
    # Display a text with success style.
    st.success("* This is made with st.success()")
    # Display a text with warning style.
    st.warning("* This is made with st.warning()")
    # Display a text with error style.
    st.error("* This is made with st.error()")
    # creates a horizontal line, useful to separate the content in the page
    st.write("---")
