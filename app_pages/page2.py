import streamlit as st
import datasetupandclean as dc

df = dc.load_data()  # Load the data

def hlf_body():
    """
    This function displays the content of Page two.
    """
    st.write("# Topline Summary of Political Donations to the UK Political Parties")
    st.write("## Headline Figures")
    
    col1, col2 =st.columns(2)
    with col1:
        st.write("* 1,384 regulated bodies received donations")
        st.write("* £1,090M donated in total")
    with col2:
            # use data from the dataset
        st.write("## Displaying data from the dataset")
        st.write("* Here is a sample of the data from the dataset")
        st.write(df.head())  # Display the first 5 rows of the dataset
        st.write("* Here is a summary of the data from the dataset")
        st.write(df.describe())  # Display the summary statistics of the dataset
        st.write("---")  # creates a horizontal line, useful to separate the content in the page