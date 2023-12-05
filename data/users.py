"""
This module interfaces to our user data.
"""
import random

import data.db_connect as dbc

NAME = 'name'
EMAIL = 'email'
BIG_NUM = 100000000000000
MIN_USER_NAME_LEN = 2
USER_COLLECT = "users"


# Return random user name
def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


# Return random user name
def _get_test_email():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    email_suffix = '@gmail.com'
    return name + str(rand_part) + email_suffix


def get_test_user():
    test_user = {}
    test_user[NAME] = _get_test_name()
    test_user[EMAIL] = _get_test_email()
    return test_user


def get_users():
    """
    Our contract:
    - No arguments.
    - Returns a dictionary of users keyed on user name (a str).
    - Each user name must be the key for a dictionary.
    - That dictionary must at least include a EMAIL member that is a string
    value.
    """
    dbc.connect_db()
    return dbc.fetch_all_as_dict(EMAIL, USER_COLLECT)


def get_old_users():
    users = {
        "Windy": {
            EMAIL: "pretty_windy@gmail.com",
        },
        "Joy": {
            EMAIL: "pretty_joy@gmail.com",
        },
    }
    return users


# Return fetched song as doc if found, else return false
def already_exist(user_email: str):
    dbc.connect_db()
    fetched_user = dbc.fetch_one(USER_COLLECT, {EMAIL: user_email})
    return fetched_user is not None


def add_user(user_data: dict) -> bool:
    # Check if a song with same name + artist
    # is already in the database
    if already_exist(user_data[EMAIL]):
        raise ValueError("A user with the same email already existed!")
    if len(user_data[NAME]) < 2:
        raise ValueError("Minimum user name length is 2 characters!")
    if '@' not in user_data[EMAIL]:
        raise ValueError("Please enter a valid email!")
    dbc.connect_db()
    _id = dbc.insert_one(USER_COLLECT, user_data)
    return _id is not None


def del_user(user_email: str):
    if already_exist(user_email):
        return dbc.del_one(USER_COLLECT, {EMAIL: user_email})
    else:
        raise ValueError(f"Delete failure: User with email {user_email} "
                         "not in database.")
