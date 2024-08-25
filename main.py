import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

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


# ------------------------------ MAIN EXECUTION ------------------------------ #
user_date_input = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

if is_valid_date(user_date_input):
    date_url = URL + f"{user_date_input}/"
    website_soup = get_website_soup(date_url)

    # Find all 100 songs and capture all raw data for each song
    songs_list_full_details = website_soup.findAll(name="div", class_="o-chart-results-list-row-container")

    # Find the song name within each song item within the list
    top_100_list = [entry.find(name="h3", id="title-of-a-story").getText().strip() for entry in songs_list_full_details]
    print(top_100_list)
    print(len(top_100_list))
    assert len(top_100_list) == 100
