"""
songs.py: the interface to our song data.
"""
import random

ID_LEN = 24
BIG_NUM = 100000000000000
MOCK_ID = '0'*ID_LEN
NAME = 'name'
SONG_NAME = 'song_name'
ARTIST = 'artist'
ALBUM = 'album'
GENRE = 'genre'
BPM = 'bpm'


TEST_SONG_NAME = 'Beat It'
TEST_ARTIST_NAME = 'Michael Jackson'

# Test songs
songs = {
    'ABC123': {
        'name': 'Billie Jean',
        'artist': 'Michael Jackson',
        'album': 'idk',
        'genre': 'Pop',
        'bpm': 116,
    },
    'BCD456': {
        'name': TEST_SONG_NAME,
        'artist': TEST_ARTIST_NAME,
        'album': 'idk2',
        'genre': 'Pop',
        'bpm': 125,
    },
}


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
    return songs


def already_exist(song_data: dict):
    for song in songs:
        if songs[song]['name'] == song_data['name']:
            if songs[song]['artist'] == song_data['artist']:
                return True
    return False


def add_song(song_id: str, song_data: dict) -> str:
    # Check if a song with same name + artist
    # is already in the database
    if already_exist(song_data):
        raise ValueError("A song with the same name \
                         sand artist already existed!")
    songs[song_id] = song_data
    return _gen_id()
