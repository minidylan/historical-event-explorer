import requests
import random
import streamlit as st

# API keys - replace with actual keys once you have them
HISTORICAL_EVENTS_API_KEY = 'AELODrSUbplSOvWhZGOXwA==8y6wpe5HcQKm2hCf'
YOUTUBE_API_KEY = 'AIzaSyAtnErcjqnaTV_b6npMna5sB5LR5rk6n9A'
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'
WIKIPEDIA_SEARCH_URL = "https://en.wikipedia.org/wiki/"
HISTORICAL_EVENTS_API_URL = 'https://api.api-ninjas.com/v1/historicalevents'
GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'

# Function to fetch a random historical event within a specific date range
def get_random_historical_event(start_year, end_year):
    attempts = 20  # Number of attempts to find a valid event
    for _ in range(attempts):
        year = random.randint(start_year, end_year)
        month = random.randint(1, 12)
        day = random.randint(1, 28)

        query = {'year': year, 'month': month, 'day': day}
        headers = {'X-Api-Key': HISTORICAL_EVENTS_API_KEY}

        response = requests.get(HISTORICAL_EVENTS_API_URL, headers=headers, params=query)

        if response.status_code == 200:
            events = response.json()
            if events:
                event = random.choice(events)
                return int(event['year']), int(event['month']), int(event['day']), event['event']
            else:
                continue  # Try another date
        else:
            st.error(f"Failed to retrieve events. Status code: {response.status_code}")
            return None

    st.warning("No events found after multiple attempts. Please try again.")
    return None

def clean_query(query):
    """Cleans up the search query for use in URLs."""
    return query.strip().lower().replace(" ", "-")

def get_wikipedia_link(event):
    main_topic = event.split(',')[0].replace(' ', '_')
    return f"{WIKIPEDIA_SEARCH_URL}{main_topic}"

def get_britannica_search_link(event):
    """Generates a search URL for Britannica based on the event."""
    main_topic = event.split(',')[0].replace(' ', '%20')  # Use %20 for spaces in URLs
    return f"https://www.britannica.com/search?query={main_topic}"

def get_history_com_search_link(event):
    """Generates a search URL for History.com based on the event."""
    main_topic = event.split(',')[0].replace(' ', '+')  # Use + for spaces in History.com search
    return f"https://www.history.com/search?q={main_topic}"

# Function to get book recommendations using Google Books API (without API key)
def get_book_recommendations(query):
    params = {
        'q': query,
        'maxResults': 3
    }
    response = requests.get(GOOGLE_BOOKS_API_URL, params=params)

    if response.status_code == 200:
        books = response.json().get('items', [])
        recommendations = []
        for book in books:
            title = book['volumeInfo'].get('title', 'No Title')
            authors = book['volumeInfo'].get('authors', ['Unknown Author'])
            link = book['volumeInfo'].get('infoLink', 'No Link Available')
            recommendations.append({'title': title, 'authors': ', '.join(authors), 'link': link})
        return recommendations
    else:
        st.error(f"Failed to retrieve books. Status code: {response.status_code}")
        return []

# Function to get YouTube video links using YouTube Data API
def get_youtube_videos(query):
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': 3,
        'key': YOUTUBE_API_KEY
    }
    response = requests.get(YOUTUBE_SEARCH_URL, params=params)

    if response.status_code == 200:
        videos = response.json().get('items', [])
        video_links = []
        for video in videos:
            title = video['snippet']['title']
            video_id = video['id']['videoId']
            link = f"https://www.youtube.com/watch?v={video_id}"
            video_links.append({'title': title, 'link': link})
        return video_links
    else:
        st.error(f"Failed to retrieve YouTube videos. Status code: {response.status_code}")
        return []

# Function to display the event and related resources
def display_event_and_resources(year, month, day, event):
    st.header(f"Date: {year}-{month:02d}-{day:02d}")
    st.subheader("Event")
    st.write(event)

    # Display the Wikipedia link
    wikipedia_link = get_wikipedia_link(event)
    st.subheader("Learn More")
    if wikipedia_link:
        st.markdown(f"[Read more on Wikipedia]({wikipedia_link})")

    # Display the Britannica search link
    britannica_link = get_britannica_search_link(event)
    st.markdown(f"[Search on Britannica]({britannica_link})")

    # Display the History.com search link
    history_com_link = get_history_com_search_link(event)
    st.markdown(f"[Search on History.com]({history_com_link})")

    # Display book recommendations
    st.subheader("Book Recommendations")
    recommendations = get_book_recommendations(event)
    if recommendations:
        for book in recommendations:
            st.markdown(f"**{book['title']}** by {book['authors']}")
            st.markdown(f"[More Info]({book['link']})")
    else:
        st.write("No book recommendations found.")

    # Display YouTube video recommendations
    st.subheader("YouTube Videos")
    videos = get_youtube_videos(event)
    if videos:
        for video in videos:
            st.markdown(f"**{video['title']}**")
            st.markdown(f"[Watch on YouTube]({video['link']})")
    else:
        st.write("No related YouTube videos found.")

# Main function to run the app
def main():
    st.title("Random Historical Event Explorer")

    # Dropdown for selecting the time period
    period = st.selectbox("Select a time period:", 
                          ["1700s", "1800s", "1900s", "2000s", "All time periods"])

    # Map the selected period to a date range
    if period == "1700s":
        start_year, end_year = 1700, 1799
    elif period == "1800s":
        start_year, end_year = 1800, 1899
    elif period == "1900s":
        start_year, end_year = 1900, 1999
    elif period == "2000s":
        start_year, end_year = 2000, 2023
    else:  # "All time periods"
        start_year, end_year = 1700, 2023

    if st.button("Get Random Historical Event"):
        event_info = get_random_historical_event(start_year, end_year)
        if event_info:
            year, month, day, event = event_info
            display_event_and_resources(year, month, day, event)
        else:
            st.error("No event found or an error occurred.")

if __name__ == "__main__":
    main()
