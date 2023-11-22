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
ARTIST = 'artist'
ALBUM = 'album'
GENRE = 'genre'
BPM = 'bpm'

# db = slackifyDB
# collection = songs
# {
#     'name'
#     'artist'
#     'bpm'
# }

# Test songs
songs = {}


# Return random song name
def _get_test_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


def get_test_song():
    test_song = {}
    test_song[NAME] = _get_test_name()
    test_song[ARTIST] = "Popular artist"
    test_song[ALBUM] = "Some album"
    test_song[GENRE] = "Some genre"
    test_song[BPM] = 116
    return test_song


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def get_songs() -> dict:
    try:
        dbc.connect_db()
        return dbc.fetch_all_as_dict(SONGS_COLLECT)
    except Exception:
        return {}


# Take in the name + artist of a song that you want to find in DB
# Return fetched song as doc if found, else return false
def already_exist(song_name: str, song_artist: str):
    dbc.connect_db()
    fetched_song = dbc.fetch_one(SONGS_COLLECT, {NAME: song_name, ARTIST: song_artist})
    return fetched_song is not None


def del_song(song_name: str, song_artist: str):
    if already_exist(song_name, song_artist):
        return dbc.del_one(SONGS_COLLECT, {NAME: song_name, ARTIST: song_artist})
    else:
        raise ValueError(f'Delete failure: {song_name} by {song_artist} not in database.')


def add_song(song_data: dict) -> bool:
    # Check if a song with same name + artist
    # is already in the database
    if already_exist(song_data[NAME], song_data[ARTIST]):
        raise ValueError("A song with the same name \
                         sand artist already existed!")
    dbc.connect_db()
    _id = dbc.insert_one(SONGS_COLLECT, song_data)
    return _id is not None


def main():
    print(get_songs())


if __name__ == '__main__':
    main()
