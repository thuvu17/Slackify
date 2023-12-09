"""
playlists.py: the interface to our playlist data.
"""
import random

import data.db_connect as dbc

PLAYLISTS_COLLECT = 'playlists'

NAME = 'name'
EMAIL = 'email'
SONGS = 'playlists'
MIN_NAME_LEN = 1

BIG_NUM = 100000000000000


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
    - Returns a dictionary of playlists keyed on playlist email (a str).
    - Each playlist email must be the key for a dictionary.
    - That dictionary must at least include a EMAIL member that is a string
    value.
    """
    dbc.connect_db()
    return dbc.fetch_all_as_list(PLAYLISTS_COLLECT, {EMAIL: user_email}, NAME)


# Return fetched playlist as doc if found, else return false
def already_exist(user_email: str, playlist_name: str):
    dbc.connect_db()
    fetched_playlist = dbc.fetch_one(PLAYLISTS_COLLECT, {EMAIL: user_email,
                                     NAME: playlist_name})
    return fetched_playlist is not None


def add_playlist(user_email: str, playlist_name: str) -> bool:
    # Check if a playlist with same name + playlist
    # is already in the database
    if already_exist(user_email, playlist_name):
        raise ValueError("A playlist with the same name already existed!")
    if len(playlist_name) < MIN_NAME_LEN:
        raise ValueError("Minimum playlist name length is 1 character!")
    if '@' not in user_email:
        raise ValueError("Invalid user email!")
    playlist_data = {EMAIL: user_email, NAME: playlist_name, SONGS: []}
    dbc.connect_db()
    _id = dbc.insert_one(PLAYLISTS_COLLECT, playlist_data)
    return _id is not None


def del_playlist(user_email: str, playlist_name: str):
    if already_exist(user_email, playlist_name):
        return dbc.del_one(PLAYLISTS_COLLECT, {EMAIL: user_email,
                           NAME: playlist_name})
    else:
        raise ValueError(f"Delete failure: Playlist {playlist_name} "
                         "not in database.")
