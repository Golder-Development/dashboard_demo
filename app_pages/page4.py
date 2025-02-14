import streamlit as st


def page4_body():
    """
    This function displays the content of Page two.
    """
    st.write("# Summary of data per regulated entity")
    st.write("## This is subsection 1")
    st.write("* Here is content for subsection 1")
    st.write("## This is subsection 2")
    st.write("* Here is content for subsection 2")
    st.write("### This is sub-subsection 2")
    st.write("Here other content")
    st.info("* This is made with st.info()")
    st.success("* This is made with st.success()")
    st.warning("* This is made with st.warning()")
    st.error("* This is made with st.error()")
    st.write("---")
