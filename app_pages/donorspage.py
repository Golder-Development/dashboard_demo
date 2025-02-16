import streamlit as st


def donorspage_body():
    """
    This function displays the content of Page two.
    """
    df = st.session_state.get("data", None)
    regulatedentities = df["RegulatedEntityName"].nunique()
    totaldonations = df['Value'].sum()
    st.write("# Topline Summary of Political Donations to the UK Political "
             "Parties")
    col1, col2 = st.columns(2)
    with col1:
        st.write("## Headline Figures")
        st.write(f"* {regulatedentities} regulated bodies received donations")
        st.write(f"* £{totaldonations} donated in total")
    with col2:
        # use data from the dataset
        st.write("## Displaying data from the dataset")
        st.write("* Here is a sample of the data from the dataset")
        if df is not None:
            # Display the first 5 rows of the dataset
            st.write(df.describe())
        else:
            st.error("Data not found. Please check dataset loading in the "
                     "main app.")
        st.write("Top 5 rows of the dataset:")
        if df is not None:
            # Display the summary statistics of the dataset
            st.write(df.head())
        else:
            st.error("Data not found. Please check dataset loading in the "
                     "main app.")
    st.write("## Next Steps")
