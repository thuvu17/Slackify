"""
playlists_songs.py: the interface to our playlist-song interaction data.
"""
import data.db_connect as dbc
import random

PLAYLISTS_SONGS_COLLECT = 'playlists_songs'
PLAYLIST_ID = '_id'     # playlist_id is the key
SONG_ID_LIST = 'song_ids'
BIG_NUM = 1000000


# Return random playlist id
def _get_test_playlist_id():
    name = 'test_playlist_id'
    return name + str(random.randint(0, BIG_NUM))


# Return random song id
def _get_test_song_id():
    name = 'test_song_id'
    return name + str(random.randint(0, BIG_NUM))


# Return a test playlist with random test name and email
def get_test_playlists_songs():
    test_playlists_songs = {}
    test_playlists_songs[PLAYLIST_ID] = _get_test_playlist_id()
    test_playlists_songs[SONG_ID_LIST] = [_get_test_song_id(),
                                          _get_test_song_id()]
    return test_playlists_songs


# Returns the list of song_ids that belongs to a given playlist_id
def get_song_ids_list(playlist_id: str):
    dbc.connect_db()
    ret_obj = dbc.fetch_one(PLAYLISTS_SONGS_COLLECT,
                            {PLAYLIST_ID: playlist_id})
    return ret_obj[SONG_ID_LIST]


# Tests if a song is already in a playlist
def song_exists_in_playlist(playlist_id: str, song_id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(PLAYLISTS_SONGS_COLLECT, {PLAYLIST_ID: playlist_id,
                                                   SONG_ID_LIST:
                                                   {'$in': [song_id]}})


# Updates the playlists_songs schema when user adds a song to playlist
def update_add_songs_in_playlist(playlist_id: str, song_id: str) -> bool:
    # If song is not already in playlist, add it
    if not song_exists_in_playlist(playlist_id, song_id):
        dbc.connect_db()
        old_song_ids_list = get_song_ids_list(playlist_id)
        updated_song_ids_list = old_song_ids_list.append(song_id)
        return dbc.update_doc(PLAYLISTS_SONGS_COLLECT,
                              {PLAYLIST_ID: playlist_id},
                              updated_song_ids_list)
    # If song already in playlist, raise value error
    else:
        raise ValueError("Failed to add a song: the song"
                         "is already in the playlist.")
