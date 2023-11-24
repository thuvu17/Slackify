from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch

import pytest

import data.songs as songs

import server.endpoints_song as ep

TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json


def test_list_users():
    resp = TEST_CLIENT.get(ep.USERS_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.TITLE in resp_json
    assert ep.TYPE in resp_json
    assert ep.DATA in resp_json


def test_songs_get():
    resp = TEST_CLIENT.get(ep.SONGS_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


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
    Testing we do the right thing with a value error from del_song.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_SONG_EP}/AnyName/AnyArtist')
    assert resp.status_code == NOT_FOUND


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


@pytest.mark.skip('This test is failing, but it is just an example of using '
                  + 'skip')
def test_that_doesnt_work():
    assert False