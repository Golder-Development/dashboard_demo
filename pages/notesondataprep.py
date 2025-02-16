import streamlit as st
import calculations as ppcalc


def notesondataprep_body():
    df = st.session_state.get("data_clean", None)
    # set filters to None and filtered_df to the original dataset
    filters = None
    filtered_df = df
    min_date = ppcalc.get_mindate(filtered_df, filters).date()
    max_date = ppcalc.get_maxdate(filtered_df, filters).date()
    electoral_commission = "https://www.electoralcommission.org.uk/"
    # use markdown to create headers and sub headers
    st.write("## Notes on Data, Data Preperation and Assumptions")
    st.write("### Notes on Data Source")
    st.write(f"* The data covers the period from {min_date} to {max_date}")
    st.write("* The data was sourced from the [Electoral Commission](%s)." % electoral_commission,
                "Having been initially extracted and compiled by https://data.world/vizwiz.")
    st.write("* The data is a snapshot of donations made to Political Parties ")
    st.write("### Data Cleansing and Assumptions")
    st.write("* This was built using Streamlit and Python following training "
             "from the [Code Institute](%s)." % "https://codeinstitute.net/", 
             "On a Data Analytics and AI Course funded by the [WMCA](%s)." % "https://www.wmca.org.uk/")
    st.write("* The initial data had the value changed into a numeric format to enable calculations"
             " and visualisations.  It is available from [Kaggle](%s)." % "https://www.kaggle.com/robertjacobson/uk-political-donations")
    st.write("* The data was then cleaned to ensure that every record had a valid received date, this was achieved by"
             " firstly populating the missing dates with either the Recorded Date or the Reported Date. If both of these"
             " were also missing then a date was calculated based on the Reporting Period.  If the value was still blank"
             " then the value was set to 1900-01-01.  All time values were set to 00:00:00.")
    st.write("* Regulated Entities were then analysed and categorised based on the number of donations received. The table below"
             " shows the categories used.")
    st.write("## Entity Classification Based on Donations")
    col1, col2 = st.columns(2)
    with col1:
        ppcalc.display_thresholds_table()
