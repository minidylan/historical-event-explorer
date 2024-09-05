import streamlit as st
from event_fetcher import get_historical_event, get_random_historical_event
from display import display_event_and_resources

def main():
    st.title("Historical Event Explorer")

    # Step 3: User selects between search box or random event
    search_or_random = st.radio("Choose an option:", ("Search by Keyword", "Random Event from Year Range"))

    if search_or_random == "Search by Keyword":
        search_text = st.text_input("Search for a historical event (enter a keyword or phrase):")

        if st.button("Search"):
            if search_text:
                event_info = get_historical_event(text=search_text)
                if event_info:
                    day, month, year, event = event_info
                    display_event_and_resources(day, month, year, event)
                else:
                    st.error("No event found or an error occurred.")
            else:
                st.warning("Please enter a keyword or phrase to search.")

        if search_text and st.button("Search Again"):
            event_info = get_historical_event(text=search_text)
            if event_info:
                day, month, year, event = event_info
                display_event_and_resources(day, month, year, event)
            else:
                st.error("No event found or an error occurred.")

    elif search_or_random == "Random Event from Year Range":
        period = st.selectbox("Select a time period:", 
                              ["1700s", "1800s", "1900s", "2000s", "All time periods"])

        period_mapping = {
            "1700s": (1700, 1799),
            "1800s": (1800, 1899),
            "1900s": (1900, 1999),
            "2000s": (2000, 2023),
            "All time periods": (1700, 2023)
        }
        
        start_year, end_year = period_mapping[period]

        if st.button("Get Random Historical Event"):
            event_info = get_random_historical_event(start_year, end_year)
            if event_info:
                day, month, year, event = event_info
                display_event_and_resources(day, month, year, event)
            else:
                st.error("No event found or an error occurred.")

if __name__ == "__main__":
    main()
