from http.client import (
    BAD_REQUEST,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
    FOUND,
    UNAUTHORIZED,
)

from unittest.mock import patch

import pytest

import data.songs as songs

import data.users as usrs

import data.playlists as plists

import server.endpoints_song as ep


TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json


# ---------- USER EP TESTS -----------
# Get user
def test_get_users():
    """
    Testing if users get ep returns the right type and data
    """
    resp = TEST_CLIENT.get(ep.USERS_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.TITLE in resp_json
    assert ep.TYPE in resp_json
    assert ep.DATA in resp_json


# Delete user
@patch('data.users.del_user', autospec=True)
def test_users_del(mock_del):
    """
    Testing we do the right thing with a call to del_user that succeeds.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_USER_EP}/AnyEmail')
    assert resp.status_code == OK


@patch('data.users.del_user', side_effect=ValueError(), autospec=True)
def test_users_bad_del(mock_del):
    """
    Testing we do the right thing with a value error from del_user.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_USER_EP}/AnyEmail')
    assert resp.status_code == NOT_FOUND


# Add user
@patch('data.users.add_user', return_value=usrs.EMAIL, autospec=True)
def test_users_add(mock_add):
    """
    Testing we do the right thing with a good return from add_user.
    """
    resp = TEST_CLIENT.post(ep.USERS_EP, json=usrs.get_test_user())
    assert resp.status_code == OK


@patch('data.users.add_user', side_effect=ValueError(), autospec=True)
def test_users_bad_add(mock_add):
    """
    Testing we do the right thing when deleting a non-existed user.
    """
    resp = TEST_CLIENT.post(ep.USERS_EP, json=usrs.get_test_user())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.users.add_user', return_value=None)
def test_users_add_db_failure(mock_add):
    """
    Testing we do the right thing with a technical problem from add_user.
    """
    resp = TEST_CLIENT.post(ep.USERS_EP, json=usrs.get_test_user())
    assert resp.status_code == SERVICE_UNAVAILABLE


# ---------- SONG EP TESTS -----------
# Get song
def test_songs_get():
    """
    Testing songs_get_ep returns the correct data
    """
    resp = TEST_CLIENT.get(ep.SONGS_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


# Add song
@patch('data.songs.add_song', return_value=songs.MOCK_ID, autospec=True)
def test_songs_add(mock_add):
    """
    Testing we do the right thing with a good return from add_song.
    """
    resp = TEST_CLIENT.post(ep.SONGS_EP, json=songs.get_test_song())
    assert resp.status_code == OK


@patch('data.songs.add_song', side_effect=ValueError(), autospec=True)
def test_songs_bad_add(mock_add):
    """
    Testing we do the right thing with a value error from add_song.
    """
    resp = TEST_CLIENT.post(ep.SONGS_EP, json=songs.get_test_song())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.songs.add_song', return_value=None)
def test_songs_add_db_failure(mock_add):
    """
    Testing we do the right thing with a null ID return from add_song.
    """
    resp = TEST_CLIENT.post(ep.SONGS_EP, json=songs.get_test_song())
    assert resp.status_code == SERVICE_UNAVAILABLE


# Delete song
@patch('data.songs.del_song', autospec=True)
def test_songs_del(mock_del):
    """
    Testing we do the right thing with a call to del_song that succeeds.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_SONG_EP}/AnyName/AnyArtist')
    assert resp.status_code == OK


@patch('data.songs.del_song', side_effect=ValueError(), autospec=True)
def test_songs_bad_del(mock_del):
    """
    Testing we do the right thing with a value error from del_song ep.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_SONG_EP}/AnyName/AnyArtist')
    assert resp.status_code == NOT_FOUND


# ---------- PLAYLIST EP TESTS -----------
# Get playlist
def test_playlists_get():
    """
    Testing get_playlist EP return the correct data.
    """
    resp = TEST_CLIENT.get(f'{ep.GET_PLAYLISTS_EP}/AnyID')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


# Get all playlists
def test_all_playlists_get():
    """
    Testing playlists_get_ep returns the correct data
    """
    resp = TEST_CLIENT.get(ep.GET_PLAYLISTS_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


# Get all songs in a playlist
def test_all_songs_in_playlist_get():
    resp = TEST_CLIENT.get(f"{ep.PLAYLIST_EP}/AnyUser_id/AnyName")
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


# Add playlist
@patch('data.playlists.add_playlist', return_value=plists.MOCK_ID,
       autospec=True)
def test_playlists_add(mock_add):
    """
    Testing we do the right thing with a good return from add_playlist.
    """
    resp = TEST_CLIENT.post(ep.PLAYLISTS_EP, json=plists.get_test_playlist())
    assert resp.status_code == OK


@patch('data.playlists.add_playlist', side_effect=ValueError(), autospec=True)
def test_playlists_bad_add(mock_add):
    """
    Testing we do the right thing with a value error from add_playlist.
    """
    resp = TEST_CLIENT.post(ep.PLAYLISTS_EP, json=plists.get_test_playlist())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.playlists.add_playlist', return_value=None)
def test_playlists_add_db_failure(mock_add):
    """
    Testing we do the right thing when add_playlist failed.
    """
    resp = TEST_CLIENT.post(ep.PLAYLISTS_EP, json=plists.get_test_playlist())
    assert resp.status_code == SERVICE_UNAVAILABLE


# Delete playlist
@patch('data.playlists.del_playlist', autospec=True)
def test_playlists_del(mock_del):
    """
    Testing we do the right thing with a call to del_playlist that succeeds.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_PLAYLIST_EP}/AnyID/AnyName')
    assert resp.status_code == OK


@patch('data.playlists.del_playlist', side_effect=ValueError(), autospec=True)
def test_playlists_bad_del(mock_del):
    """
    Testing we do the right thing when user deletes a non-existent playlist.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_PLAYLIST_EP}/AnyID/AnyName')
    assert resp.status_code == NOT_FOUND


