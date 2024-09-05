import re
import streamlit as st
from data_sources import (
    get_wikipedia_article, 
    get_google_books, 
    get_youtube_videos, 
    get_britannica_search_link, 
    get_history_com_search_link,
    get_wikipedia_search_link
)

def extract_search_query(event):
    """
    Extract a meaningful search query from the event description.
    Focus on specific historical terms like 'Battle', 'War', 'Revolution', etc.
    If the event mentions 'Name of person:', extract the name for the search.
    """
    # Look for the "Name of person:" pattern
    person_match = re.search(r'Name of person:\s*([A-Za-z\s]+)', event)
    if person_match:
        person_name = person_match.group(1).strip()
        return person_name  # Return the person's name as the search query

    # Extract the year from the event (look for a 4-digit year)
    year_match = re.search(r'\b\d{4}\b', event)
    year = year_match.group(0) if year_match else ""

    # Define historical keywords to look for in the event description
    keywords = ["battle", "war", "revolution", "earthquake", "massacre", "treaty", "rebellion", "siege", "conference", "incident", "campaign"]

    # Look for the keyword in the event description and extract the phrase that contains it
    for word in keywords:
        if word in event.lower():
            # Extract the phrase around the keyword (e.g., 'First Battle of Bud Dajo')
            match = re.search(rf'(\b[A-Za-z0-9\'\s]+{word}[A-Za-z0-9\'\s]*)', event, re.IGNORECASE)
            if match:
                return f"{match.group(0)} {year}".strip()  # Combine with year if available

    # If no keywords are found, fallback to using the first part of the event
    location_words = event.split(',')[0].split()[0:5]  # First 5 words for location/event type
    return " ".join(location_words + [year]).strip()

def display_event_and_resources(day, month, year, event):
    # Handle None or missing day, month, or year
    if day is None or day == "":
        day = "Unknown"
    if month is None or month == "":
        month = "Unknown"
    if year is None or year == "":
        year = "Unknown"

    # Format the date as "DD-MM-YYYY"
    if month == "Unknown" or day == "Unknown":
        formatted_date = f"{year}"  # Only show year if day or month is unknown
    else:
        formatted_date = f"{day}-{month}-{year}"

    st.header(f"Date: {formatted_date}")
    st.subheader("Event")
    st.write(event)

    # Extract search query from the event description
    search_query = extract_search_query(event)

    st.subheader(f"Search Query: {search_query}")  # Display the search query for debugging purposes

    st.subheader("Learn More from Alternative Links")

    # Fetch and display Wikipedia article using the search query
    title, summary, link = get_wikipedia_article(search_query)
    if title and summary:
        st.markdown(f"**{title}**")
        st.write(summary)
        st.markdown(f"[Read more on Wikipedia]({link})")
    else:
        st.write("No related Wikipedia article found.")

    # Alternative search links for Britannica and History.com using the search query
    st.markdown(f"[Search on Wikipedia]({get_wikipedia_search_link(search_query)})")
    st.markdown(f"[Search on Britannica]({get_britannica_search_link(search_query)})")
    st.markdown(f"[Search on History.com]({get_history_com_search_link(search_query)})")

    # Book Recommendations
    st.subheader("Book Recommendations")
    recommendations = get_google_books(search_query)
    if recommendations:
        for book in recommendations:
            st.markdown(f"**{book['title']}** by {book['authors']}")
            st.markdown(f"[More Info]({book['link']})")
    else:
        st.write("No book recommendations found.")

    # YouTube Video Recommendations
    st.subheader("YouTube Videos")
    videos = get_youtube_videos(search_query)
    if videos:
        for video in videos:
            st.markdown(f"**{video['title']}**")
            st.markdown(f"[Watch on YouTube]({video['link']})")
    else:
        st.write("No related YouTube videos found.")
