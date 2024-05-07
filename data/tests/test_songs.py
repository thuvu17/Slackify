import pytest

import data.songs as data_songs


# Generate a temporary song using the get_test_song function and
# adds it to the database.
# Yield the generated song for test cases
# Delete the song from the database after the test
@pytest.fixture(scope='function')
def temp_song():
    song = data_songs.get_test_song()
    ret = data_songs.add_song(song)
    yield song
    if data_songs.already_exist(song['name'], song['artist']):
        data_songs.del_song(song['name'], song['artist'])


# Assertion:
# Name is a string
# Length of name is larger than 0
def test_get_test_name():
    name = data_songs._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 0


# Assertion:
# Song ID is a string
# Length of song ID is correct
def test_gen_id():
    _id = data_songs._gen_id()
    assert isinstance(_id, str)
    assert len(str(_id)) == data_songs.ID_LEN


# Assertion:
# Test song is a disctionary
def test_get_test_song():
    song = data_songs.get_test_song()
    assert isinstance(song, dict)
    assert data_songs.SONG_ID in song
    assert data_songs.NAME in song
    assert data_songs.ARTIST in song
    assert data_songs.ALBUM in song
    assert data_songs.ENERGY in song
    assert data_songs.BPM in song


# Assertion:
# Songs is a dictionary
# The format of songs is correct
def test_get_songs(temp_song):
    songs = data_songs.get_songs()
    assert isinstance(songs, dict)
    assert len(songs) >= 0
    for song in songs:
        assert isinstance(song, str)
        assert isinstance(songs[song], dict)


# If the function correctly identifies an existing song,
# Assert it has already existed, delete the song
def test_already_exist(temp_song):
    name = temp_song['name']
    artist = temp_song['artist']
    assert data_songs.already_exist(name, artist) is True
    data_songs.del_song(name, artist)


# If song does not exist, assertion is false
def test_already_exist_not_there():
    new_name = data_songs._get_test_name()
    new_song = {
        'name': new_name,
        'artist': 'Some artist',
        'album': 'Some album',
        'genre': 'Some genre',
        'bpm': 10000,
    }
    assert data_songs.already_exist(new_song['name'],
                                    new_song['artist']) is False


# Adding a duplicate song raises a ValueError
def test_add_song_dup_name_and_artist(temp_song):
    with pytest.raises(ValueError):
        data_songs.add_song(temp_song)


# Assertion:
# New song is new in the database
# It can be added to the database
# Delete after testing
def test_add_song():
    new_name = data_songs._get_test_name()
    new_id = data_songs._gen_id()
    new_song = {
        '_id': new_id,
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


# Test whether it can successfully delete a song from the database
def test_del_song(temp_song):
    name = temp_song['name']
    artist = temp_song['artist']
    data_songs.del_song(name, artist)
    assert data_songs.already_exist(name, artist) is False


# Trying to delete a non-existing song raises a ValueError
def test_del_song_not_there():
    name = data_songs._get_test_name()
    artist = "unknown"
    with pytest.raises(ValueError):
        data_songs.del_song(name, artist)


# Test to delete a developed song from the database
def test_develope_del_song(temp_song):
    name = temp_song['name']
    artist = temp_song['artist']
    data_songs.develop_del_song(data_songs.NAME, name,
                                data_songs.ARTIST, artist)
    assert data_songs.already_exist(name, artist) is False


# Test to retrieve a song from the database by its ID
def test_get_song(temp_song):
    song_id = temp_song[data_songs.SONG_ID]
    song_data = data_songs.get_song(song_id)
    print("song data", song_data)
    assert isinstance(song_data, dict)
    assert data_songs.SONG_ID in song_data
    assert data_songs.NAME in song_data
    assert data_songs.ARTIST in song_data
    assert data_songs.ALBUM in song_data
    assert data_songs.ENERGY in song_data
    assert data_songs.BPM in song_data
