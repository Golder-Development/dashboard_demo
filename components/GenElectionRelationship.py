# Original Code https://github.com/Hysnap/ElectionDateDifferentialCalc/
# Module to calculate the difference in a definable period between a given
# date and the nearest election date, for a set period defined in Days
# Direction can be "DaysTill" or "DaysSince"
import math
import datetime as dt
import pdpy
import streamlit as st
from utils.logger import logger
from utils.logger import log_function_call  # Import decorator

@log_function_call
def load_election_dates():
    """
    Load the general election dates from the pdpy.elections module.

    Returns:
        dict: A dictionary of general election dates.
    """
    #returns elections name, dissolution date, election date
    ElectionDates_dict = pdpy.get_general_elections_dict()
    print(ElectionDates_dict)
    # Create List of Election Dates from ElectionDates_dict
    ElectionDates = []
    for key in ElectionDates_dict.keys():
        # load key, election date
        ElectionDates.append(ElectionDates_dict[key, "election_date"])

    ## List of Election Dates
    # ElectionDates_old = [
    #     "2001/06/07 00:00:00",
    #     "2005/05/05 00:00:00",
    #     "2010/06/05 00:00:00",
    #     "2015/07/05 00:00:00",
    #     "2017/07/05 00:00:00",
    #     "2019/12/12 00:00:00",
    #     "2024/07/04 00:00:00",
    # ]
    st.session_state.ElectionDates = ElectionDates
    logger.info("Election Dates Loaded")

@log_function_call
def GenElectionRelation2(
    R_Date, divisor=1, direction="DaysTill", date_format="%Y/%m/%d %H:%M:%S"
        ):
    """
    Calculate the difference in a definable period between a given date and
    the nearest election date.

    Parameters:
        R_Date (str): The reference date in string format.
        divisor (int): The unit divisor to group days (e.g., 7 for weeks,
                        1 for days) defaults to 1 if not provided.
        direction (str): The direction to calculate ("DaysTill" or "DaysSince")
                        , defaults to "DaysTill" if not provided.
        date_format (str): The date format of the input R_Date string defaults
                        to "%Y/%m/%d %H:%M:%S" is none provided

    Returns:
        int: The calculated difference in the specified period, or 0 if no
              match is found.
    """
    # Load Election Dates
    if "ElectionDates" not in st.session_state:
        logger.info("Election Dates not loaded, loading now")
        load_election_dates()

    # Pre-sorted lists of election dates
    logger.info("Sorting Election Dates")
    ElectionDatesAscend = sorted(st.session_state.ElectionDates)
    ElectionDatesDescend = sorted(st.session_state.ElectionDates, reverse=True)

    try:
        # Convert the reference date to datetime
        R_Date2 = dt.datetime.strptime(R_Date, date_format)

        # Use the appropriate election date list based on direction
        if direction == "DaysTill":
            for ED in ElectionDatesAscend:
                ED2 = dt.datetime.strptime(ED, date_format)
                if R_Date2 <= ED2:
                    DaysDiff = (ED2 - R_Date2).days
                    return math.ceil(DaysDiff / divisor)
        elif direction == "DaysSince":
            for ED in ElectionDatesDescend:
                ED2 = dt.datetime.strptime(ED, date_format)
                if R_Date2 >= ED2:
                    DaysDiff = (R_Date2 - ED2).days
                    return math.ceil(DaysDiff / divisor)

        # If no match is found
        return 0

    except Exception as e:
        # Handle invalid date formats or other errors
        print(f"Error: {e}")
        return None


"""
# Example usage with a DataFrame
if __name__ == "__main__":
    # Example DataFrame
    data = {'ReceivedDate': ['2019/01/01 00:00:00', '2023/01/01 00:00:00']}
    df = pd.DataFrame(data)

    # Apply the function to calculate days till the next election
    df['WeeksTillNextElection'] = df['ReceivedDate'].apply(
        lambda x: GenElectionRelation2(x, divisor=7, direction="DaysTill")
    )

    # Apply the function to calculate days since the last election
    df['WeeksSinceLastElection'] = df['ReceivedDate'].apply(
        lambda x: GenElectionRelation2(x, divisor=7, direction="DaysSince")
    )

    print(df)
"""
