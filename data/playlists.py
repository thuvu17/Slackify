"""
playlists.py: the interface to our playlist data.
"""
import random
import datetime

import data.db_connect as dbc

PLAYLISTS_COLLECT = 'playlists'

NAME = 'name'
USER_ID = 'user_id'
DATE = 'date_created'
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
def _get_test_user_id():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


# Return real time date
def get_date():
    return str(datetime.date.today())


# Return a test playlist with random test name and user_id
def get_test_playlist():
    test_playlist = {}
    test_playlist[NAME] = _get_test_name()
    test_playlist[USER_ID] = _get_test_user_id()
    test_playlist[DATE] = get_date()
    test_playlist[SONGS] = []
    return test_playlist


def get_playlists(user_id):
    """
    Our contract:
    - No arguments.
    - Returns a list of playlist names keyed on playlist user_id (a str).
    - Each playlist user_id must be the key for a dictionary.
    - That dictionary must at least include a user_id member that is a string
    value.
    """
    dbc.connect_db()
    return dbc.fetch_all_as_list(PLAYLISTS_COLLECT, {USER_ID: user_id},
                                 NAME)


# Connect to MongoDB and get users from MongoDB database
def get_all_playlists():
    dbc.connect_db()
    return dbc.fetch_all_songs_as_dict(PLAYLISTS_COLLECT)
    # name to be changed


# Take in the user id and name of a playlist that you want to find in DB
# Return the associated playlist if it exists, None if not
def get_playlist(user_id: str, playlist_name: str) -> dict:
    dbc.connect_db()
    return dbc.fetch_one(PLAYLISTS_COLLECT, {USER_ID: user_id,
                         NAME: playlist_name})


# Take in the user id and name of a playlist that you want to find in DB
# Return true if given playlist is found, else return false
def already_exist(user_id: str, playlist_name: str) -> bool:
    return get_playlist(user_id, playlist_name) is not None


# Take in user id and playlist name to create a playlist and add to DB
# Return true if successfully added, else return false
# Raise error if given playlist already exists, or playlist name too short
def add_playlist(user_id: str, playlist_name: str) -> bool:
    # Check if a playlist with same user id + name
    # is already in the database
    if already_exist(user_id, playlist_name):
        raise ValueError("A playlist with the same name already existed!")
    if len(playlist_name) < MIN_NAME_LEN:
        raise ValueError("Minimum playlist name length is 1 character!")

    date = get_date()
    playlist_data = {USER_ID: user_id, NAME: playlist_name,
                     DATE: date, SONGS: []}
    dbc.connect_db()
    _id = dbc.insert_one(PLAYLISTS_COLLECT, playlist_data)
    return _id is not None


# Take in user id and playlist name to delete a playlist from DB
# Return true if successfully added, else return false
# Raise error if given playlist does not exist
def del_playlist(user_id: str, playlist_name: str):
    if already_exist(user_id, playlist_name):
        return dbc.del_one(PLAYLISTS_COLLECT, {USER_ID: user_id,
                           NAME: playlist_name})
    else:
        raise ValueError(f"Delete failure: Playlist {playlist_name} "
                         "not in database.")


def update_playlist_name(user_id: str, playlist_name: str,
                         new_playlist_name: str) -> bool:
    if not already_exist(user_id, playlist_name):
        raise ValueError(f"Update failure: {playlist_name} not in database.")
    if already_exist(user_id, new_playlist_name):
        raise ValueError("A playlist with the same name already existed!")
    if len(new_playlist_name) < MIN_NAME_LEN:
        raise ValueError("Minimum playlist name length is 1 character!")
    else:
        dbc.connect_db()
        return dbc.update_doc(PLAYLISTS_COLLECT, {USER_ID: user_id,
                              NAME: playlist_name},
                              {NAME: new_playlist_name})


def song_exists_in_playlist(user_id: str, playlist_name: str,
                            song_id: str) -> bool:
    playlist = get_playlist(user_id, playlist_name)
    return song_id in playlist.get(SONGS)


