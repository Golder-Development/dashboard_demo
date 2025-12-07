"""
Donor Loyalty Analysis Page
Analyzes whether donors are loyal to particular parties or follow those in power.
"""
import streamlit as st
import pandas as pd
import numpy as np
from utils.logger import log_function_call
from components.calculations import calculate_agg_by_variable
from utils.logger import logger


# Government power timeline
GOVERNMENT_TIMELINE = {
    1979: {'party': 'Conservative', 'start': 1979, 'end': 1997},
    1997: {'party': 'Labour', 'start': 1997, 'end': 2010},
    2010: {'party': 'Conservative', 'start': 2010, 'end': 2024},
    2024: {'party': 'Labour', 'start': 2024, 'end': 2025},
}


def get_government_party(year):
    """Get the party in government for a given year"""
    for election_year in sorted(GOVERNMENT_TIMELINE.keys(), reverse=True):
        if year >= election_year:
            return GOVERNMENT_TIMELINE[election_year]['party']
    return 'Unknown'


def extract_year_from_parliamentary_sitting(sitting):
    """Extract year from parliamentary sitting identifier"""
    try:
        return int(str(sitting))
    except (ValueError, TypeError):
        return None


@log_function_call
def mod_donor_loyalty():
    """
    Main function to display donor loyalty analysis
    Analyzes donor behavior across different government periods
    """
    st.header("Donor Loyalty Analysis")
    st.markdown("""
    This page analyzes whether political donors show:
    - **Party Loyalty**: Consistent support for the same party(ies)
    - **Power Following**: Increased donations when their preferred party is in power
    - **Power Switching**: Switching donations to the party in power regardless of preference
    """)
    
    # Get the cleaned data
    if st.session_state.get("data_clean") is None:
        st.warning("Data not loaded. Please go to the main page first.")
        return
    
    df = st.session_state.get("data_clean")
    
    # Filter to only parties (exclude individuals and other entities)
    # Focus on RegulatedEntityName that are actual parties
    parties_list = [
        'Conservative And Unionist Party',
        'Labour Party',
        'Liberal Democrats',
        'Scottish National Party (Snp)',
        'Green Party',
        'Plaid Cymru - Party Of Wales',
        'Reform UK',
        'Uk Independence Party (Ukip)',
    ]
    
    # Get donor data
    donor_df = df[df['DonorName'].notna()].copy()
    
    # Create tabs for different analyses
    tab1, tab2, tab3 = st.tabs([
        "Donor Distribution Across Parties",
        "Donor Behavior by Government Period",
        "Loyalty Metrics"
    ])
    
    with tab1:
        st.subheader("Which parties receive donations from the same donors?")
        display_donor_distribution(donor_df, parties_list)
    
    with tab2:
        st.subheader("Do donor patterns change when parties are in power?")
        display_government_period_analysis(donor_df, parties_list)
    
    with tab3:
        st.subheader("Donor Loyalty Metrics")
        display_loyalty_metrics(donor_df, parties_list)


@log_function_call
def display_donor_distribution(donor_df, parties_list):
    """
    Show which donors give to multiple parties and the patterns
    """
    st.write("""
    This analysis shows donors who gave to multiple parties, indicating whether 
    they have preferred parties or spread donations across the political spectrum.
    """)
    
    # Count parties donated to per donor
    donor_party_counts = donor_df.groupby('DonorName')['PartyName'].nunique()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Total Donors",
            f"{len(donor_party_counts):,}"
        )
    with col2:
        loyal_donors = (donor_party_counts == 1).sum()
        st.metric(
            "Single-Party Donors",
            f"{loyal_donors:,}",
            f"{100*loyal_donors/len(donor_party_counts):.1f}%"
        )
    with col3:
        multi_party_donors = (donor_party_counts > 1).sum()
        st.metric(
            "Multi-Party Donors",
            f"{multi_party_donors:,}",
            f"{100*multi_party_donors/len(donor_party_counts):.1f}%"
        )
    with col4:
        avg_parties = donor_party_counts.mean()
        st.metric(
            "Avg Parties per Donor",
            f"{avg_parties:.2f}"
        )
    
    # Show distribution
    st.write("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Distribution of parties per donor:**")
        party_dist = donor_party_counts.value_counts().sort_index()
        st.bar_chart(party_dist)
    
    with col2:
        st.write("**Top 10 donors by party diversity:**")
        top_diverse = donor_party_counts.nlargest(10)
        for donor, count in top_diverse.items():
            st.write(f"- {donor}: {count} parties")


