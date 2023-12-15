"""
playlists.py: the interface to our playlist data.
"""
import random

import data.db_connect as dbc

PLAYLISTS_COLLECT = 'playlists'

NAME = 'name'
EMAIL = 'email'
SONGS = 'songs'
MIN_NAME_LEN = 1

ID_LEN = 24
BIG_NUM = 100000000000000
MOCK_ID = '0'*ID_LEN


# Return random playlist name
def _get_test_name():
    name = 'playlist'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


# Return random playlist name
def _get_test_email():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    email_suffix = '@gmail.com'
    return name + str(rand_part) + email_suffix


# Return a test playlist with random test name and email
def get_test_playlist():
    test_playlist = {}
    test_playlist[NAME] = _get_test_name()
    test_playlist[EMAIL] = _get_test_email()
    test_playlist[SONGS] = []
    return test_playlist


def get_playlists(user_email):
    """
    Our contract:
    - No arguments.
    - Returns a list of playlist names keyed on playlist email (a str).
    - Each playlist email must be the key for a dictionary.
    - That dictionary must at least include a EMAIL member that is a string
    value.
    """
    dbc.connect_db()
    return dbc.fetch_all_as_list(PLAYLISTS_COLLECT, {EMAIL: user_email}, NAME)


# Take in the user email and name of a playlist that you want to find in DB
# Return true if given playlist is found, else return false
def already_exist(user_email: str, playlist_name: str) -> bool:
    dbc.connect_db()
    fetched_playlist = dbc.fetch_one(PLAYLISTS_COLLECT, {EMAIL: user_email,
                                     NAME: playlist_name})
    return fetched_playlist is not None


# Take in user email and playlist name to create a playlist and add to DB
# Return true if successfully added, else return false
# Raise error if given playlist already exists, or playlist name too short
# or invalid user email is given
def add_playlist(user_email: str, playlist_name: str) -> bool:
    # Check if a playlist with same email + name
    # is already in the database
    if already_exist(user_email, playlist_name):
        raise ValueError("A playlist with the same name already existed!")
    if len(playlist_name) < MIN_NAME_LEN:
        raise ValueError("Minimum playlist name length is 1 character!")
    # ensure user email is valid
    # can be deleted in the future since user email must be valid here
    if '@' not in user_email:
        raise ValueError("Invalid user email!")
    else:
        email_components = user_email.split('@')
        if len(email_components[0]) < 1 or '.' not in email_components[1]:
            raise ValueError("Invalid user email!")
    playlist_data = {EMAIL: user_email, NAME: playlist_name, SONGS: []}
    dbc.connect_db()
    _id = dbc.insert_one(PLAYLISTS_COLLECT, playlist_data)
    return _id is not None


# Take in user email and playlist name to delete a playlist from DB
# Return true if successfully added, else return false
# Raise error if given playlist does not exist
def del_playlist(user_email: str, playlist_name: str):
    if already_exist(user_email, playlist_name):
        return dbc.del_one(PLAYLISTS_COLLECT, {EMAIL: user_email,
                           NAME: playlist_name})
    else:
        raise ValueError(f"Delete failure: Playlist {playlist_name} "
                         "not in database.")
