import streamlit as st
import components.calculations as ppcalc


def notesondataprep_body():
    df = st.session_state.get("data_clean", None)
    # set filters to None and filtered_df to the original dataset
    filters = None
    filtered_df = df
    min_date = ppcalc.get_mindate(filtered_df, filters).date()
    max_date = ppcalc.get_maxdate(filtered_df, filters).date()
    # set the urls for the data sources and references
    code_institute = "https://codeinstitute.net/"
    electoral_commission = "https://www.electoralcommission.org.uk/"
    wmca = "https://www.wmca.org.uk/"
    datalink = "https://www.kaggle.com/robertjacobson/uk-political-donations"
    # use markdown to create headers and sub headers
    st.markdown("---")
    st.markdown("### Notes on Data Source")
    st.markdown(f"* The data covers the period from {min_date} to {max_date}")
    st.markdown(f"* The data was sourced from the " +
        f"[Electoral Commission](%s)." % electoral_commission +
        f"the first version used data compiled by https://data.world/vizwiz, this has now been replaced with the latest data from the Electoral Commission."
    )
    st.markdown("* The data is a snapshot of donations made to Political Parties")
    st.markdown("---")
    st.markdown("### Data Cleansing and Assumptions")
    st.markdown(
        f"This was built using Streamlit and Python following training " +
        f"from the [Code Institute](%s). " % code_institute +
        f"On a Data Analytics and AI Course funded " +
        f"by the [WMCA](%s)." % wmca
    )
    st.markdown("#### Removal of Dublicate Donations")
    st.markdown("The data was deduplicated using python and pandas, to ensure "+
                "no inaccurate double counting of donations. " + 
                " This deduplication was an improvement on implemented in July" +
                " 2025 and will explain variations in reported values.")
    st.markdown("#### Donation Value Cleansing")
    st.markdown(
        "The initial data had the value changed into a numeric format " +
        "by removing the currency sign and commas, then converting to a float " +
        "to enable calculations and visualisations."
    )
    st.markdown("#### Text Based Data Cleaning")
    st.markdown(
        "Then all text based data was cleaned and transformed " +
        "to enable analysis.  The following steps were taken:")
    st.markdown(" * Leading and trailing spaces were removed ")
    st.markdown(" * all text was converted to Title case")
    st.markdown(" * all special characters were removed.")
    st.markdown("#### Donor Entity Cleaning")
    st.markdown(
        " * The DonorId and DonorName fields were then analysed to identify " +
        "dublicates due to poor data entry.  This was preformed using Fuzzy Logic " +
        "to identify similar names and then manually checked to ensure " +
        "the correct donor was identified." +
        " There is an element of subjectivity in this process, and as such may introduce " +
        " some minor errors into the data. " 
    )
    st.markdown("#### Northern Ireland Assembly")
    st.markdown(
        "The data included records for the Northern Ireland Assembly" +
        "and were identified by their own register, these have been " +
        "seperated out and are not included in the analysis unless " +
        "explicitly stated otherwise."
    )
    st.markdown("#### Donations from Public Funds")
    st.markdown(
        "The data included records for donations from Public Funds " +
        "these have been excluded from the analysis unless explicitly " +
        "stated otherwise."
    )
    st.markdown("#### Donations Type labels")
    st.markdown(
        "Two Donation Types were identified as have exceptionally long" +
        " names and so were shortened for ease of use." +
        "These were:"
    )
    st.markdown(
        " * 'Total value of donations not reported individually' was " +
        "changed to 'Aggregated Donation'."
    )
    st.markdown(
        " * 'Permissible Donor Exempt Trust' was changed to 'P.D. Exempt" +
        " Trust'."
    )
    st.markdown("#### Received Date and Time Cleansing and population")
    st.markdown(
        "The data was cleaned to ensure that every record had a " +
        "valid Received Date, this was achieved by populating the missing dates")
    st.markdown(" * with the Recorded Date if present,")
    st.markdown(" * or the Reported Date, if present,")
    st.markdown(" * or a date calculated from the Reporting Period Name.")
    st.markdown(" * If the value was still blank then the value was set to 1900-01-01.")
    st.markdown("All time values were set to 00:00:00."
    )
    st.markdown("#### Nature of Donation Cleansing and Population")
    st.markdown(
        "The Nature of Donation field was populated based on the"
        "values in the dataset.  The following rules were applied in sequence stopping at the first valid one:"
    )
    st.markdown(
        " *  If the Nature of Donation was already populated then it" "was left as is."
    )
    st.markdown(
        "  * If the IsBequest field was populated then the Nature of"
        "Donation was set to 'Is A Bequest'."
    )
    st.markdown(
        "  * If the IsAggregation field was populated then the Nature of"
        "Donation was set to 'Aggregated Donation'."
    )
    st.markdown(
        "  * If the IsSponsorship field was populated then the Nature of"
        "Donation was set to 'Sponsorship'."
    )
    st.markdown(
        "  * If the RegulatedDoneeType field was populated then the "
        "Nature of Donation was set to "
        "'Donation to {RegulatedDoneeType}'."
    )
    st.markdown(
        "  * If the Nature of Donation was 'Donation to nan' then it was"
        "set to 'Other'."
    )
    st.markdown(
        "  * If the Nature of Donation was 'Other Payment' then it was"
        "set to 'Other'."
    )
    st.markdown(
        "  * If the DonationAction field was populated then the Nature of"
        "Donation was set to '{DonationAction}'."
    )
    st.markdown(
        "  * If the DonationType field was populated then the Nature of"
        " Donation was set to '{DonationType}'."
    )
    st.markdown("#### Regulated Entity Classification")
    st.markdown(
        "Regulated Entities were then analysed and categorised based on "
        "the number of donations received during a parliamentary sitting. The table below"
        " shows the categories used."
    )
    st.markdown("---")
    st.markdown("## Entity Classification Based on Donations")
    col1, col2 = st.columns(2)
    with col1:
        ppcalc.display_thresholds_table()
    
    st.write("---")
