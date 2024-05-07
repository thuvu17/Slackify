import pytest

import data.playlists_songs as pls_songs


# Yield a temporary playlist_song for testing
@pytest.fixture(scope='function')
def temp_playlists_songs():
    test_pls_songs = pls_songs._get_test_playlists_songs()
    playlist_id = test_pls_songs[pls_songs.PLAYLIST_ID]
    song_id = test_pls_songs[pls_songs.SONG_ID]
    ret = pls_songs.add_playlist_song(playlist_id, song_id)
    print(ret)
    yield test_pls_songs
    if pls_songs.already_exist(test_pls_songs[pls_songs.PLAYLIST_ID],
                               test_pls_songs[pls_songs.SONG_ID]):
        pls_songs.del_playlists_songs(test_pls_songs[pls_songs.PLAYLIST_ID],
                                      test_pls_songs[pls_songs.SONG_ID])


# ---------- GET FUNCTION TESTS -----------
def test_already_exist(temp_playlists_songs):
    playlist_id = temp_playlists_songs[pls_songs.PLAYLIST_ID]
    song_id = temp_playlists_songs[pls_songs.SONG_ID]
    assert pls_songs.already_exist(str(playlist_id), str(song_id)) is not None


def test_already_exist_not_there():
    test_pls_songs_not_there = pls_songs._get_test_playlists_songs()
    playlist_id = test_pls_songs_not_there[pls_songs.PLAYLIST_ID]
    song_id = test_pls_songs_not_there[pls_songs.SONG_ID]
    assert pls_songs.already_exist(str(playlist_id), str(song_id)) is None


# ---------- ADD FUNCTION TESTS -----------
def test_add_playlist_song():
    test_pls_songs_to_add = pls_songs._get_test_playlists_songs()
    playlist_id = test_pls_songs_to_add[pls_songs.PLAYLIST_ID]
    song_id = test_pls_songs_to_add[pls_songs.SONG_ID]
    ret = pls_songs.add_playlist_song(playlist_id, song_id)
    assert ret is not None
    pls_songs.del_playlists_songs(playlist_id, song_id)


# ---------- DELETE FUNCTION TESTS -----------
def test_del_playlist():
    test_pls_songs_to_del = pls_songs._get_test_playlists_songs()
    playlist_id = test_pls_songs_to_del[pls_songs.PLAYLIST_ID]
    song_id = test_pls_songs_to_del[pls_songs.SONG_ID]
    add = pls_songs.add_playlist_song(playlist_id, song_id)
    delete = pls_songs.del_playlists_songs(playlist_id, song_id)
    assert pls_songs.already_exist(playlist_id, song_id) is None
