import streamlit as st
import components.calculations as ppcalc


def notesondataprep_body():
    df = st.session_state.get("data_clean", None)
    # set filters to None and filtered_df to the original dataset
    filters = None
    filtered_df = df
    min_date = ppcalc.get_mindate(filtered_df, filters).date()
    max_date = ppcalc.get_maxdate(filtered_df, filters).date()
    electoral_commission = "https://www.electoralcommission.org.uk/"
    wmca = "https://www.wmca.org.uk/"
    datalink = "https://www.kaggle.com/robertjacobson/uk-political-donations"
    # use markdown to create headers and sub headers
    st.write("---")
    st.write("## Notes on Data, Data Preperation and Assumptions")
    st.write("---")
    st.write("### Notes on Data Source")
    st.write(f"* The data covers the period from {min_date} to {max_date}")
    st.write("* The data was sourced from the "
             "[Electoral Commission](%s)." % electoral_commission,
             "Having been initially extracted and "
             "compiled by https://data.world/vizwiz.")
    st.write("* The data is a snapshot of donations made to Political Parties")
    st.write("---")
    st.write("### Data Cleansing and Assumptions")
    st.write("This was built using Streamlit and Python following training "
             "from the [Code Institute](%s)." % "https://codeinstitute.net/"
             "On a Data Analytics and AI Course funded "
             "by the [WMCA](%s)." % wmca)
    st.write("The initial data had the value changed into a numeric format "
             "to enable calculations and visualisations.  It is available from"
             " [Kaggle](%s)." % datalink)
    st.write("The all text based data was the cleaned and transformed "
             "to enable analysis.  The following steps were taken:"
             "Leading and trailing spaces were removed, all text was "
             "converted to Title case, and all special characters were "
             "removed.")
    st.write("The data was then analysed to identify any missing values.  The"
             "following fields were identified as having missing values:")
    st.write("The DonorId and DonorName fields were then analysed to identify"
             "dublicates due to poor data entry.  The following rules were "
             "used to identify duplicates:")
    st.write("The data included records for the Northern Ireland Assembly"
             "and were identified by their own register, these have been "
             "seperated out and are not included in the analysis unless "
             "explicitly stated otherwise.")
    st.write("The data included records for donations from Public Funds "
             "these have been excluded from the analysis unless explicitly "
             "stated otherwise.")
    st.write("Two Donation Types were identified as have exceptionally long"
             " names and so were shortened for ease of use."
             "These were:")
    st.write(" * 'Total value of donations not reported individually' was "
             "changed to 'Aggregated Donation'.")
    st.write(" * 'Permissible Donor Exempt Trust' was changed to 'P.D. Exempt "
             "Trust'.")
    st.write("The data was then cleaned to ensure that every record had a"
             "valid received date, this was achieved by"
             " firstly populating the missing dates with either the Recorded"
             "Date or the Reported Date. If both of these"
             " were also missing then a date was calculated based on the"
             "Reporting Period.  If the value was still blank"
             " then the value was set to 1900-01-01.  All time values were set"
             "to 00:00:00.")
    st.write("The Nature of Donation field was then populated based on the"
             "values in the dataset.  The following rules were used:")
    st.markdown(" *  If the Nature of Donation was already populated then it"
                "was left as is.")
    st.write("  * If the IsBequest field was populated then the Nature of"
             "Donation was set to 'Is A Bequest'.")
    st.write("  * If the IsAggregation field was populated then the Nature of"
             "Donation was set to 'Aggregated Donation'.")
    st.write("  * If the IsSponsorship field was populated then the Nature of"
             "Donation was set to 'Sponsorship'.")
    st.write("  * If the RegulatedDoneeType field was populated then the"
             "Nature of Donation was set to "
             "'Donation to {RegulatedDoneeType}'.")
    st.write("  * If the Nature of Donation was 'Donation to nan' then it was"
             "set to 'Other'.")
    st.write("  * If the Nature of Donation was 'Other Payment' then it was"
             "set to 'Other'.")
    st.write("  * If the DonationAction field was populated then the Nature of"
             "Donation was set to '{DonationAction}'.")
    st.write("  * If the DonationType field was populated then the Nature of"
             " Donation was set to '{DonationType}'.")
    st.write("Regulated Entities were then analysed and categorised based on"
             "the number of donations received. The table below"
             " shows the categories used.")
    st.write("---")
    st.write("## Entity Classification Based on Donations")
    col1, col2 = st.columns(2)
    with col1:
        ppcalc.display_thresholds_table()
    st.write("---")
