import requests
import random
import streamlit as st

HISTORICAL_EVENTS_API_URL = 'https://api.api-ninjas.com/v1/historicalevents'
HISTORICAL_EVENTS_API_KEY = 'AELODrSUbplSOvWhZGOXwA==8y6wpe5HcQKm2hCf'

def get_historical_event(text=None, year=None, month=None, day=None, offset=0):
    """
    Fetch a historical event based on text, year, month, day, and offset.
    """
    query = {}
    if text:
        query['text'] = text
    if year:
        query['year'] = year
    if month:
        query['month'] = month
    if day:
        query['day'] = day
    if offset:
        query['offset'] = offset

    headers = {'X-Api-Key': HISTORICAL_EVENTS_API_KEY}

    response = requests.get(HISTORICAL_EVENTS_API_URL, headers=headers, params=query)

    if response.status_code == 200:
        events = response.json()
        if events:
            event = events[0]  # Take the first event for simplicity
            return event['year'], event.get('month', 1), event.get('day', 1), event['event']
        else:
            st.warning("No events found for the given query.")
            return None
    else:
        st.error(f"Failed to retrieve events. Status code: {response.status_code}")
        return None

def get_random_historical_event(start_year, end_year):
    """
    Fetch a random historical event within a specific date range.
    """
    attempts = 20  # Number of attempts to find a valid event
    for _ in range(attempts):
        year = random.randint(start_year, end_year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)

        event_info = get_historical_event(year=year, month=month, day=day)

        if event_info:
            return event_info
        else:
            continue  # Try another date

    st.warning("No events found after multiple attempts. Please try again.")
    return None
