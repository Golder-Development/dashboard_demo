import requests
import datetime

# UK Parliament API URL for elections
API_URL = "https://members.parliament.uk/api/Elections"

def get_uk_election_dates_since_2000():
    response = requests.get(API_URL)
    
    if response.status_code != 200:
        print("Error fetching data from UK Parliament API")
        return []

    data = response.json()

    elections = []
    for election in data.get("items", []):
        start_date = election.get("startDate")
        election_type = election.get("electionType", {}).get("name", "Unknown Type")
        election_name = election.get("name", "Unknown Election")

        if start_date:
            election_date = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
            if election_date.year >= 2000:
                elections.append((election_name, election_type, election_date.date()))
    
    return elections

# Fetch and print election details
elections_since_2000 = get_uk_election_dates_since_2000()
for name, e_type, date in elections_since_2000:
    print(f"{name} ({e_type}): {date}")