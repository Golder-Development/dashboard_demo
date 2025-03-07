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
        mod_corporate_donations_per_entity,
        mod_sponsorships,
        mod_sponsorships_per_entity,
        mod_donations_per_political_party,
        mod_dubious_donations,
        mod_dubious_donations_per_entity,
        mod_dubious_donors,
        mod_dubious_donors_per_entity,
        mod_visits,
        mod_visits_per_regulated_entity,
        mod_regulated_donor_per_entity,
        loginpage,
        logoutpage,
        mod_cash_donations,
        mod_cash_donations_per_entity,
        mod_non_cash_donations,
        mod_non_cash_donations_per_entity,
        mod_publicfund_donations,
        mod_publicfund_donations_per_entity,
    )

    # Create an instance of the MultiPage class
    app = MultiPage(app_name="UK Political Donations")  # Create an instance

    # Add your app pages here using .add_page()
    app.add_page("Introduction", introduction_body)
    app.add_page("Login", loginpage)
    app.add_page("Head Line Figures", hlf_body)
    app.add_page("Cash Donations", mod_cash_donations)
    app.add_page("Non Cash Donations", mod_non_cash_donations)
    app.add_page("Public Fund Donations", mod_publicfund_donations)
    app.add_page("Bequeths", mod_bequeths)
    app.add_page("Corporate Donations", mod_corporate_donations)
    app.add_page("Sponsorships", mod_sponsorships)
    app.add_page("Paid Visits", mod_visits)
    app.add_page("Dubious Donors", mod_dubious_donors)
    app.add_page("Dubious Donations", mod_dubious_donations)
    app.add_page("Cash Donations by...",
                 mod_cash_donations_per_entity)
    app.add_page("Non Cash Donations by...",
                 mod_non_cash_donations_per_entity)
    app.add_page("Public Fund Donations by...",
                 mod_publicfund_donations_per_entity)
    app.add_page("Corporate Donations by...",
                 mod_corporate_donations_per_entity)
    app.add_page("Sponsorship by...", mod_sponsorships_per_entity)
    app.add_page("Paid Visits by...", mod_visits_per_regulated_entity)
    app.add_page("Donors per by...",
                 mod_regulated_donor_per_entity)
    app.add_page("Dubious Donors by...",
                 mod_dubious_donors_per_entity)
    app.add_page("Dubious Donations by...",
                 mod_dubious_donations_per_entity)
    app.add_page("Donations by Political Party",
                 mod_donations_per_political_party)
    app.add_page("Notes on Data and Manipulations", notesondataprep_body)
    app.add_page("Logout", logoutpage)

    # app.add_page("Regulated Entities", regulatedentitypage_body)

    app.run()  # Run the  app
    # End of PoliticalPartyAnalysisDashboard.py
