import streamlit as st

def page3_body():
    """
    This function displays the content of Page two.
    """
    ######### Learning Sections #########
    # Display text
    # Display data
    # Display plots
    # Optimize performance
    # Display widgets 
    # Display media


    ################################################################################
    ### Display text ###
    ################################################################################
    st.write("# This is a major section")  # use markdown to create headers and sub headers
    st.write("## This is subsection 1")
    st.write("* Here is content for subsection 1")
    st.write("## This is subsection 2")
    st.write("* Here is content for subsection 2")
    st.write("### This is sub-subsection 2") # you can play around by adding more sub-sections
    st.write("Here other content")
    st.info("* This is made with st.info()") # Display a text with informational style.
    st.success("* This is made with st.success()") # Display a text with success style.
    st.warning("* This is made with st.warning()") # Display a text with warning style.
    st.error("* This is made with st.error()") # Display a text with error style.
    st.write("---")  # creates a horizontal line, useful to separate the content in the page