# Update playlist
@patch('data.playlists.update_playlist_name', autospec=True)
def test_playlist_name_update(mock_update):
    """
    Testing we do the right thing with a call to
    update_playlist_name that succeeds.
    """
    resp = TEST_CLIENT.put(
        f'{ep.UPDATE_PLAYLIST_EP}/AnyID/AnyName/AnyNewName')
    assert resp.status_code == OK


@patch('data.playlists.update_playlist_name', side_effect=ValueError(),
       autospec=True)
def test_playlist_name_bad_update(mock_update):
    """
    Testing we do the right thing with a call to
    update_playlist_name that fails.
    """
    resp = TEST_CLIENT.put(
        f'{ep.UPDATE_PLAYLIST_EP}/AnyID/AnyName/AnyNewName')
    assert resp.status_code == NOT_FOUND


@patch('data.playlists.update_add_songs_in_playlist', autospec=True)
def test_update_add_songs_in_playlist(mock_update):
    """
    Testing we do the right thing with a call to
    update_add_songs_in_playlist that succeeds.
    """
    resp = TEST_CLIENT.put(
        f'{ep.ADD_SONG_PLAYLIST_EP}/AnyUserId/AnyName/AnySongId')
    assert resp.status_code == OK


@patch('data.playlists.update_add_songs_in_playlist', side_effect=ValueError(),
       autospec=True)
def test_update_add_songs_in_playlist_bad(mock_update):
    """
    Testing we do the right thing with a call to
    update_add_songs_in_playlist that fails.
    """
    resp = TEST_CLIENT.put(
        f'{ep.ADD_SONG_PLAYLIST_EP}/AnyUserId/AnyName/AnySongId')
    assert resp.status_code == NOT_FOUND


# ---------- AUTH EP TESTS -----------
# Sign in
@patch('data.users.auth_user', autospec=True)
def test_sign_in(mock_get):
    """
    Testing we do the right thing with a call to sign_in that succeeds.
    """
    resp = TEST_CLIENT.get(f'{ep.SIGN_IN_EP}/AnyEmail/AnyPassword')
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


@patch('data.users.auth_user', return_value=False, autospec=True)
def test_failed_sign_in(mock_get):
    """
    Testing we do the right thing with a call to sign_in that fails.
    """
    resp = TEST_CLIENT.get(f'{ep.SIGN_IN_EP}/AnyEmail/AnyPassword')
    assert resp.status_code == UNAUTHORIZED


@patch('data.users.auth_user', side_effect=ValueError(), autospec=True)
def test_bad_sign_in(mock_get):
    """
    Testing we do the right thing with an unacceptable call to sign_in.
    """
    resp = TEST_CLIENT.get(f'{ep.SIGN_IN_EP}/AnyEmail/AnyPassword')
    assert resp.status_code == NOT_ACCEPTABLE


# Sign up
@patch('data.users.add_user', autospec=True)
def test_sign_up(mock_get):
    """
    Testing we do the right thing with a call to sign_up that succeeds.
    """
    resp = TEST_CLIENT.get(f'{ep.SIGN_UP_EP}/AnyEmail/AnyPassword/AnyUsername')
    assert resp.status_code == FOUND


@patch('data.users.add_user', side_effect=ValueError(), autospec=True)
def test_failed_sign_up(mock_get):
    """
    Testing we do the right thing with a call to sign_up that failed.
    """
    resp = TEST_CLIENT.get(f'{ep.SIGN_UP_EP}/AnyEmail/AnyPassword/AnyUsername')
    assert resp.status_code == BAD_REQUEST


# # Sign out
# def test_sign_out():
#     """
#     Testing we do the right thing with a call to sign_out that succeeds.
#     """
#     valid_test_email = "thu@gmail.com"
#     valid_test_password = "thisismypassword"
#     resp = TEST_CLIENT.get(
#         f'{ep.SIGN_IN_EP}/{valid_test_email}/{valid_test_password}')
#     assert resp.status_code == FOUND
#     # Sign out
#     resp = TEST_CLIENT.get(f'{ep.SIGN_OUT_EP}')
#     assert resp.status_code == OK


# def test_failed_sign_out():
#     """
#     Testing we do the right thing with a call to sign_out that fails.
#     """
#     resp = TEST_CLIENT.get(f'{ep.SIGN_OUT_EP}')
#     assert resp.status_code == BAD_REQUEST


@pytest.mark.skip('This test is failing, but it is just an example of using '
                  + 'skip')
def test_that_doesnt_work():
    assert False
