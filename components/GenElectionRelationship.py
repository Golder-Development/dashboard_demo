import math
import datetime as dt
import bisect
import streamlit as st
from pdpy.elections import get_general_elections_dict
from utils.logger import logger
from utils.logger import log_function_call  # Import decorator


@log_function_call
@st.cache_data
def load_election_dates():
    """Load general election dates into session state."""
    try:
        ElectionDates_dict = get_general_elections_dict()
        logger.debug(f"ElectionDatesDict: {ElectionDates_dict}")

        # Extract only election dates as `date` objects
        election_dates = [
            value["election"]  # Extract the election date
            for key, value in ElectionDates_dict.items()
            # Ensure structure is valid
            if isinstance(value, dict) and "election" in value
        ]

        if not election_dates:
            raise ValueError("No valid election dates found.")

        # Store sorted election dates in session state
        st.session_state.ElectionDatesAscend = sorted(election_dates)
        st.session_state.ElectionDatesDescend = sorted(election_dates,
                                                       reverse=True)

        logger.info("Election Dates Loaded Successfully.")

    except Exception as e:
        logger.error(f"Failed to load election dates: {e}")
        st.session_state.ElectionDatesAscend = []
        st.session_state.ElectionDatesDescend = []


def GenElectionRelation2(R_Date, divisor=1,
                         direction="DaysTill",
                         date_format="%Y/%m/%d %H:%M:%S"):
    """
    Calculate the difference in days/weeks between a given date and
    the nearest election date.

    Args:
        R_Date (str): The reference date in string format.
        divisor (int): The unit divisor (e.g., 7 for weeks, 1 for days).
        Defaults to 1. direction (str): "DaysTill" (next election)
        or "DaysSince"
        (previous election). Defaults to "DaysTill".
        date_format (str): The format of R_Date (default: "%Y/%m/%d %H:%M:%S").

    Returns:
        int: Days/weeks difference (rounded up if necessary),
        or None on failure.
    """
    # Ensure election dates are loaded
    if ("ElectionDatesAscend" not in st.session_state or
            "ElectionDatesDescend" not in st.session_state):
        logger.info("Election Dates not found in session, loading now.")
        load_election_dates()

    if not st.session_state.ElectionDatesAscend:
        logger.error("Election dates could not be loaded. Returning None.")
        return None

    # Validate input
    if not isinstance(R_Date, str):
        logger.error(f"Invalid R_Date type: {type(R_Date)}. Expected string.")
        return None

    valid_directions = {"DaysTill", "DaysSince"}
    if direction not in valid_directions:
        logger.error(f"Invalid direction: {direction}."
                     " Expected 'DaysTill' or 'DaysSince'.")
        return None

    try:
        # Convert R_Date to date object (ignore time component)
        R_Date2 = dt.datetime.strptime(R_Date, date_format).date()

        if direction == "DaysTill":
            idx = bisect.bisect_left(st.session_state.ElectionDatesAscend,
                                     R_Date2)
            if idx < len(st.session_state.ElectionDatesAscend):
                DaysDiff = (st.session_state.ElectionDatesAscend[idx] -
                            R_Date2).days
                return (math.ceil(DaysDiff / divisor) if divisor > 1
                        else DaysDiff)

        elif direction == "DaysSince":
            idx = bisect.bisect_right(st.session_state.ElectionDatesDescend,
                                      R_Date2) - 1
            if idx < 0:  # Prevent out-of-bounds access
                return None
            DaysDiff = (R_Date2 -
                        st.session_state.ElectionDatesDescend[idx]).days
            return math.ceil(DaysDiff / divisor) if divisor > 1 else DaysDiff

        return 0

    except Exception as e:
        logger.error(f"Error processing date: {e}")
        return None


# # Example usage
# if __name__ == "__main__":
#     import pandas as pd

#     data = {'ReceivedDate': ['2019/01/01 00:00:00', '2023/01/01 00:00:00']}
#     df = pd.DataFrame(data)

#     df['WeeksTillNextElection'] = df['ReceivedDate'].apply(
#         lambda x: GenElectionRelation2(x, divisor=7, direction="DaysTill")
#     )
#     df['WeeksSinceLastElection'] = df['ReceivedDate'].apply(
#         lambda x: GenElectionRelation2(x, divisor=7, direction="DaysSince")
#     )

#     print(df)
