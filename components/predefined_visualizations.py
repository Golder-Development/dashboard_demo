import streamlit as st
from components.Visualisations import plot_bar_line_by_year, plot_custom_bar_chart

def display_donations_by_entity(cleaned_c_d_df):
    if cleaned_c_d_df.empty:
        st.write("No data available for the selected filters.")
        return
    else:
        plot_bar_line_by_year(cleaned_c_d_df,
                                XValues="YearReceived",
                                YValue="Value",
                                GGroup="RegulatedEntityType",
                                XLabel="Year",
                                YLabel="Value of Donations £",
                                Title="Value of Donations by Year and"
                                    " Entity",
                                CalcType='sum',
                                use_custom_colors=True,
                                widget_key="Value_by_entity",
                                ChartType='Bar',
                                LegendTitle="Political Entity Type",
                                percentbars=True,
                                use_container_width=True)
    st.write("Most donations are made to Political Parties, this"
                " changed in 2016 with the Brexit Referendum. "
                "Medium size political entities such as 'Vote Leave' and"
                " 'Leave.EU' were very active, but were not"
                " Political Parties."
                " As such they appear as Permitted Participants.")

def display_donations_by_year_and_entity(cleaned_c_d_df):
    plot_bar_line_by_year(cleaned_c_d_df,
                            XValues="YearReceived",
                            YValue="Value",
                            GGroup="RegEntity_Group",
                            XLabel="Year",
                            YLabel="Value of Donations £",
                            Title="Value of Donations by Year and Entity",
                            CalcType='sum',
                            use_custom_colors=True,
                            widget_key="Value_by_entity",
                            ChartType='Bar',
                            LegendTitle="Political Entity",
                            percentbars=False,
                            use_container_width=True)
    st.write("The top 3 political entities by value of donations are "
                "the Conservative Party, the Labour Party and the "
                "Liberal Democrats. This is not surprising as these are "
                "the three main political parties in the UK.")
    st.write("This pattern changes in 2016 to coincide with the EU "
                "Referendum. Here Medium size political entities such "
                "as 'Vote Leave' and 'Leave.EU' were very active.")

def display_donations_by_donor_type(cleaned_c_d_df):
    plot_bar_line_by_year(cleaned_c_d_df,
                            XValues="YearReceived",
                            YValue="Value",
                            GGroup="DonorStatus",
                            XLabel="Year",
                            YLabel="Total Value (£)",
                            Title="Donations Value by Donor Types",
                            CalcType='sum',
                            widget_key="Value by type",
                            use_container_width=True)
    st.write("The majority of cash donations are from individuals. "
                "These are followed by donations from companies and "
                "trade unions.")
    st.write("The pattern of donations by donor type is consistent "
                "over time. This is not surprising as the majority of "
                "donations are from individuals.")

def display_donations_by_donor_type_chart(df):
    plot_custom_bar_chart(df=df,
                            x_column='DonorStatus',
                            y_column='Value',
                            group_column='DonationType',
                            agg_func='sum',
                            title='Total Donations by Donation Type',
                            x_label='Donation Type',  # X-axis label
                            y_label='Donation £',  # Y-axis label
                            orientation='v',  # Vertical bars
                            barmode='stack',  # Grouped bars
                            x_scale='category',
                            y_scale='linear',
                            widget_key='donation_donation_type',
                            use_container_width=True
                            )
    st.write("The majority of cash donations are from individuals. "
                "These are followed by donations from companies and "
                "trade unions.")
    st.write("The pattern of donations by donor type is consistent "
                "over time. This is not surprising as the majority of "
                "donations are from individuals.")