"""
songs.py: the interface to our song data.
"""

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


def get_songs() -> dict:
    return songs

def already_exist(song_data: dict):
    for song in songs:
        if songs[song]['name'] == song_data['name'] and songs[song]['artist'] == song_data['artist']:
            return True
    return False


def add_song(song_id: str, song_data: dict):
    # Check if a song with same name + artist is already in the database
    if already_exist(song_data): 
        raise ValueError("A song with the same name and artist already existed!")
    songs[song_id] = song_data
