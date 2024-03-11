"""
playlists_songs.py: the interface to our playlist-song interaction data.
"""
import data.db_connect as dbc
from bson import ObjectId

PLAYLISTS_SONGS_COLLECT = 'playlists_songs'
PLAYLIST_ID = 'playlist_id'     # playlist_id is the key
SONG_ID = 'song_id'
BIG_NUM = 1000000


# Return a test playlist with random test ids
def _get_test_playlists_songs():
    test_playlists_songs = {}
    test_playlists_songs[PLAYLIST_ID] = str(ObjectId())
    test_playlists_songs[SONG_ID] = str(ObjectId())
    return test_playlists_songs


# Returns the list of song_ids that belongs to a given playlist_id
def get_all_song_ids(playlist_id: str):
    dbc.connect_db()
    if playlist_already_exist(playlist_id):
        ret_obj = dbc.fetch_all_as_list(PLAYLISTS_SONGS_COLLECT,
                                        {PLAYLIST_ID: ObjectId(playlist_id)})
    else:
        raise ValueError("Playlist does not exist!")
    return ret_obj


# Delete a playlist-song relationship
def del_playlists_songs(playlist_id: str, song_id: str):
    dbc.connect_db()
    ret_obj = dbc.del_one(PLAYLISTS_SONGS_COLLECT,
                          {PLAYLIST_ID: ObjectId(playlist_id),
                           SONG_ID: ObjectId(song_id)})
    return ret_obj


# Returns the list of song_ids that belongs to a given playlist_id
def already_exist(playlist_id: str, song_id: str):
    dbc.connect_db()
    ret_obj = dbc.fetch_one(PLAYLISTS_SONGS_COLLECT,
                            {PLAYLIST_ID: ObjectId(playlist_id),
                             SONG_ID: ObjectId(song_id)})
    return ret_obj


# Returns the list of song_ids that belongs to a given playlist_id
def playlist_already_exist(playlist_id: str):
    dbc.connect_db()
    ret_obj = dbc.fetch_one(PLAYLISTS_SONGS_COLLECT,
                            {PLAYLIST_ID: ObjectId(playlist_id)})
    return ret_obj


# Add a new playlist id into playlists_songs schema
def add_playlist_song(playlist_id: str, song_id: str):
    dbc.connect_db()
    if not already_exist(playlist_id, song_id):
        insert_doc = {PLAYLIST_ID: ObjectId(playlist_id),
                      SONG_ID: ObjectId(song_id)}
    else:
        raise ValueError("Playlist already exists!")
    return dbc.insert_one(PLAYLISTS_SONGS_COLLECT, insert_doc)


# Updates the playlists_songs schema when user adds a song to playlist
# def update_add_songs_in_playlist(playlist_id: str, song_id: str) -> bool:
#     if playlist_already_exist(playlist_id):
#         # If song is not already in playlist, add it
#         if not song_exists_in_playlist(playlist_id, song_id):
#             dbc.connect_db()
#             old_song_ids_list = get_song_ids_list(playlist_id)
#             updated_song_ids_list = old_song_ids_list.append(song_id)
#             return dbc.update_doc(PLAYLISTS_SONGS_COLLECT,
#                                   {PLAYLIST_ID: playlist_id},
#                                   updated_song_ids_list)
#         # If song already in playlist, raise value error
#         else:
#             raise ValueError("Song is already in the playlist.")
#     else:
#         raise ValueError("Playlist does not exist!")
