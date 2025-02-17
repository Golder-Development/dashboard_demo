import streamlit as st
import calculations as ppcalc
#import Visualisations as vis


def donorsheadlinespage_body():
    """
    This function displays the content of Page two.
    """
    donors_df = st.session_state.get("data_clean", None)
    donors = ppcalc.get_donors_ct(donors_df)
    donations = ppcalc.get_donations_ct(donors_df)
    totaldonations = ppcalc.get_value_total(donors_df)
    min_date = ppcalc.get_mindate(donors_df).date()
    max_date = ppcalc.get_maxdate(donors_df).date()
    st.write("# Analysis of Political Donations by Donor")
    col1, col2 = st.columns(2)
    with col1:
        st.write("## Headline Figures")
        st.write(f"* Between {min_date} and {max_date}, {donors} made "
                 f"{donations} these were worth £{totaldonations}")
        #create x,y graph showing average donor donation vs total number of donations per donor with size of circle set to number of regulated entities donated to.
        
        
        
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
