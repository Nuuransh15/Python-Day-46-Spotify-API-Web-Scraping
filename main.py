import requests
import bs4
from datetime import datetime
import re

valid_date_pattern = r"^\d{4}-\d{2}-\d{2}$"


# ------------------------ Helper Functions ------------------------ #
def is_valid_date(date_string):
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
                return False

        except ValueError:
            # If the date is not valid (e.g., 2023-02-30), it will raise a ValueError
            return False
    else:
        print(f"Your entered date: {date_string} is in the wrong format")
        return False


user_date_input = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

if is_valid_date(user_date_input):
    print("Valid date!")
else:
    print(f"Your entered date {user_date_input} is nvalid date and/or date format!")
