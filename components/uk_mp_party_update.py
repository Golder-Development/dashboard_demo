import requests
# import pandas as pd
from datetime import datetime


def get_mp_party(mp_name, event_date):
    """
    Fetches the political party an MP belonged to on a specific date.
    """
    base_url = "https://members-api.parliament.uk/api/Members/Search"
    params = {"Name": mp_name}

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return None  # Failed request

    data = response.json()
    if "items" not in data or len(data["items"]) == 0:
        return None  # MP not found

    mp_id = data["items"][0]["value"]["id"]  # Extract MP ID
    party_url = f"https://members-api.parliament.uk/api/Members/{mp_id}/parties"

    response = requests.get(party_url)
    if response.status_code != 200:
        return None  # Failed request

    party_data = response.json()
    for party in party_data.get("items", []):
        start_date = datetime.strptime(party["value"]["startDate"], "%Y-%m-%dT%H:%M:%S")
        end_date = (datetime.strptime(party["value"].get("endDate"), "%Y-%m-%dT%H:%M:%S")
                    if party["value"].get("endDate") else None)
        event_datetime = datetime.strptime(event_date, "%Y-%m-%d")

        if start_date <= event_datetime and (end_date is None or event_datetime <= end_date):
            return party["value"]["party"]["name"]

    return None  # No party found for the given date


"""
# Example usage
mp_events = [
    {"name": "Keir Starmer", "event_date": "2021-06-15"},
    {"name": "Boris Johnson", "event_date": "2019-07-23"},
    {"name": "Theresa May", "event_date": "2016-07-13"}
]

# Updating list with party information
for event in mp_events:
    event["party"] = get_mp_party(event["name"], event["event_date"])

# Convert to DataFrame and display
df = pd.DataFrame(mp_events)
print(df)
"""
