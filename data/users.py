"""
This module interfaces to our user data.
"""
import random

import data.db_connect as dbc

NAME = 'name'
EMAIL = 'email'
PASSWORD = 'password'
PLAYLISTS = 'playlists'
BIG_NUM = 100000000000000
MIN_USER_NAME_LEN = 2
MIN_PW_LEN = 8
USER_COLLECT = "users"


# Return random user name
def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


# Return random user email
def _get_test_email():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    email_suffix = '@gmail.com'
    return name + str(rand_part) + email_suffix


# Return random user password
def _get_test_password():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


# Return a test user based on random user name, user email, and password
def get_test_user():
    test_user = {}
    test_user[NAME] = _get_test_name()
    test_user[EMAIL] = _get_test_email()
    test_user[PASSWORD] = _get_test_password()
    return test_user


# Connect to MongoDB and get users from MongoDB database
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


# Return fetched user as doc if found, else return false
def already_exist(user_email: str):
    dbc.connect_db()
    fetched_user = dbc.fetch_one(USER_COLLECT, {EMAIL: user_email})
    return fetched_user is not None


# Return fetched user as doc if found, else return false
def already_exist_playlist(user_email: str, playlist_name: str):
    dbc.connect_db()
    fetched_user = dbc.fetch_one(USER_COLLECT, {EMAIL: user_email})
    return fetched_user is not None


# Check if a user with same email is already in the database
def add_user(user_data: dict) -> bool:
    if already_exist(user_data[EMAIL]):
        raise ValueError("A user with the same email already existed!")
    if len(user_data[NAME]) < 2:
        raise ValueError("Minimum user name length is 2 characters!")
    # ensure user email is valid
    if '@' not in user_data[EMAIL]:
        raise ValueError("Please enter a valid email!")
    else:
        email_components = user_data[EMAIL].split('@')
        if len(email_components[0]) < 1 or '.' not in email_components[1]:
            raise ValueError("Please enter a valid email!")
    if len(user_data[PASSWORD]) < MIN_PW_LEN:
        raise ValueError("Minimum password length is 8 characters!")
    dbc.connect_db()
    _id = dbc.insert_one(USER_COLLECT, user_data)
    return _id is not None


# Delete the user if it is already in the database
# Raise ValueError for user not in the database
def del_user(user_email: str):
    if already_exist(user_email):
        return dbc.del_one(USER_COLLECT, {EMAIL: user_email})
    else:
        raise ValueError(f"Delete failure: User with email {user_email} "
                         "not in database.")


# Check if a user types in password that matches the one in the database
# Else return False
# If the length of password is smaller than the required length,
# Raise ValueError
def auth_user(user_email: str, password: str):
    if len(password) < MIN_PW_LEN:
        raise ValueError("Minimum password length is 8 characters!")
    dbc.connect_db()
    fetched_user = dbc.fetch_one(USER_COLLECT, {EMAIL: user_email})
    if fetched_user:
        return fetched_user['password'] == password
    return False


# Get user id
def get_id(user_email: str, password: str):
    if len(password) < MIN_PW_LEN:
        raise ValueError("Minimum password length is 8 characters!")
    dbc.connect_db()
    fetched_user = dbc.fetch_one(USER_COLLECT, {EMAIL: user_email})
    if fetched_user:
        if fetched_user['password'] == password:
            return fetched_user['_id']
        else:
            raise ValueError("Password is incorrect!")
    raise ValueError("Email is incorrect!")
