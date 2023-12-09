import pytest

import data.playlists as pls


@pytest.fixture(scope='function')
def temp_playlist():
    playlist = pls.get_test_playlist()
    ret = pls.add_playlist(playlist)
    yield playlist
    if pls.already_exist(playlist['email'], playlist['name']):
        pls.del_playlist(playlist['email'], playlist['name'])


def test_get_test_name():
    name = pls._get_test_name()
    assert isinstance(name, str)
    assert len(name) > 1


def test_get_test_email():
    email = pls._get_test_email()
    assert isinstance(email, str)
    assert len(email) > 0
    assert '@' in email


def test_get_test_playlist():
    assert isinstance(pls.get_test_playlist(), dict)