def update_add_songs_in_playlist(user_id: str, playlist_name: str,
                                 song_id: str) -> bool:
    if not already_exist(user_id, playlist_name):
        raise ValueError(f"Failed to add a song: {playlist_name}"
                         "not in database.")
    elif song_exists_in_playlist(user_id, playlist_name, song_id):
        raise ValueError("Failed to add a song: the song"
                         "is already in the playlist.")
    else:
        playlist = get_playlist(user_id, playlist_name)
        songs_in = playlist[SONGS]
        print(songs_in)
        songs_in.append(song_id)
        print(songs_in)
        dbc.connect_db()
        return dbc.update_doc(PLAYLISTS_COLLECT, {USER_ID: user_id,
                              NAME: playlist_name}, {SONGS: songs_in})


# import random
# import datetime
# from bson import ObjectId
# import data.db_connect as dbc

# PLAYLISTS_COLLECT = 'playlists'

# MONGO_ID = '_id'
# NAME = 'name'
# DATE = 'date_created'

# MIN_NAME_LEN = 1

# ID_LEN = 24
# BIG_NUM = 100000000000000
# MOCK_ID = '0'*ID_LEN


# # Return random playlist name
# def _get_test_name():
#     name = 'playlist'
#     rand_part = random.randint(0, BIG_NUM)
#     return name + str(rand_part)


# def _gen_id() -> str:
#     _id = random.randint(0, BIG_NUM)
#     _id = str(_id)
#     _id = _id.rjust(ID_LEN, '0')
#     return _id


# # Return real time date
# def get_date():
#     return str(datetime.date.today())


# # Return a test playlist with random test name and email
# def get_test_playlist():
#     test_playlist = {}
#     test_playlist[NAME] = _get_test_name()
#     test_playlist[DATE] = get_date()
#     return test_playlist


# def already_exist(playlist_id: str) -> bool:
#     return get_playlist(playlist_id) is not None


# # Take in the user email and name of a playlist that you want to find in DB
# # Return the associated playlist if it exists, None if not
# def get_playlist(playlist_id: str) -> dict:
#     dbc.connect_db()
#     return dbc.fetch_one(PLAYLISTS_COLLECT,
# {MONGO_ID: ObjectId(playlist_id)})


# # Take in user email and playlist name to create a playlist and add to DB
# # Return true if successfully added, else return false
# # Raise error if given playlist already exists, or playlist name too short
# # or invalid user email is given
# def add_playlist(playlist_name: str) -> bool:
#     # Check if a playlist with same email + name
#     # is already in the database
#     if len(playlist_name) < MIN_NAME_LEN:
#         raise ValueError("Minimum playlist name length is 1 character!")
#     # ensure user email is valid
#     # can be deleted in the future since user email must be valid here
#     else:
#         date = get_date()
#         playlist_data = {NAME: playlist_name, DATE: date}
#         dbc.connect_db()
#         _id = dbc.insert_one(PLAYLISTS_COLLECT, playlist_data)
#         if _id is not None:
#             return str(_id.inserted_id)
#         return None


# # Take in user email and playlist name to delete a playlist from DB
# # Return true if successfully added, else return false
# # Raise error if given playlist does not exist
# def del_playlist(playlist_id: str):
#     if not already_exist(playlist_id):
#         raise ValueError(f"Delete Fail: Playlist with id {playlist_id} "
#                          "not in database")
#     return dbc.del_one(PLAYLISTS_COLLECT, {MONGO_ID:  ObjectId(playlist_id)})


# # def update_playlist_name(playlist_id: str, playlist_name: str,
# #                          new_playlist_name: str) -> bool:
# #     if len(new_playlist_name) < MIN_NAME_LEN:
# #         raise ValueError("Minimum playlist name length is 1 character!")
# #     elif playlist_name == new_playlist_name:
# #         raise ValueError("New name is the same as the old name!")
# #     else:
# #         dbc.connect_db()
# #         return dbc.update_doc(PLAYLISTS_COLLECT, {MONGO_ID: playlist_id},
# #                               {NAME: new_playlist_name})
