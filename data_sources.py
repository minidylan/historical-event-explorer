import requests
import streamlit as st

GOOGLE_BOOKS_API_URL = 'https://www.googleapis.com/books/v1/volumes'
YOUTUBE_API_KEY = 'AIzaSyAtnErcjqnaTV_b6npMna5sB5LR5rk6n9A'
YOUTUBE_SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'

def get_wikipedia_article(topic):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'titles': topic,
        'prop': 'extracts',
        'exintro': True,
        'explaintext': True
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        pages = response.json()['query']['pages']
        for page_id, page in pages.items():
            if 'extract' in page:
                return page['title'], page['extract'], f"https://en.wikipedia.org/wiki/{page['title'].replace(' ', '_')}"
    return None, "No extract available", None

def get_google_books(query):
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

def get_britannica_search_link(event):
    main_topic = event.split(',')[0].replace(' ', '%20')  # Use %20 for spaces in URLs
    return f"https://www.britannica.com/search?query={main_topic}"

def get_history_com_search_link(event):
    main_topic = event.split(',')[0].replace(' ', '+')  # Use + for spaces in History.com search
    return f"https://www.history.com/search?q={main_topic}"

def get_wikipedia_search_link(event):
    main_topic = event.split(',')[0].replace(' ', '_')
    return f"https://en.wikipedia.org/wiki/Special:Search?search={main_topic}"
