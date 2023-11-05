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

import data.games as gm

import server.endpoints as ep

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


def test_games_get():
    resp = TEST_CLIENT.get(ep.GAMES_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)


@patch('data.games.add_game', return_value=gm.MOCK_ID, autospec=True)
def test_games_add(mock_add):
    """
    Testing we do the right thing with a good return from add_game.
    """
    resp = TEST_CLIENT.post(ep.GAMES_EP, json=gm.get_test_game())
    assert resp.status_code == OK


@patch('data.games.add_game', side_effect=ValueError(), autospec=True)
def test_games_bad_add(mock_add):
    """
    Testing we do the right thing with a value error from add_game.
    """
    resp = TEST_CLIENT.post(ep.GAMES_EP, json=gm.get_test_game())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.games.add_game', return_value=None)
def test_games_add_db_failure(mock_add):
    """
    Testing we do the right thing with a null ID return from add_game.
    """
    resp = TEST_CLIENT.post(ep.GAMES_EP, json=gm.get_test_game())
    assert resp.status_code == SERVICE_UNAVAILABLE


@pytest.mark.skip('This test is failing, but it is just an example of using '
                   + 'skip')
def test_that_doesnt_work():
    assert False