import pytest

import data.songs as data_songs


@pytest.fixture(scope='function')
def temp_song():
    song = data_songs.get_test_song()
    ret = data_songs.add_song(song)
    yield song
    if data_songs.already_exist(song['name'], song['artist']):
        data_songs.del_song(song['name'], song['artist'])


def test_get_test_name():
    name = data_songs._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 0


def test_gen_id():
    _id = data_songs._gen_id()
    assert isinstance(_id, str)
    assert len(_id) == data_songs.ID_LEN


def test_get_test_song():
    assert isinstance(data_songs.get_test_song(), dict)


def test_get_songs(temp_song):
    songs = data_songs.get_songs()
    assert isinstance(songs, dict)
    assert len(songs) >= 0
    for song in songs:
        assert isinstance(song, str)
        assert isinstance(songs[song], dict)


def test_already_exist(temp_song):
    name = temp_song['name']
    artist = temp_song['artist']
    assert data_songs.already_exist(name, artist) is True
    data_songs.del_song(name, artist)


def test_already_exist_not_there():
    new_name = data_songs._get_test_name()
    new_song = {
        'name': new_name,
        'artist': 'Some artist',
        'album': 'Some album',
        'genre': 'Some genre',
        'bpm': 10000,
    }
    assert data_songs.already_exist(new_song['name'], new_song['artist']) is False


def test_add_song_dup_name_and_artist(temp_song):
    with pytest.raises(ValueError):
        data_songs.add_song(temp_song)


def test_add_song():
    new_name = data_songs._get_test_name()
    new_song = {
        'name': new_name,
        'artist': 'Some artist',
        'album': 'Some album',
        'genre': 'Some genre',
        'bpm': 10000,
    }
    ret = data_songs.add_song(new_song)
    assert data_songs.already_exist(new_song['name'], new_song['artist'])
    assert isinstance(ret, bool)
    data_songs.del_song(new_song['name'], new_song['artist'])


def test_del_song(temp_song):
    name = temp_song['name']
    artist = temp_song['artist']
    data_songs.del_song(name, artist)
    assert data_songs.already_exist(name, artist) is False


def test_del_song_not_there():
    name = data_songs._get_test_name()
    artist = "unknown"
    with pytest.raises(ValueError):
        data_songs.del_song(name, artist)
