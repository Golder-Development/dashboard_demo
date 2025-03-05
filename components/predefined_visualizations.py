import Visualisations
import streamlit as st

def display_donations_by_entity(cleaned_c_d_df):
    if cleaned_c_d_df.empty:
        st.write("No data available for the selected filters.")
        return
    else:
        plot_bar_line(graph_df=cleaned_c_d_df,
                      XValues="YearReceived",
                      YValues="Value",
                      GroupData="RegulatedEntityType",
                      XLabel="Year",
                      YLabel="Value of Donations £",
                      Title="Value of Donations by Year and Entity",
                      CalcType='sum',
                      use_custom_colors=True,
                      widget_key="Value_by_entity",
                      ChartType='Bar',
                      LegendTitle="Political Entity Type",
                      percentbars=True,
                      use_container_width=True)


def display_donations_by_year_and_entity(cleaned_c_d_df):
    plot_bar_line(grapg_df=cleaned_c_d_df,
                  XValues="YearReceived",
                  YValues="Value",
                  GroupData="RegEntity_Group",
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


def display_donations_by_donor_type(cleaned_c_d_df):
    plot_bar_line(graph_df=cleaned_c_d_df,
                  XValues="YearReceived",
                  YValues="Value",
                  GroupData="DonorStatus",
                  XLabel="Year",
                  YLabel="Total Value (£)",
                  Title="Donations Value by Donor Types",
                  CalcType='sum',
                  widget_key="Value by type",
                  use_container_width=True)


def display_donations_by_donor_type_chart(df):
    plot_bar_chart(graph_df=df,
                   XValues='DonorStatus',
                   YValues='Value',
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


def visit_graph1(target_label, cleaned_c_d_df):
    plot_bar_line(graph_df=cleaned_c_d_df,
                  XValues="YearReceived",
                  YValues="Value",
                  GroupData="RegulatedEntityType",
                  XLabel="Year",
                  YLabel="Value of Donations £",
                  Title=f"Value of {target_label}s by Year and"
                        " Entity",
                  CalcType='sum',
                  use_custom_colors=False,
                  widget_key="Value_by_entity",
                  ChartType='Bar',
                  LegendTitle="Political Entity Type",
                  percentbars=True,
                  use_container_width=True)


def visits_graph2(target_label, cleaned_c_d_df):
    plot_bar_line(graph_df=cleaned_c_d_df,
                  XValues="YearReceived",
                  YValues="Value",
                  GroupData="RegEntity_Group",
                  XLabel="Year",
                  YLabel="Value of Donations £",
                  Title=f"Value of {target_label}s by Year and"
                        " Entity",
                  CalcType='sum',
                  use_custom_colors=True,
                  widget_key="Value_by_entity",
                  ChartType='Bar',
                  LegendTitle="Political Entity",
                  percentbars=False,
                  use_container_width=True)


def visits_graph3(target_label, cleaned_c_d_df):
    plot_bar_line(graph_df=cleaned_c_d_df,
                  XValues="YearReceived",
                  YValues="Value",
                  GroupData="DonorStatus",
                  XLabel="Year",
                  YLabel="Total Value (£)",
                  Title=f"{target_label}s Value by Donor Types",
                  CalcType='sum',
                  widget_key="Value by type",
                  use_container_width=True)


def visits_graph4(target_label, cleaned_c_d_df):
    plot_bar_chart(graph_df=cleaned_c_d_df,
                   XValues='DonorStatus',
                   YValues='Value',
                   agg_func='avg',
                   Title=f'Avg {target_label}s Value by Donor Types',
                   XLabel='Donor',  # X-axis label
                   YLabel='Donation £',  # Y-axis label
                   orientation='v',  # Vertical bars
                   barmode='stack',  # Grouped bars
                   x_scale='category',
                   y_scale='linear',
                   color_palette='Set1',
                   widget_key='donation_donation_type',
                   use_container_width=True
                   )
