"""
songs.py: the interface to our song data.
"""
import random

import data.db_connect as dbc

SONGS_COLLECT = 'songs'

ID_LEN = 24
BIG_NUM = 100000000000000
MOCK_ID = '0'*ID_LEN
NAME = 'name'
SONG_NAME = 'song_name'
ARTIST = 'artist'
ALBUM = 'album'
GENRE = 'genre'
BPM = 'bpm'
SONG_ID = 'song_id'

# TEST_SONG_NAME = 'Beat It'
# TEST_ARTIST_NAME = 'Michael Jackson'

# Test songs
songs = {}


def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def get_test_song():
    test_song = {}
    test_song[NAME] = _get_test_name()
    test_song[SONG_NAME] = "Generic song name"
    test_song[ARTIST] = "Popular artist"
    test_song[ALBUM] = "idk"
    test_song[GENRE] = "Pop"
    test_song[BPM] = 116
    return test_song


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def get_songs() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(NAME, SONGS_COLLECT)


def already_exist(song_data: dict, song_id: str):
    dbc.connect_db()
    fetched_song = dbc.fetch_one(SONGS_COLLECT, {SONG_ID: song_id})
    if song_id in fetched_song:
        for song in songs:
            if songs[song] == song_id:
                if songs[song] == song_data:
                    return True
    return False


def del_song(name: str):
    if already_exist(name, "NEW000"):
        dbc.del_one(SONGS_COLLECT, {NAME: name})
    else:
        raise ValueError(f'Delete failure: {name} not in database.')


def add_song(song_id: str, song_data: dict) -> str:
    # Check if a song with same name + artist
    # is already in the database
    if already_exist(song_data, song_id):
        raise ValueError("A song with the same name \
                         sand artist already existed!")
    song = {}
    song[song_id] = song_data
    dbc.connect_db()
    _id = dbc.insert_one(SONGS_COLLECT, song)
    return _id is not None


def main():
    print(get_songs())


if __name__ == '__main__':
    main()
