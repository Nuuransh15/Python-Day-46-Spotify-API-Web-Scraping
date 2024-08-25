import json
import os

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

valid_date_pattern = r"^\d{4}-\d{2}-\d{2}$"
URL = "https://www.billboard.com/charts/hot-100/"


# ------------------------ HELPER FUNCTIONS ------------------------ #
def is_valid_date(date_string):
    """
    Function to check if the user input string meets the following conditions:
    - In valid format (YYYY-MM-DD)
    - Is a valid date (e.g. not 2024-02-31)
    - Is not a date in the future
    :param date_string: The user input string for the date they want the top 100 songs from.
    :return: True if the date is valid, False if the date is invalid.
    """
    # Check if the entered user input is in the correct format
    if re.match(valid_date_pattern, date_string):
        try:
            # Try to create a datetime object from the user input string
            entered_date = datetime.strptime(date_string, "%Y-%m-%d")

            # Get today's date
            today = datetime.today()

            # Check if the entered date is not in the future
            if entered_date <= today:
                return True
            else:
                print(f"Your entered date: {date_string} cannot exist in the future! Please try again!")
                return False

        except ValueError:
            # If the date is not valid (e.g., 2023-02-30), it will raise a ValueError
            print(f"Your entered date: {date_string} is invalid and cannot exist! Please try again!")
            return False
    else:
        print(f"Your entered date: {date_string} is in the wrong format! Please try again!")
        return False


def get_website_soup(target_url):
    """
    Function to extract the webpage data of the provided URL as a soup object.
    :param target_url: The URL string from which we want the response
    :return: The raw html webpage data retrieved by the request as a soup object
    """
    response = requests.get(target_url)
    raw_data = response.text
    soup = BeautifulSoup(raw_data, "html.parser")
    return soup


def spotipy_search(sp: spotipy.Spotify, track_list: list, uris: list):
    """
    Searches for tracks on Spotify and appends their URIs to a provided list.
    :param sp: The authenticated Spotipy Spotify client instance
    :param track_list: A list of track names (strings) to search for on Spotify.
    :param uris: A list to hold the URIs of searched tracks.
    :return:
    """
    for track in track_list:
        query = f"track:{track}"

        # Perform the search on Spotify using the Spotipy client
        response = sp.search(q=query, type="track")

        try:
            # Attempt to extract the URI of first search result item
            track_uri = response["tracks"]["items"][0]["uri"]
        except KeyError:
            # If key error occurs - no items were found
            print(f"No URI results found in search for Track: {track}")
        else:
            uris.append(track_uri)


def spotipy_operations(track_list: list, uris: list, input_date: str):
    """
    Function to authenticate user into their spotify development application and create a list of Spotify
    song URIs for the list of song names found from the top 100 billboard search.
    :return:
    """
    # Load the environment variables (Client ID and secret)
    load_dotenv()

    # Create authenticated spotify client instance with scope to allow user to create a private playlist
    scope = "playlist-modify-private"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    spotipy_search(sp, track_list, uris)

    playlist_name = f"{input_date} Billboard 100"

    # create a new playlist and store the metadata returned upon creation
    playlist_metadata = sp.user_playlist_create(user=os.getenv("USER_ID"),
                                                name=playlist_name,
                                                public=False,
                                                description="Playlist created for Python Day 46")

    # add the track uris from the spotify search to the newly created playlist
    sp.playlist_add_items(playlist_id=playlist_metadata["uri"], items=uris)

    # NOTE! To fetch the user's created playlist, set the scope to "playlist-read-private" and then run this code:
    # my_playlists = sp.user_playlists(user=os.getenv("USER_ID"))
    # print(my_playlists)


# ------------------------------ MAIN EXECUTION ------------------------------ #
user_date_input = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

if is_valid_date(user_date_input):
    date_url = URL + f"{user_date_input}/"
    website_soup = get_website_soup(date_url)

    # Find all 100 songs and capture all raw data for each song
    songs_list_full_details = website_soup.findAll(name="div", class_="o-chart-results-list-row-container")

    # Find the song name within each song item within the list
    top_100_list = [entry.find(name="h3", id="title-of-a-story").getText().strip() for entry in songs_list_full_details]

    track_uris = []
    spotipy_operations(top_100_list, track_uris, user_date_input)
