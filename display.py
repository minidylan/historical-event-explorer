import streamlit as st
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
        month = "Unknown"
    if year is None or not isinstance(year, (int, str)):
        year = "Unknown"

    st.header(f"Date: {day}-{month}-{year}")
    st.subheader("Event")
    st.write(event)

    st.subheader("Learn More from Alternative Links")
    title, summary, link = get_wikipedia_article(event.split(',')[0])  # Use the first part of the event as the query
    if title and summary:
        st.markdown(f"**{title}**")
        st.write(summary)
        st.markdown(f"[Read more on Wikipedia]({link})")
    else:
        st.write("No related Wikipedia article found.")

    st.markdown(f"[Search on Wikipedia]({get_wikipedia_search_link(event)})")
    st.markdown(f"[Search on Britannica]({get_britannica_search_link(event)})")
    st.markdown(f"[Search on History.com]({get_history_com_search_link(event)})")

    st.subheader("Book Recommendations")
    recommendations = get_google_books(event)
    if recommendations:
        for book in recommendations:
            st.markdown(f"**{book['title']}** by {book['authors']}")
            st.markdown(f"[More Info]({book['link']})")
    else:
        st.write("No book recommendations found.")

    st.subheader("YouTube Videos")
    videos = get_youtube_videos(event)
    if videos:
        for video in videos:
            st.markdown(f"**{video['title']}**")
            st.markdown(f"[Watch on YouTube]({video['link']})")
    else:
        st.write("No related YouTube videos found.")
