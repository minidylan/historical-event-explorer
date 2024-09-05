import streamlit as st
import calendar
from data_sources import (
    get_wikipedia_article, 
    get_google_books, 
    get_youtube_videos, 
    get_britannica_search_link, 
    get_history_com_search_link,
    get_wikipedia_search_link
)

def display_event_and_resources(day, month, year, event):
    # Handle None or unexpected values for month and year
    if month is None or not isinstance(month, int):
        month_name = "Unknown"
    elif 1 <= month <= 12:
        month_name = calendar.month_name[month]
    else:
        month_name = "Unknown"

    # Format the date as "Day Month Year" or handle missing month
    if month_name == "Unknown":
        formatted_date = f"{day} {year}"  # Skip the month if it's unknown
    else:
        formatted_date = f"{day} {month_name} {year}"

    st.header(f"Date: {formatted_date}")
    st.subheader("Event")
    st.write(event)

    st.subheader("Learn More from Alternative Links")
    
    # Fetch and display Wikipedia article
    title, summary, link = get_wikipedia_article(event.split(',')[0])  # Use the first part of the event as the query
    if title and summary:
        st.markdown(f"**{title}**")
        st.write(summary)
        st.markdown(f"[Read more on Wikipedia]({link})")
    else:
        st.write("No related Wikipedia article found.")

    # Alternative links for Britannica and History.com
    st.markdown(f"[Search on Wikipedia]({get_wikipedia_search_link(event)})")
    st.markdown(f"[Search on Britannica]({get_britannica_search_link(event)})")
    st.markdown(f"[Search on History.com]({get_history_com_search_link(event)})")

    # Book Recommendations
    st.subheader("Book Recommendations")
    recommendations = get_google_books(event)
    if recommendations:
        for book in recommendations:
            st.markdown(f"**{book['title']}** by {book['authors']}")
            st.markdown(f"[More Info]({book['link']})")
    else:
        st.write("No book recommendations found.")

    # YouTube Video Recommendations
    st.subheader("YouTube Videos")
    videos = get_youtube_videos(event)
    if videos:
        for video in videos:
            st.markdown(f"**{video['title']}**")
            st.markdown(f"[Watch on YouTube]({video['link']})")
    else:
        st.write("No related YouTube videos found.")