@log_function_call
def display_government_period_analysis(donor_df, parties_list):
    """
    Analyze donor behavior across government periods
    """
    st.write("""
    This analysis compares donation patterns before, during, and after
    each party is in government.
    """)
    
    # Extract year from parliamentary_sitting
    donor_df['Year'] = donor_df['parliamentary_sitting'].apply(
        extract_year_from_parliamentary_sitting
    )
    
    # Get government party for each year
    donor_df['Government_Party'] = donor_df['Year'].apply(get_government_party)
    
    # Normalize party names for comparison
    donor_df['Party_Normalized'] = donor_df['PartyName'].apply(
        lambda x: 'Conservative' if 'Conservative' in str(x) else
                  'Labour' if 'Labour' in str(x) else
                  'Liberal Democrat' if 'Liberal' in str(x) else
                  'SNP' if 'Scottish' in str(x) else
                  'Other'
    )
    
    # Filter to major parties
    major_parties_norm = ['Conservative', 'Labour', 'Liberal Democrat']
    donor_df_major = donor_df[donor_df['Party_Normalized'].isin(major_parties_norm)].copy()
    
    # Create analysis by government period
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Donation counts by party and government status:**")
        
        # Aggregate donations for each government period
        pivot_data = []
        for gov_year in sorted([1979, 1997, 2010, 2024]):
            gov_party = GOVERNMENT_TIMELINE[gov_year]['party']
            gov_end = GOVERNMENT_TIMELINE[gov_year]['end']
            
            period_df = donor_df_major[
                (donor_df_major['Year'] >= gov_year) &
                (donor_df_major['Year'] < gov_end)
            ]
            
            for party in major_parties_norm:
                party_donations = len(period_df[
                    period_df['Party_Normalized'] == party
                ])
                # Only add if there are donations to avoid empty rows
                if party_donations > 0:
                    pivot_data.append({
                        'Government': gov_party,
                        'Receiving Party': party,
                        'Donations': party_donations
                    })
        
        if pivot_data:
            pivot_df = pd.DataFrame(pivot_data)
            # Group by Government and Receiving Party to avoid duplicates
            pivot_df = pivot_df.groupby(['Government', 'Receiving Party'], as_index=False)['Donations'].sum()
            pivot_display = pivot_df.pivot_table(
                index='Receiving Party',
                columns='Government',
                values='Donations',
                aggfunc='sum'
            )
            st.dataframe(pivot_display.fillna(0).astype(int))
        else:
            st.info("No donation data available for major parties")
    
    with col2:
        st.write("**Average donation value by government period:**")
        
        value_data = []
        for gov_year in sorted([1979, 1997, 2010, 2024]):
            gov_party = GOVERNMENT_TIMELINE[gov_year]['party']
            gov_end = GOVERNMENT_TIMELINE[gov_year]['end']
            
            period_df = donor_df[
                (donor_df['Year'] >= gov_year) &
                (donor_df['Year'] < gov_end)
            ]
            
            if len(period_df) > 0:
                avg_value = period_df['Value'].mean()
                total_value = period_df['Value'].sum()
                
                value_data.append({
                    'Period': f"{gov_party} ({gov_year})",
                    'Avg Donation': avg_value,
                    'Total': total_value
                })
        
        if value_data:
            value_df = pd.DataFrame(value_data)
            st.dataframe(value_df.style.format({
                'Avg Donation': '${:,.2f}',
                'Total': '${:,.0f}'
            }))
        else:
            st.info("No value data available")


