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
        mod_bequeths_page,
        mod_corporate_donations_page,
        mod_corporate_donations_per_entity_page,
        mod_corporate_donations_per_donor_page,
        mod_sponsorship_page,
        mod_sponsorships_per_entity_page,
        mod_sponsorships_per_donor_page,
        mod_donations_per_political_party_page,
        mod_dubious_donations_page,
        mod_dubious_donations_per_entity_page,
        mod_dubious_donations_per_donor_page,
        mod_dubious_donors_page,
        mod_dubious_donors_per_entity_page,
        mod_sponsorships_per_entity_page,
        mod_visits_page,
        mod_visits_per_regulated_entity,
        mod_visits_per_donor,     
        mod_regulated_donor_per_entity_page,
        mod_regulated_entity_per_donors_page,
        loginpage,
        logoutpage,
    )

    # Create an instance of the MultiPage class
    app = MultiPage(app_name="UK Political Donations")  # Create an instance

    # Add your app pages here using .add_page()
    app.add_page("Introduction", introduction_body)
    app.add_page("Login", loginpage)
    app.add_page("Head Line Figures", hlf_body)
    app.add_page("Bequeths", mod_bequeths_page)
    app.add_page("Corporate Donations", mod_corporate_donations_page)
    app.add_page("Sponsorships", mod_sponsorship_page)
    app.add_page("Paid Visits", mod_visits_page)
    app.add_page("Dubious Donors", mod_dubious_donors_page)
    app.add_page("Dubious Donations", mod_dubious_donations_page)
    app.add_page("Corporate Donations per Entity", mod_corporate_donations_per_entity_page)
    app.add_page("Sponsorship per Entity ", mod_sponsorships_per_entity_page)
    app.add_page("Paid Visits per Entity", mod_visits_per_regulated_entity)
    app.add_page("Donors per Regulated Entity", mod_regulated_entity_per_donors_page)    
    app.add_page("Dubious Donors per Regulated Entity", mod_dubious_donors_per_entity_page)
    app.add_page("Dubious Donations per Regulated Entity", mod_dubious_donations_per_entity_page)
    app.add_page("Corporate Donations per Donor", mod_corporate_donations_per_donor_page)
    app.add_page("Sponsorships per Donor", mod_sponsorships_per_donor_page)
    app.add_page("Paid Visits per Donor", mod_visits_per_donor)
    app.add_page("Regulated Entities per Donor", mod_regulated_donor_per_entity_page)
    app.add_page("Dubious donations per Donor", mod_dubious_donations_per_donor_page)
    app.add_page("Donations by Political Party", mod_donations_per_political_party_page)
    app.add_page("Notes on Data and Manipulations", notesondataprep_body)
    app.add_page("Logout", logoutpage)

    # app.add_page("Regulated Entities", regulatedentitypage_body)

    app.run()  # Run the  app
    # End of PoliticalPartyAnalysisDashboard.py
