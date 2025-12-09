from utils.logger import log_function_call


@log_function_call
def pagesetup():
    # Description: This is the main file to set up the menu
    # from app_pages import introduction
    from app_pages.multi_page import MultiPage
    from app_pages.introduction import introduction_body
    from app_pages.headlinefigures import hlf_body
    from app_pages.notesondataprep import notesondataprep_body
    from app_pages.mod_page_calls import (
        mod_bequeths,
        mod_corporate_donations,
        mod_sponsorships,
        mod_donations_per_political_party,
        mod_dubious_donations,
        mod_dubious_donors,
        mod_visits,
        loginpage,
        logoutpage,
        mod_cash_donations,
        mod_non_cash_donations,
        mod_publicfund_donations,
        mod_regulated_donor_per_entity,
        mod_regulated_entity_per_donor
    )
    from app_pages.donor_loyalty_analysis import mod_donor_loyalty
    from app_pages.donor_type_analysis import mod_donor_type

    # Create an instance of the MultiPage class
    app = MultiPage(app_name="UK Political Donations")  # Create an instance

    # Add your app pages here using .add_page()
    app.add_page("Introduction", introduction_body)
    app.add_page("Login", loginpage)
    app.add_page("Head Line Figures", hlf_body)
    app.add_page("Cash Donations", mod_cash_donations)
    app.add_page("Non Cash Donations", mod_non_cash_donations)
    app.add_page("Public Fund Donations", mod_publicfund_donations)
    app.add_page("Bequests", mod_bequeths)
    app.add_page("Corporate Donations", mod_corporate_donations)
    app.add_page("Sponsorships", mod_sponsorships)
    app.add_page("Paid Visits", mod_visits)
    app.add_page("Dubious Donors", mod_dubious_donors)
    app.add_page("Dubious Donations", mod_dubious_donations)
    app.add_page("Internal Political Party Donations",
                 mod_donations_per_political_party)
    app.add_page("Regulated Donor per Entity",
                 mod_regulated_donor_per_entity)
    app.add_page("Regulated Entity per Donor",
                 mod_regulated_entity_per_donor)
    app.add_page("Donor Loyalty Analysis", mod_donor_loyalty)
    app.add_page("Donor Type Analysis", mod_donor_type)
    app.add_page("Notes on Data and Manipulations", notesondataprep_body)
    app.add_page("Logout", logoutpage)

    # app.add_page("Regulated Entities", regulatedentitypage_body)

    app.run()  # Run the  app
    # End of PoliticalPartyAnalysisDashboard.py