@log_function_call
def display_loyalty_metrics(donor_df, parties_list):
    """
    Calculate and display loyalty metrics
    """
    st.write("""
    **Loyalty Score**: Higher score = more consistent support for same party
    
    Calculated as: (Donations to most-donated party) / (Total donations)
    """)
    
    # Calculate loyalty for each donor
    loyalty_list = []
    donor_party_donations = donor_df.groupby(
        ['DonorName', 'PartyName']).size().reset_index(name='count')
    
    for donor in donor_df['DonorName'].unique():
        donor_donations = donor_party_donations[
            donor_party_donations['DonorName'] == donor
        ]
        if len(donor_donations) > 0:
            max_to_one_party = donor_donations['count'].max()
            total_donations = donor_donations['count'].sum()
            loyalty = (max_to_one_party / total_donations
                       if total_donations > 0 else 0)

            loyalty_list.append({
                'Donor': donor,
                'Loyalty_Score': float(loyalty),
                'Parties_Count': len(donor_donations),
                'Total_Donations': total_donations,
                'Top_Party': donor_donations.loc[
                    donor_donations['count'].idxmax(), 'PartyName'
                ]
            })
    
    if loyalty_list:
        # Create dataframe from list instead of transposing
        loyalty_df = pd.DataFrame(loyalty_list)
        # Ensure Loyalty_Score is numeric
        loyalty_df['Loyalty_Score'] = loyalty_df['Loyalty_Score'].astype(float)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Avg Loyalty Score",
                f"{loyalty_df['Loyalty_Score'].mean():.2f}"
            )
        with col2:
            loyal_count = (loyalty_df['Loyalty_Score'] >= 0.8).sum()
            loyal_pct = loyal_count / len(loyalty_df) * 100
            st.metric("Very Loyal Donors (≥0.8)", f"{loyal_pct:.1f}%")
        with col3:
            diversified_count = (loyalty_df['Loyalty_Score'] < 0.6).sum()
            diversified_pct = diversified_count / len(
                loyalty_df) * 100
            st.metric(
                "Diversified Donors (<0.6)",
                f"{diversified_pct:.1f}%"
            )
        with col4:
            single_count = (loyalty_df['Parties_Count'] == 1).sum()
            single_pct = single_count / len(loyalty_df) * 100
            st.metric("Single-Party Donors", f"{single_pct:.1f}%")
        
        st.write("---")
        st.write("**Distribution of loyalty scores:**")
        
        col1, col2 = st.columns(2)
        with col1:
            # Create loyalty score histogram data
            hist_counts = pd.Series({
                '0.0-0.2': len(loyalty_df[
                    (loyalty_df['Loyalty_Score'] >= 0.0) &
                    (loyalty_df['Loyalty_Score'] <= 0.2)
                ]),
                '0.2-0.4': len(loyalty_df[
                    (loyalty_df['Loyalty_Score'] > 0.2) &
                    (loyalty_df['Loyalty_Score'] <= 0.4)
                ]),
                '0.4-0.6': len(loyalty_df[
                    (loyalty_df['Loyalty_Score'] > 0.4) &
                    (loyalty_df['Loyalty_Score'] <= 0.6)
                ]),
                '0.6-0.8': len(loyalty_df[
                    (loyalty_df['Loyalty_Score'] > 0.6) &
                    (loyalty_df['Loyalty_Score'] <= 0.8)
                ]),
                '0.8-1.0': len(loyalty_df[
                    (loyalty_df['Loyalty_Score'] > 0.8) &
                    (loyalty_df['Loyalty_Score'] <= 1.0)
                ]),
            })
            st.bar_chart(hist_counts)
        
        with col2:
            st.write("**Top donors by loyalty score:**")
            top_loyal = loyalty_df.nlargest(10, 'Loyalty_Score')[
                ['Donor', 'Loyalty_Score', 'Parties_Count', 'Top_Party']
            ]
            st.dataframe(top_loyal.style.format({'Loyalty_Score': '{:.2%}'}))
        
        # Power followers analysis
        st.write("---")
        st.subheader("Power Followers Detection")
        st.write("""
        A "power follower" donor switches donations to the party
        in government or increases donations significantly when
        their party gains power.
        """)

        # Simplified detection - donors with lower loyalty
        # to multiple parties
        power_followers = loyalty_df[
            (loyalty_df['Loyalty_Score'] < 0.7) &
            (loyalty_df['Parties_Count'] > 1)
        ]

        st.metric(
            "Potential Power Followers",
            f"{len(power_followers)} donors",
            f"{len(power_followers)/len(loyalty_df)*100:.1f}% of total"
        )

        if len(power_followers) > 0:
            st.write(
                "Sample power followers (donors giving to "
                "multiple parties):"
            )
            st.dataframe(power_followers.head(10).style.format(
                {'Loyalty_Score': '{:.2%}'}
            ))
