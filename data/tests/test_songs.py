import pytest

import data.songs as songs

DUP_SONG_DATA = {
    'name': songs.TEST_SONG_NAME,
    'artist': songs.TEST_ARTIST_NAME,
    'album': 'idk',
    'genre': 'Pop',
    'bpm': 116,
}


def test_get_songs():
    songs = songs.get_songs()
    assert isinstance(songs, dict)
    assert len(songs) > 0
    for song in songs:
        assert isinstance(song, str)
        assert isinstance(songs[song], dict)


def test_already_exist():
    assert songs.already_exist(DUP_SONG_DATA) is True

def test_add_song_dup_name_and_artist():
    with pytest.raises(ValueError):
        songs.add_song("XYZ789", DUP_SONG_DATA)

NEW_SONG_DATA = {
    'name': "Rolling in the deep",
    'artist': "Adele",
    'album': '21',
    'genre': 'Soul',
    'bpm': 105,
}

def test_add_game():
    songs.add_game("NEW000", NEW_SONG_DATA)
    assert songs.already_exist(NEW_SONG_DATA) is True
