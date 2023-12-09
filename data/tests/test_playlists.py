import pytest

import data.playlists as pls


@pytest.fixture(scope='function')
def temp_playlist():
    playlist = pls.get_test_playlist()
    ret = pls.add_playlist(playlist['email'], playlist['name'])
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


def test_get_playlists(temp_playlist):
    playlists = pls.get_playlists(temp_playlist['email'])
    assert isinstance(playlists, list)
    assert len(playlists) >= 0
    for name in playlists:
        assert isinstance(name, str)
        assert len(name) >= pls.MIN_NAME_LEN


def test_add_playlist():
    new_name = pls._get_test_name()
    new_email = pls._get_test_email()
    ret = pls.add_playlist(new_email, new_name)
    assert pls.already_exist(new_email, new_name)
    assert isinstance(ret, bool)
    pls.del_playlist(new_email, new_name)


def test_add_playlist_dup_name(temp_playlist):
    with pytest.raises(ValueError):
        pls.add_playlist(temp_playlist['email'], temp_playlist['name'])


def test_add_playlist_lt_1_char():
    new_name = ''
    new_email = pls._get_test_email()
    with pytest.raises(ValueError):
        pls.add_playlist(new_email, new_name)


def test_add_playlist_invalid_email():
    new_name = pls._get_test_name()
    new_email = 'randomstring'
    with pytest.raises(ValueError):
        pls.add_playlist(new_email, new_name)


def test_del_playlist(temp_playlist):
    email = temp_playlist['email']
    name = temp_playlist['name']
    pls.del_playlist(email, name)
    assert pls.already_exist(email, name) is False


def test_del_playlist_not_there():
    email = pls._get_test_email()
    name = pls._get_test_name()
    with pytest.raises(ValueError):
        pls.del_playlist(email, name)
