"""
This module interfaces to our user data.
"""

EMAIL = 'email'
MIN_USER_NAME_LEN = 2


def get_users():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user name (a str).
        - Each user name must be the key for a dictionary.
        - That dictionary must at least include a EMAIL member that is a string
        value.
    """
    users = {
        "Windy": {
            EMAIL: "pretty_windy@gmail.com",
        },
        "Joy": {
            EMAIL: "pretty_joy@gmail.com",
        },
    }
    return users
